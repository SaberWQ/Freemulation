import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import sqlite3
import os
from PIL import Image, ImageTk
from core.config import THEME, FONT_UI, FONT_CODE

class SQLiteViewer(ctk.CTkFrame):
    def __init__(self, master, filepath, **kwargs):
        super().__init__(master, fg_color=THEME["bg_editor"], **kwargs)
        self.filepath = filepath
        
        header = ctk.CTkFrame(self, fg_color=THEME["bg_sidebar"], height=45, corner_radius=0)
        header.pack(fill="x")
        ctk.CTkLabel(header, text=f"🗄 БД Аналізатор: {os.path.basename(filepath)}", 
                     font=(FONT_UI[0], 12, "bold"), text_color=THEME["fg_text"]).pack(side="left", padx=15)

        self.table_var = ctk.StringVar(value="")
        self.table_dropdown = ctk.CTkOptionMenu(header, values=["Завантаження..."], variable=self.table_var, command=self.load_table_data)
        self.table_dropdown.pack(side="right", padx=15, pady=8)

        self.tree_container = ctk.CTkFrame(self, fg_color=THEME["bg_editor"])
        self.tree_container.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.load_tables()

    def load_tables(self):
        try:
            conn = sqlite3.connect(self.filepath)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [row[0] for row in cursor.fetchall()]
            conn.close()
            if tables:
                self.table_dropdown.configure(values=tables)
                self.table_var.set(tables[0])
                self.load_table_data(tables[0])
        except Exception as e:
            ctk.CTkLabel(self.tree_container, text=f"Помилка БД: {e}", text_color="#FF5555").pack(pady=20)

    def load_table_data(self, table_name):
        for widget in self.tree_container.winfo_children():
            widget.destroy()
        try:
            conn = sqlite3.connect(self.filepath)
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {table_name} LIMIT 200")
            rows = cursor.fetchall()
            cols = [desc[0] for desc in cursor.description]
            conn.close()

            tree = ttk.Treeview(self.tree_container, show="headings")
            tree.pack(fill="both", expand=True)
            tree["columns"] = cols
            for col in cols:
                tree.heading(col, text=col)
                tree.column(col, width=130, anchor="w")
            for row in rows:
                tree.insert("", "end", values=row)
        except Exception as e:
            ctk.CTkLabel(self.tree_container, text=f"Помилка таблиці: {e}", text_color="#FF5555").pack(pady=10)

class HexViewer(ctk.CTkFrame):
    def __init__(self, master, filepath, **kwargs):
        super().__init__(master, fg_color=THEME["bg_editor"], **kwargs)
        ctk.CTkLabel(self, text="⚡ Швидкий Hex-дамп бінарного файлу", font=(FONT_UI[0], 12, "bold"), text_color=THEME["fg_text"]).pack(pady=5)
        
        text_area = tk.Text(self, bg=THEME["bg_editor"], fg=THEME["fg_text"], font=FONT_CODE, bd=0, highlightthickness=0)
        text_area.pack(fill="both", expand=True, padx=10, pady=10)
        
        try:
            with open(filepath, "rb") as f:
                data = f.read(2048)
            hex_view = ""
            for i in range(0, len(data), 16):
                chunk = data[i:i+16]
                h_str = " ".join(f"{b:02X}" for b in chunk)
                a_str = "".join(chr(b) if 32 <= b <= 126 else "." for b in chunk)
                hex_view += f"{i:08X}  {h_str:<48}  |{a_str}|\n"
            text_area.insert("1.0", hex_view)
            text_area.config(state="disabled")
        except Exception as e:
            text_area.insert("1.0", f"Помилка читання файлу: {e}")

class ImageViewer(ctk.CTkFrame):
    def __init__(self, master, filepath, **kwargs):
        super().__init__(master, fg_color=THEME["bg_editor"], **kwargs)
        self.filepath = filepath
        
        try:
            self.original_image = Image.open(filepath)
        except Exception as e:
            ctk.CTkLabel(self, text=f"Помилка завантаження зображення: {e}", text_color="#FF5555").pack(expand=True)
            return

        # Контейнер для адаптивного центрування та ресайзу
        self.img_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.img_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.lbl = tk.Label(self.img_frame, bg=THEME["bg_editor"])
        self.lbl.pack(expand=True)

        self.info_lbl = ctk.CTkLabel(self, text="", font=FONT_UI, text_color=THEME["fg_muted"])
        self.info_lbl.pack(pady=5)

        # Динамічний ресайз при зміні розміру вікна
        self.bind("<Configure>", self.on_resize)

    def on_resize(self, event):
        if event.width < 50 or event.height < 50:
            return
        
        # Обчислюємо доступний простір для картинки
        target_w = max(100, event.width - 40)
        target_h = max(100, event.height - 60)

        img = self.original_image.copy()
        img.thumbnail((target_w, target_h))
        self.photo = ImageTk.PhotoImage(img)
        
        self.lbl.configure(image=self.photo)
        orig_w, orig_h = self.original_image.size
        self.info_lbl.configure(text=f"Формат: {self.original_image.format} | Оригінал: {orig_w}x{orig_h}px | Відображено: {img.size[0]}x{img.size[1]}px")