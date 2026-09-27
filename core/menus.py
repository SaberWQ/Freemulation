import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
import customtkinter as ctk

from .config import THEME, DEFAULT_THEME, FONT_UI, FONT_CODE
from modules.palette_manager import palette
from modules.translator import TranslatorWindow
from modules.language_manager import lang_mgr
from modules.mini_browser import FreemulationBrowserWindow, FreemulationBrowserTab

class SettingsWindow(ctk.CTkToplevel):
    def __init__(self, master, update_callback=None):
        super().__init__(master)
        self.title("IDE Advanced Settings & Themes v1.0")
        self.geometry("650x700")
        self.minsize(450, 500)
        self.configure(fg_color=THEME["bg_editor"])
        self.update_callback = update_callback

        # Гнучке сіткове розміщення для адаптивності вікна
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self, 
            text="Повний кастомізатор інтерфейсу та тем v1.0", 
            font=(FONT_UI[0], 18, "bold"), 
            text_color=THEME["fg_text"]
        ).grid(row=0, column=0, pady=20, sticky="n")

        # Динамічний скролер
        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=5)
        self.scroll_frame.columnconfigure(0, weight=1)

        self.color_buttons = {}
        
        labels_map = {
            "bg_activity": "Активність панелі (Activity Bar)",
            "bg_sidebar": "Бічна панель (Sidebar / Explorer)",
            "bg_editor": "Фон редактора коду",
            "bg_panel": "Нижня панель / Термінал",
            "bg_tab_active": "Активна вкладка",
            "bg_tab_inactive": "Неактивна вкладка",
            "fg_text": "Основний колір тексту",
            "fg_accent": "Акцентний колір (Accent / Кнопки)",
            "fg_muted": "Приглушений текст",
            "border": "Колір меж та ліній розділювачів",
            "hover": "Колір при наведенні (Hover)"
        }

        for key, desc in labels_map.items():
            self.create_color_picker_row(desc, key)

        # Нижня панель кнопок
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=2, column=0, sticky="ew", padx=30, pady=20)
        btn_frame.columnconfigure(1, weight=1)

        ctk.CTkButton(
            btn_frame, text="Скинути за замовчуванням", fg_color="#C42B1C", 
            hover_color="#A82316", command=self.reset_defaults
        ).pack(side="left")
        
        ctk.CTkButton(
            btn_frame, text="Застосувати зміни", fg_color=THEME["fg_accent"], 
            command=self.apply_changes
        ).pack(side="right")

    def create_color_picker_row(self, label_text, key):
        row = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        row.pack(fill="x", padx=10, pady=8)
        
        ctk.CTkLabel(row, text=label_text, text_color=THEME["fg_text"], font=FONT_UI).pack(side="left", padx=5)
        
        btn = ctk.CTkButton(
            row, text=THEME.get(key, "#000000"), width=120, fg_color=THEME.get(key, "#000000"), 
            command=lambda k=key: self.pick_color(k)
        )
        btn.pack(side="right", padx=5)
        self.color_buttons[key] = btn

    def pick_color(self, key):
        color_code = colorchooser.askcolor(title=f"Виберіть колір для {key}")[1]
        if color_code:
            THEME[key] = color_code
            self.color_buttons[key].configure(fg_color=color_code, text=color_code)

    def reset_defaults(self):
        for key, val in DEFAULT_THEME.items():
            THEME[key] = val
            if key in self.color_buttons:
                self.color_buttons[key].configure(fg_color=val, text=val)
        if self.update_callback:
            self.update_callback()
        messagebox.showinfo("Скидання", "Тему успішно скинуто до заводських налаштувань версії 1.0!")

    def apply_changes(self):
        if self.update_callback:
            self.update_callback()
        messagebox.showinfo("Успіх", "Усі зміни оформлення застосовано динамічно!")
        self.destroy()


