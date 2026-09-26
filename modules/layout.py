import tkinter as tk
import customtkinter as ctk
from modules.editor_ui import CodeEditor
from modules.palette_manager import palette
from modules.language_manager import lang_mgr

class MainLayout:
    def __init__(self, parent):
        self.parent = parent
        self.tab_keys = ["tab_problems", "tab_output", "tab_debug", "tab_terminal", "tab_ports"]
        self._build_layout()
        palette.subscribe(self.apply_colors)
        lang_mgr.subscribe(self.apply_language)

    def _build_layout(self):
        self.main_paned = tk.PanedWindow(self.parent, orient=tk.HORIZONTAL, bd=0, sashwidth=4)
        self.main_paned.pack(fill=tk.BOTH, expand=True)

        # Сайдбар
        self.sidebar = ctk.CTkFrame(self.main_paned, width=230, corner_radius=0)
        self.main_paned.add(self.sidebar, minsize=150)

        self.sidebar_title = ctk.CTkLabel(
            self.sidebar, text=lang_mgr.get("explorer"), font=("Arial", 11, "bold"), anchor="w"
        )
        self.sidebar_title.pack(fill="x", padx=15, pady=10)

        # Права частина
        self.right_paned = tk.PanedWindow(self.main_paned, orient=tk.VERTICAL, bd=0, sashwidth=4)
        self.main_paned.add(self.right_paned, minsize=400)

        self.editor = CodeEditor(self.right_paned)
        self.right_paned.add(self.editor, minsize=200)

        # Нижня панель
        self.bottom_panel = ctk.CTkTabview(self.right_paned, height=220, corner_radius=0)
        self.right_paned.add(self.bottom_panel, minsize=100)

        self._setup_tabs()

        self.terminal_text = tk.Text(
            self.bottom_panel.tab(lang_mgr.get("tab_terminal")),
            font=("SF Mono", 12) if "SF Mono" in tk.font.families() else ("Menlo", 12),
            bd=0, highlightthickness=0
        )
        self.terminal_text.pack(fill="both", expand=True, padx=5, pady=5)
        self.terminal_text.insert("1.0", "(base) getapple@GetApples-MacBook-Pro emulation % ")

        self.apply_colors()

    def _setup_tabs(self):
        for key in self.tab_keys:
            self.bottom_panel.add(lang_mgr.get(key))
        self.bottom_panel.set(lang_mgr.get("tab_terminal"))

    def apply_language(self):
        """Оновлення заголовку сайдбару та кнопок вкладок при зміні мови"""
        # 1. Заголовок сайдбару
        self.sidebar_title.configure(text=lang_mgr.get("explorer"))

        # 2. Оновлення назв вкладок нижньої панелі
        try:
            segmented_button = self.bottom_panel._segmented_button
            old_keys = list(segmented_button._buttons_dict.keys())
            
            for idx, key in enumerate(self.tab_keys):
                new_text = lang_mgr.get(key)
                if idx < len(old_keys):
                    old_name = old_keys[idx]
                    btn = segmented_button._buttons_dict[old_name]
                    btn.configure(text=new_text)
        except Exception:
            pass

    def apply_colors(self):
        bg_main = palette.get("bg_main")
        bg_sidebar = palette.get("bg_sidebar")
        bg_panel = palette.get("bg_panel")
        fg_text = palette.get("fg_text")
        fg_muted = palette.get("fg_muted")

        self.main_paned.config(bg=bg_main)
        self.right_paned.config(bg=bg_main)
        self.sidebar.configure(fg_color=bg_sidebar)
        self.sidebar_title.configure(text_color=fg_muted)

        self.bottom_panel.configure(fg_color=bg_panel)
        self.terminal_text.config(
            bg=bg_panel, fg=fg_text, insertbackground=fg_text
        )