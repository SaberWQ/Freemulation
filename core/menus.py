import tkinter as tk
from tkinter import colorchooser, messagebox
import customtkinter as ctk
from .config import THEME, DEFAULT_THEME, FONT_UI


class SettingsWindow(ctk.CTkToplevel):
    def __init__(self, master, update_callback):
        super().__init__(master)
        self.title("IDE Advanced Settings & Themes v1.0")
        self.geometry("650x700")
        self.minsize(450, 500)
        self.configure(fg_color=THEME["bg_editor"])
        self.update_callback = update_callback

        # Гнучке сіткове розміщення для ідеальної адаптивності вікна
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self, text="Повний кастомізатор інтерфейсу та тем v1.0", 
            font=(FONT_UI[0], 18, "bold"), text_color=THEME["fg_text"]
        ).grid(row=0, column=0, pady=20, sticky="n")

        # Динамічний скролер, який розтягується разом із вікном
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

        # Нижня панель кнопок із фіксованим притисканням до низу
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
            row, text=THEME[key], width=120, fg_color=THEME[key], 
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
        self.update_callback()
        messagebox.showinfo("Скидання", "Тему успішно скинуто до заводських налаштувань версії 1.0!")

    def apply_changes(self):
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
            ("Нова вкладка термінала", "Ctrl+Shift+T / Cmd+Shift+T"),
            ("Швидкий пошук", "Ctrl+F / Cmd+F"),
            ("Зберегти файл", "Ctrl+S / Cmd+S"),
            ("Панель налаштувань", "Ctrl+, / Cmd+,"),
        ]
        for name, key in shortcuts:
            row = ctk.CTkFrame(self.content_frame, fg_color="transparent")
            row.pack(fill="x", pady=4)
            ctk.CTkLabel(row, text=name, font=FONT_UI).pack(side="left")
            ctk.CTkLabel(row, text=key, font=FONT_CODE, text_color=THEME["fg_accent"]).pack(side="right")