class VSCodeSettingsWindow(ctk.CTkToplevel):
    def __init__(self, master, update_callback=None):
        super().__init__(master)
        self.title("Налаштування (Settings)")
        self.geometry("850x600")
        self.minsize(650, 450)
        self.configure(fg_color=THEME["bg_editor"])
        self.update_callback = update_callback

        # Пошуковий рядок
        search_frame = ctk.CTkFrame(self, fg_color=THEME["bg_sidebar"], height=45)
        search_frame.pack(fill="x", side="top", padx=10, pady=10)
        
        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="🔍 Пошук налаштувань (Search settings)...", font=FONT_UI)
        self.search_entry.pack(fill="x", padx=15, pady=8)

        # Основний контент (Сайдбар + Область налаштувань)
        main_box = ctk.CTkFrame(self, fg_color="transparent")
        main_box.pack(fill="both", expand=True, padx=10, pady=5)

        # Категорії
        categories_frame = ctk.CTkFrame(main_box, width=180, fg_color=THEME["bg_sidebar"])
        categories_frame.pack(side="left", fill="y", padx=(0, 10))

        categories = [
            ("📝 Текстовий редактор", self.show_editor_settings),
            ("💻 Термінал", self.show_terminal_settings),
            ("🎨 Зовнішній вигляд", self.show_theme_settings),
            ("⌨️ Гарячі клавіші", self.show_keys_settings),
        ]

        for name, cmd in categories:
            btn = ctk.CTkButton(categories_frame, text=name, anchor="w", fg_color="transparent", hover_color=THEME["hover"], command=cmd)
            btn.pack(fill="x", padx=5, pady=4)

        # Контейнер для вмісту налаштувань
        self.content_frame = ctk.CTkScrollableFrame(main_box, fg_color=THEME["bg_sidebar"])
        self.content_frame.pack(side="right", fill="both", expand=True)

        self.show_editor_settings()

    def clear_content(self):
        for w in self.content_frame.winfo_children():
            w.destroy()

    def show_editor_settings(self):
        self.clear_content()
        ctk.CTkLabel(self.content_frame, text="Налаштування редактора", font=(FONT_UI[0], 16, "bold")).pack(anchor="w", pady=10)
        
        sw1 = ctk.CTkSwitch(self.content_frame, text="Автоматичне підсвічування дужок")
        sw1.select()
        sw1.pack(anchor="w", pady=8)

        sw2 = ctk.CTkSwitch(self.content_frame, text="Відображати номери рядків")
        sw2.select()
        sw2.pack(anchor="w", pady=8)

        sw3 = ctk.CTkSwitch(self.content_frame, text="Перенос слів (Word Wrap)")
        sw3.pack(anchor="w", pady=8)

    def show_terminal_settings(self):
        self.clear_content()
        ctk.CTkLabel(self.content_frame, text="Налаштування термінала", font=(FONT_UI[0], 16, "bold")).pack(anchor="w", pady=10)
        
        sw1 = ctk.CTkSwitch(self.content_frame, text="Відображати статус Git гілки в статусі")
        sw1.select()
        sw1.pack(anchor="w", pady=8)

        sw2 = ctk.CTkSwitch(self.content_frame, text="Зберігати історію сесій")
        sw2.select()
        sw2.pack(anchor="w", pady=8)

    def show_theme_settings(self):
        self.clear_content()
        ctk.CTkLabel(self.content_frame, text="Кастомізація кольорів інтерфейсу", font=(FONT_UI[0], 16, "bold")).pack(anchor="w", pady=10)
        
        for key, val in THEME.items():
            row = ctk.CTkFrame(self.content_frame, fg_color="transparent")
            row.pack(fill="x", pady=4)
            ctk.CTkLabel(row, text=key, font=FONT_UI).pack(side="left")
            btn = ctk.CTkButton(row, text=val, width=100, fg_color=val)
            btn.pack(side="right")

    def show_keys_settings(self):
        self.clear_content()
        ctk.CTkLabel(self.content_frame, text="Прив'язка гарячих клавіш", font=(FONT_UI[0], 16, "bold")).pack(anchor="w", pady=10)
        shortcuts = [
            ("Міні-браузер", "Ctrl+B / Cmd+B"),
            ("Швидкий перекладач", "Ctrl+T / Cmd+T"),
            ("Зберегти файл", "Ctrl+S / Cmd+S"),
            ("Запуск аналізу", "F5"),
        ]
        for name, key in shortcuts:
            row = ctk.CTkFrame(self.content_frame, fg_color="transparent")
            row.pack(fill="x", pady=4)
            ctk.CTkLabel(row, text=name, font=FONT_UI).pack(side="left")
            ctk.CTkLabel(row, text=key, font=FONT_CODE, text_color=THEME["fg_accent"]).pack(side="right")


