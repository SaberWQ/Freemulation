import customtkinter as ctk

from core.config import THEME
from modules.file_explorer import FileExplorerPanel
from modules.code_runner import CodeRunnerPanel
from modules.mini_browser import FreemulationBrowserTab


class FreemulationIDE(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Freemulation IDE")
        self.geometry("1200x800")
        self.configure(fg_color=THEME["bg_editor"])

        # Головна сітка
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        # 1. Ліва панель (File Explorer)
        self.sidebar = FileExplorerPanel(self, on_file_select_callback=self.open_file_in_tab)
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=(5, 0), pady=5)

        # 2. Права частина: Вкладки коду/браузера + Консоль
        right_container = ctk.CTkFrame(self, fg_color="transparent")
        right_container.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        right_container.rowconfigure(1, weight=1)
        right_container.columnconfigure(0, weight=1)

        # Верхні кнопки дій
        action_bar = ctk.CTkFrame(right_container, fg_color=THEME["bg_sidebar"], height=35)
        action_bar.grid(row=0, column=0, sticky="ew", pady=(0, 5))
        
        ctk.CTkButton(action_bar, text="▶ Запустити код", width=110, fg_color="#2E7D32", command=self.run_current_code).pack(side="left", padx=5, pady=4)
        ctk.CTkButton(action_bar, text="🌐 Відкрити браузер у вкладці", width=180, fg_color=THEME["fg_accent"], command=self.open_browser_tab).pack(side="left", padx=5, pady=4)

        # Горизонтальні вкладки (Tabview)
        self.tabview = ctk.CTkTabview(right_container, fg_color=THEME["bg_sidebar"])
        self.tabview.grid(row=1, column=0, sticky="nsew")

        # 3. Нижня консоль запуску
        self.runner_panel = CodeRunnerPanel(self)
        self.runner_panel.grid(row=1, column=1, sticky="ew", padx=5, pady=(0, 5))

        self.active_files = {}  # tab_name -> file_path

    def open_file_in_tab(self, file_path: str):
        file_name = os.path.basename(file_path)
        tab_name = f"📄 {file_name}"

        if tab_name in self.tabview._tab_dict:
            self.tabview.set(tab_name)
            return

        tab = self.tabview.add(tab_name)
        editor = ctk.CTkTextbox(tab, font=("Courier", 13), fg_color=THEME["bg_editor"])
        editor.pack(fill="both", expand=True)

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                editor.insert("1.0", f.read())
        except Exception as e:
            editor.insert("1.0", f"Помилка читання файлу: {e}")

        self.active_files[tab_name] = file_path
        self.tabview.set(tab_name)

    def open_browser_tab(self):
        tab_count = len([t for t in self.tabview._tab_dict if t.startswith("🌐 Browser")]) + 1
        tab_name = f"🌐 Browser {tab_count}"
        
        tab = self.tabview.add(tab_name)
        browser = FreemulationBrowserTab(tab)
        browser.pack(fill="both", expand=True)
        self.tabview.set(tab_name)

    def run_current_code(self):
        current_tab = self.tabview.get()
        file_path = self.active_files.get(current_tab)
        if file_path:
            self.runner_panel.run_file(file_path)
        else:
            self.runner_panel.write("⚠️ Відкрийте збережений файл проєкту для запуску.\n")


if __name__ == "__main__":
    app = FreemulationIDE()
    app.mainloop()