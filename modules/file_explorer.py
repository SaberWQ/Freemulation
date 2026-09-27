import os
from tkinter import filedialog, ttk
import customtkinter as ctk
from core.config import THEME, FONT_UI


class FileExplorerPanel(ctk.CTkFrame):
    """Ліва панель проєкту з можливістю відкриття папок як у VS Code"""
    def __init__(self, master, on_file_select_callback, **kwargs):
        super().__init__(master, width=220, fg_color=THEME["bg_sidebar"], **kwargs)
        self.on_file_select = on_file_select_callback
        self.current_folder = None

        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        # Верхня панель
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=8, pady=8)
        
        ctk.CTkLabel(header, text="ПРОЄКТ", font=(FONT_UI[0], 12, "bold"), text_color=THEME["fg_muted"]).pack(side="left")
        ctk.CTkButton(header, text="📁 Відкрити", width=70, height=24, fg_color=THEME["fg_accent"], command=self.open_folder).pack(side="right")

        # Дерево файлів (Treeview)
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background=THEME["bg_sidebar"], foreground=THEME["fg_text"], fieldbackground=THEME["bg_sidebar"], borderwidth=0)
        style.map("Treeview", background=[("selected", THEME["fg_accent"])])

        self.tree = ttk.Treeview(self, show="tree", selectmode="browse")
        self.tree.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.tree.bind("<Double-1>", self._on_double_click)

    def open_folder(self):
        folder = filedialog.askdirectory(title="Виберіть папку проєкту")
        if folder:
            self.current_folder = folder
            self.refresh_tree()

    def refresh_tree(self):
        self.tree.delete(*self.tree.get_children())
        if not self.current_folder:
            return
        
        root_node = self.tree.insert("", "end", text=f" 📂 {os.path.basename(self.current_folder)}", open=True, values=[self.current_folder])
        self._populate_node(root_node, self.current_folder)

    def _populate_node(self, parent, path):
        try:
            entries = sorted(os.listdir(path), key=lambda x: (not os.path.isdir(os.path.join(path, x)), x.lower()))
            for entry in entries:
                if entry.startswith("."):
                    continue
                full_path = os.path.join(path, entry)
                is_dir = os.path.isdir(full_path)
                icon = "📁 " if is_dir else "📄 "
                
                node = self.tree.insert(parent, "end", text=f"{icon}{entry}", values=[full_path])
                if is_dir:
                    # Додаємо пустий елемент для можливості розгортання
                    self.tree.insert(node, "end", text="...")
        except PermissionError:
            pass

    def _on_double_click(self, event):
        item_id = self.tree.selection()[0]
        values = self.tree.item(item_id, "values")
        if values:
            file_path = values[0]
            if os.path.isfile(file_path):
                self.on_file_select(file_path)