class MenuManager:
    def __init__(self, root, layout_ref=None):
        self.root = root
        self.layout = layout_ref
        self._current_file_path = None
        
        # Підписка на автоматичне перезавантаження мови
        lang_mgr.subscribe(self.rebuild_menu)
        
        self.rebuild_menu()
        self._bind_hotkeys()

    def rebuild_menu(self):
        """Перезбирання меню з примусовим оновленням для macOS Cocoa Bar"""
        self.root.config(menu="")  # Відв'язуємо старе меню
        
        self.menubar = tk.Menu(self.root)  # Створюємо новий об'єкт

        self._create_file_menu()
        self._create_edit_menu()
        self._create_tools_menu()
        self._create_run_menu()
        self._create_terminal_menu()
        self._create_palette_menu()
        self._create_language_menu()

        self.root.config(menu=self.menubar)  # Прив'язуємо нове меню
        self.root.update_idletasks()        # Примушуємо macOS перемалювати панель

    def _bind_hotkeys(self):
        """Реєстрація обробників гарячих клавіш для macOS (Command) та Win/Linux (Control)"""
        # Файл
        self.root.bind_all("<Command-n>", lambda e: self._new_file())
        self.root.bind_all("<Control-n>", lambda e: self._new_file())
        self.root.bind_all("<Command-o>", lambda e: self._open_file())
        self.root.bind_all("<Control-o>", lambda e: self._open_file())
        self.root.bind_all("<Command-s>", lambda e: self._save_file())
        self.root.bind_all("<Control-s>", lambda e: self._save_file())
        self.root.bind_all("<Command-Shift-S>", lambda e: self._save_file_as())
        self.root.bind_all("<Control-Shift-S>", lambda e: self._save_file_as())

        # Редагування
        self.root.bind_all("<Command-a>", lambda e: self._select_all())
        self.root.bind_all("<Control-a>", lambda e: self._select_all())

        # Інструменти
        self.root.bind_all("<Command-b>", lambda e: self._open_browser())
        self.root.bind_all("<Control-b>", lambda e: self._open_browser())
        self.root.bind_all("<Command-t>", lambda e: self._open_translator())
        self.root.bind_all("<Control-t>", lambda e: self._open_translator())
        self.root.bind_all("<F5>", lambda e: self._run_fast_analysis())

    def _create_file_menu(self):
        m = tk.Menu(self.menubar, tearoff=0)
        m.add_command(label=lang_mgr.get("new_file"), accelerator="Cmd+N", command=self._new_file)
        m.add_command(label=lang_mgr.get("open_file"), accelerator="Cmd+O", command=self._open_file)
        m.add_separator()
        m.add_command(label=lang_mgr.get("save"), accelerator="Cmd+S", command=self._save_file)
        m.add_command(label=lang_mgr.get("save_as"), accelerator="Shift+Cmd+S", command=self._save_file_as)
        m.add_separator()
        m.add_command(label=lang_mgr.get("exit"), command=self.root.destroy)
        self.menubar.add_cascade(label=lang_mgr.get("file"), menu=m)

    def _create_edit_menu(self):
        m = tk.Menu(self.menubar, tearoff=0)
        m.add_command(label=lang_mgr.get("undo"), accelerator="Cmd+Z", command=lambda: self._exec_editor("<<Undo>>"))
        m.add_command(label=lang_mgr.get("redo"), accelerator="Shift+Cmd+Z", command=lambda: self._exec_editor("<<Redo>>"))
        m.add_separator()
        m.add_command(label=lang_mgr.get("cut"), accelerator="Cmd+X", command=lambda: self._exec_editor("<<Cut>>"))
        m.add_command(label=lang_mgr.get("copy"), accelerator="Cmd+C", command=lambda: self._exec_editor("<<Copy>>"))
        m.add_command(label=lang_mgr.get("paste"), accelerator="Cmd+V", command=lambda: self._exec_editor("<<Paste>>"))
        m.add_separator()
        m.add_command(label=lang_mgr.get("select_all"), accelerator="Cmd+A", command=self._select_all)
        self.menubar.add_cascade(label=lang_mgr.get("edit"), menu=m)

    def _create_tools_menu(self):
        m = tk.Menu(self.menubar, tearoff=0)
        m.add_command(label=lang_mgr.get("mini_browser"), accelerator="Cmd+B", command=self._open_browser)
        m.add_command(label=lang_mgr.get("translator"), accelerator="Cmd+T", command=self._open_translator)
        m.add_command(label=lang_mgr.get("translate_sel"), command=self._translate_selection)
        self.menubar.add_cascade(label=lang_mgr.get("tools"), menu=m)
    
    def _open_browser(self):
        FreemulationBrowserWindow(self.root)

    def _create_run_menu(self):
        m = tk.Menu(self.menubar, tearoff=0)
        m.add_command(label=lang_mgr.get("analyze"), accelerator="F5", command=self._run_fast_analysis)
        self.menubar.add_cascade(label=lang_mgr.get("run"), menu=m)

    def _create_terminal_menu(self):
        m = tk.Menu(self.menubar, tearoff=0)
        m.add_command(label=lang_mgr.get("clear_terminal"), command=self._clear_terminal)
        self.menubar.add_cascade(label=lang_mgr.get("terminal"), menu=m)

    def _create_palette_menu(self):
        p_menu = tk.Menu(self.menubar, tearoff=0)

        presets_menu = tk.Menu(p_menu, tearoff=0)
        for name in palette.PRESETS.keys():
            presets_menu.add_command(
                label=name,
                command=lambda p_name=name: palette.set_preset(p_name)
            )
        p_menu.add_cascade(label=lang_mgr.get("presets"), menu=presets_menu)
        p_menu.add_separator()

        custom_menu = tk.Menu(p_menu, tearoff=0)
        items = [
            ("editor_bg", "editor_bg"),
            ("editor_fg", "editor_fg"),
            ("editor_cursor", "editor_cursor"),
            ("editor_select", "editor_select"),
            ("bg_sidebar", "bg_sidebar"),
            ("bg_panel", "bg_panel"),
            ("line_numbers_fg", "line_numbers_fg"),
        ]
        for label_key, key in items:
            custom_menu.add_command(
                label=label_key,
                command=lambda k=key: self._pick_color(k)
            )

        p_menu.add_cascade(label=lang_mgr.get("custom_colors"), menu=custom_menu)
        self.menubar.add_cascade(label=lang_mgr.get("palette"), menu=p_menu)

    def _create_language_menu(self):
        lang_menu = tk.Menu(self.menubar, tearoff=0)
        for name, code in lang_mgr.LANG_NAMES.items():
            lang_menu.add_command(
                label=name,
                command=lambda c=code: lang_mgr.set_language(c)
            )
        self.menubar.add_cascade(label=lang_mgr.get("language"), menu=lang_menu)

    # --- Обробники дій та команд ---

    def _exec_editor(self, event_name):
        if self.layout and hasattr(self.layout, 'editor') and hasattr(self.layout.editor, 'text_area'):
            self.layout.editor.text_area.event_generate(event_name)

    def _select_all(self):
        if self.layout and hasattr(self.layout, 'editor') and hasattr(self.layout.editor, 'text_area'):
            self.layout.editor.text_area.tag_add("sel", "1.0", "end")
            return "break"

    def _new_file(self):
        if self.layout and hasattr(self.layout, 'editor') and hasattr(self.layout.editor, 'text_area'):
            self.layout.editor.text_area.delete("1.0", "end")
            if hasattr(self.layout.editor, '_update_line_numbers'):
                self.layout.editor._update_line_numbers()

    def _open_file(self):
        path = filedialog.askopenfilename(filetypes=[("Усі файли", "*.*"), ("Python", "*.py")])
        if path and self.layout and hasattr(self.layout, 'editor') and hasattr(self.layout.editor, 'text_area'):
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            self.layout.editor.text_area.delete("1.0", "end")
            self.layout.editor.text_area.insert("1.0", content)
            if hasattr(self.layout.editor, '_update_line_numbers'):
                self.layout.editor._update_line_numbers()

    def _save_file(self):
        if self._current_file_path:
            if self.layout and hasattr(self.layout, 'editor') and hasattr(self.layout.editor, 'text_area'):
                content = self.layout.editor.text_area.get("1.0", "end-1c")
                with open(self._current_file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                messagebox.showinfo("Збереження", "Файл успішно збережено!")
        else:
            self._save_file_as()

    def _save_file_as(self):
        path = filedialog.asksaveasfilename(filetypes=[("Python", "*.py"), ("Усі файли", "*.*")])
        if path and self.layout and hasattr(self.layout, 'editor') and hasattr(self.layout.editor, 'text_area'):
            self._current_file_path = path
            content = self.layout.editor.text_area.get("1.0", "end-1c")
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            messagebox.showinfo("Збереження", "Файл збережено успішно!")

    def _open_translator(self):
        selected_text = ""
        if self.layout and hasattr(self.layout, 'editor') and hasattr(self.layout.editor, 'text_area'):
            try:
                selected_text = self.layout.editor.text_area.get("sel.first", "sel.last")
            except tk.TclError:
                selected_text = ""

        def replace_cb(new_text):
            if self.layout and hasattr(self.layout, 'editor') and hasattr(self.layout.editor, 'text_area'):
                try:
                    self.layout.editor.text_area.delete("sel.first", "sel.last")
                    self.layout.editor.text_area.insert("insert", new_text)
                except tk.TclError:
                    self.layout.editor.text_area.insert("insert", new_text)

        TranslatorWindow(self.root, initial_text=selected_text, on_insert_callback=replace_cb)

    def _translate_selection(self):
        self._open_translator()

    def _run_fast_analysis(self):
        if self.layout and hasattr(self.layout, 'editor') and hasattr(self.layout.editor, 'run_cpp_analysis'):
            self.layout.editor.run_cpp_analysis()

    def _clear_terminal(self):
        if self.layout and hasattr(self.layout, 'terminal_text'):
            self.layout.terminal_text.delete("1.0", "end")
            self.layout.terminal_text.insert("1.0", "(base) getapple@GetApples-MacBook-Pro emulation % ")

    def _pick_color(self, key):
        curr = palette.get(key)
        color = colorchooser.askcolor(color=curr, title=f"Обери колір для {key}")
        if color[1]:
            palette.set_color(key, color[1])