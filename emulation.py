import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import customtkinter as ctk

from core.config import THEME, FONT_UI
from core.terminal import TerminalTab
from core.menus import SettingsWindow
from modules.editor import CodeEditor
from modules.analyzer import SQLiteViewer, HexViewer, ImageViewer

class VSCodeMasterProMax(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("VS Code Master Pro Max Edition")
        self.geometry("1600x950")
        self.configure(fg_color=THEME["bg_editor"])

        self.current_workspace = os.getcwd()
        self.open_tabs = {}
        self.active_filepath = None
        self.terminal_tabs = []

        self.build_top_menu()
        self.build_layout()
        self.populate_explorer(self.current_workspace)

    def build_top_menu(self):
        self.menubar = tk.Menu(self, bg=THEME["bg_sidebar"], fg=THEME["fg_text"], activebackground=THEME["fg_accent"], bd=0)
        
        file_menu = tk.Menu(self.menubar, tearoff=0, bg=THEME["bg_sidebar"], fg=THEME["fg_text"])
        file_menu.add_command(label="Відкрити папку...", command=self.select_folder)
        file_menu.add_command(label="Зберегти поточний файл", command=self.save_current)
        file_menu.add_separator()
        file_menu.add_command(label="Вихід", command=self.quit)
        self.menubar.add_cascade(label="File", menu=file_menu)

        settings_menu = tk.Menu(self.menubar, tearoff=0, bg=THEME["bg_sidebar"], fg=THEME["fg_text"])
        settings_menu.add_command(label="Кастомізатор тем та кольорів", command=self.open_settings_window)
        self.menubar.add_cascade(label="Settings", menu=settings_menu)

        self.config(menu=self.menubar)

    def build_layout(self):
        # 1. Activity Bar
        self.activity_bar = ctk.CTkFrame(self, fg_color=THEME["bg_activity"], width=52, corner_radius=0)
        self.activity_bar.pack(side="left", fill="y")

        ctk.CTkButton(self.activity_bar, text="📁", width=42, height=42, fg_color="transparent", font=("Arial", 18), command=self.select_folder).pack(pady=10)
        ctk.CTkButton(self.activity_bar, text="⚙", width=42, height=42, fg_color="transparent", font=("Arial", 18), command=self.open_settings_window).pack(side="bottom", pady=10)

        # 2. Головний PanedWindow (Explorer | Робоча область з можливістю повного ресайзу)
        self.main_paned = tk.PanedWindow(self, orient="horizontal", bg=THEME["border"], bd=0, sashwidth=4)
        self.main_paned.pack(fill="both", expand=True)

        # Провідник
        self.sidebar = ctk.CTkFrame(self.main_paned, fg_color=THEME["bg_sidebar"], corner_radius=0)
        self.main_paned.add(self.sidebar, width=270, minsize=150)
        
        ctk.CTkLabel(self.sidebar, text="EXPLORER", font=(FONT_UI[0], 11, "bold"), text_color=THEME["fg_text"], anchor="w").pack(fill="x", padx=12, pady=6)
        
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background=THEME["bg_sidebar"], fieldbackground=THEME["bg_sidebar"], foreground=THEME["fg_text"], borderwidth=0, font=FONT_UI)
        style.map("Treeview", background=[("selected", THEME["hover"])])

        self.tree = ttk.Treeview(self.sidebar, show="tree", selectmode="browse")
        self.tree.pack(fill="both", expand=True, padx=2, pady=2)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        # 3. Правий вертикальний блок (Вкладки файлів + Редактор + Ресайзабельна нижня панель)
        self.right_paned = tk.PanedWindow(self.main_paned, orient="vertical", bg=THEME["border"], bd=0, sashwidth=4)
        self.main_paned.add(self.right_paned, stretch="always")

        self.tabs_bar = ctk.CTkFrame(self.right_paned, fg_color=THEME["bg_sidebar"], corner_radius=0, height=36)
        self.right_paned.add(self.tabs_bar, stretch="never")

        self.editor_container = ctk.CTkFrame(self.right_paned, fg_color=THEME["bg_editor"], corner_radius=0)
        self.right_paned.add(self.editor_container, stretch="always", minsize=200)

        # Нижня панель (Термінали з можливістю ресайзу та закриття)
        self.bottom_container = ctk.CTkFrame(self.right_paned, fg_color=THEME["bg_panel"], corner_radius=0)
        self.right_paned.add(self.bottom_container, stretch="never", minsize=120)

        bottom_top_bar = ctk.CTkFrame(self.bottom_container, fg_color=THEME["bg_sidebar"], height=30, corner_radius=0)
        bottom_top_bar.pack(fill="x")
        ctk.CTkLabel(bottom_top_bar, text="  PANEL", font=(FONT_UI[0], 10, "bold"), text_color=THEME["fg_text"]).pack(side="left")
        
        ctk.CTkButton(bottom_top_bar, text="+ Новий термінал", width=110, height=22, fg_color=THEME["fg_accent"], command=self.add_terminal_tab).pack(side="right", padx=5)

        self.bottom_notebook = ttk.Notebook(self.bottom_container)
        self.bottom_notebook.pack(fill="both", expand=True)

        self.setup_problems_panel()
        self.add_terminal_tab()

    def setup_problems_panel(self):
        problems_frame = ctk.CTkFrame(self.bottom_notebook, fg_color=THEME["bg_panel"])
        self.bottom_notebook.add(problems_frame, text="Problems (0)")
        ctk.CTkLabel(problems_frame, text="У проєкті не виявлено жодних синтаксичних чи логічних проблем.", text_color=THEME["fg_muted"]).pack(expand=True)

    def add_terminal_tab(self):
        term_frame = TerminalTab(self.bottom_notebook, close_callback=self.close_terminal_tab)
        tab_title = f"Термінал {len(self.terminal_tabs) + 1}"
        self.bottom_notebook.add(term_frame, text=tab_title)
        self.bottom_notebook.select(term_frame)
        self.terminal_tabs.append((term_frame, tab_title))

    def close_terminal_tab(self, term_frame):
        for i, (tab, title) in enumerate(self.terminal_tabs):
            if tab == term_frame:
                self.bottom_notebook.forget(tab)
                tab.destroy()
                self.terminal_tabs.pop(i)
                break

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.current_workspace = folder
            self.populate_explorer(folder)

    def populate_explorer(self, path):
        self.tree.delete(*self.tree.get_children())
        root = self.tree.insert("", "end", text=f" 📁 {os.path.basename(path)}", open=True)
        self._build_tree(root, path)

    def _build_tree(self, parent, path):
        try:
            for item in sorted(os.listdir(path)):
                if item.startswith('.'): continue
                abs_path = os.path.join(path, item)
                if os.path.isdir(abs_path):
                    node = self.tree.insert(parent, "end", text=f" 📁 {item}", values=(abs_path, "dir"))
                    self.tree.insert(node, "end", text="dummy")
                else:
                    self.tree.insert(parent, "end", text=f" 📄 {item}", values=(abs_path, "file"))
        except PermissionError:
            pass

    def on_tree_select(self, event):
        selected = self.tree.selection()
        if not selected: return
        values = self.tree.item(selected[0], "values")
        if not values: return
        filepath, ftype = values[0], values[1]
        
        if ftype == "dir":
            children = self.tree.get_children(selected[0])
            if len(children) == 1 and self.tree.item(children[0], "text") == "dummy":
                self.tree.delete(children[0])
                self._build_tree(selected[0], filepath)
        elif ftype == "file":
            self.open_file(filepath)

    def open_file(self, filepath):
        if filepath in self.open_tabs:
            self.switch_to_tab(filepath)
            return

        ext = os.path.splitext(filepath)[1].lower()
        if self.active_filepath and self.active_filepath in self.open_tabs:
            self.open_tabs[self.active_filepath]["frame"].pack_forget()

        try:
            if ext in ['.py', '.js', '.html', '.css', '.json', '.md', '.txt', '.pyx']:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                frame = CodeEditor(self.editor_container, filepath, content)
                ftype = "code"
            elif ext in ['.db', '.sqlite', '.sqlite3']:
                frame = SQLiteViewer(self.editor_container, filepath)
                ftype = "db"
            elif ext in ['.png', '.jpg', '.jpeg']:
                frame = ImageViewer(self.editor_container, filepath)
                ftype = "image"
            else:
                frame = HexViewer(self.editor_container, filepath)
                ftype = "hex"

            frame.pack(fill="both", expand=True)

            tab_btn_frame = ctk.CTkFrame(self.tabs_bar, fg_color=THEME["bg_tab_active"], corner_radius=0, height=36)
            tab_btn_frame.pack(side="left", padx=1)
            
            lbl = ctk.CTkLabel(tab_btn_frame, text=os.path.basename(filepath), text_color=THEME["fg_text"], font=FONT_UI)
            lbl.pack(side="left", padx=(10, 5), pady=6)
            lbl.bind("<Button-1>", lambda e: self.switch_to_tab(filepath))

            close_btn = ctk.CTkButton(tab_btn_frame, text="×", width=22, height=22, fg_color="transparent", text_color=THEME["fg_text"], hover_color="#C42B1C", command=lambda: self.close_tab(filepath))
            close_btn.pack(side="left", padx=(0, 5))

            self.open_tabs[filepath] = {"frame": frame, "tab_frame": tab_btn_frame, "type": ftype}
            self.active_filepath = filepath
            self.update_tabs_style()
        except Exception as e:
            print(f"Помилка відкриття файлу: {e}")

    def switch_to_tab(self, filepath):
        if self.active_filepath == filepath: return
        if self.active_filepath and self.active_filepath in self.open_tabs:
            self.open_tabs[self.active_filepath]["frame"].pack_forget()
        if filepath in self.open_tabs:
            self.open_tabs[filepath]["frame"].pack(fill="both", expand=True)
            self.active_filepath = filepath
            self.update_tabs_style()

    def close_tab(self, filepath):
        if filepath not in self.open_tabs: return
        info = self.open_tabs[filepath]
        info["frame"].destroy()
        info["tab_frame"].destroy()
        del self.open_tabs[filepath]

        if self.active_filepath == filepath:
            self.active_filepath = None
            remaining = list(self.open_tabs.keys())
            if remaining:
                self.switch_to_tab(remaining[-1])

    def update_tabs_style(self):
        for path, info in self.open_tabs.items():
            color = THEME["bg_tab_active"] if path == self.active_filepath else THEME["bg_tab_inactive"]
            info["tab_frame"].configure(fg_color=color)

    def save_current(self):
        if self.active_filepath and self.active_filepath in self.open_tabs:
            if self.open_tabs[self.active_filepath]["type"] == "code":
                self.open_tabs[self.active_filepath]["frame"].save_file()

    def open_settings_window(self):
        SettingsWindow(self, self.refresh_theme)

    def refresh_theme(self):
        self.configure(fg_color=THEME["bg_editor"])
        self.sidebar.configure(fg_color=THEME["bg_sidebar"])
        self.tabs_bar.configure(fg_color=THEME["bg_sidebar"])
        self.activity_bar.configure(fg_color=THEME["bg_activity"])
        self.bottom_container.configure(fg_color=THEME["bg_panel"])
        self.menubar.config(bg=THEME["bg_sidebar"], fg=THEME["fg_text"])


if __name__ == "__main__":
    app = VSCodeMasterProMax()
    app.mainloop()