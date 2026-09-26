import tkinter as tk
import customtkinter as ctk
import re
from core.config import THEME, FONT_CODE

class SyntaxCodeEditor(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=THEME["bg_editor"], **kwargs)

        self.line_numbers = tk.Text(
            self, width=4, bg=THEME["bg_sidebar"], fg=THEME["fg_muted"],
            font=FONT_CODE, bd=0, highlightthickness=0, state="disabled"
        )
        self.line_numbers.pack(side="left", fill="y")

        self.text_area = tk.Text(
            self, bg=THEME["bg_editor"], fg=THEME["fg_text"],
            font=FONT_CODE, bd=0, highlightthickness=0, undo=True, wrap="none"
        )
        self.text_area.pack(side="right", fill="both", expand=True)

        self.setup_tags()
        self.text_area.bind("<KeyRelease>", self.on_content_changed)
        self.text_area.bind("<MouseWheel>", self.sync_scroll)
        self.text_area.bind("<Button-4>", self.sync_scroll)
        self.text_area.bind("<Button-5>", self.sync_scroll)

    def setup_tags(self):
        self.text_area.tag_configure("keyword", foreground="#569CD6")
        self.text_area.tag_configure("string", foreground="#CE9178")
        self.text_area.tag_configure("comment", foreground="#6A9955")
        self.text_area.tag_configure("number", foreground="#B5CEA8")

    def on_content_changed(self, event=None):
        self.update_line_numbers()
        self.apply_highlighting()

    def update_line_numbers(self):
        lines = self.text_area.get("1.0", "end-1c").split("\n")
        num_str = "\n".join(str(i) for i in range(1, len(lines) + 1))
        self.line_numbers.config(state="normal")
        self.line_numbers.delete("1.0", "end")
        self.line_numbers.insert("1.0", num_str)
        self.line_numbers.config(state="disabled")

    def sync_scroll(self, event=None):
        self.line_numbers.yview_moveto(self.text_area.yview()[0])

    def apply_highlighting(self):
        content = self.text_area.get("1.0", "end-1c")
        for tag in ["keyword", "string", "comment", "number"]:
            self.text_area.tag_remove(tag, "1.0", "end")

        rules = [
            (r'\b(def|class|import|from|return|if|else|elif|for|while|try|except|with|as|int|void|auto|include|public|private)\b', "keyword"),
            (r'".*?"|\'.*?\'', "string"),
            (r'#.*$|//.*$', "comment"),
            (r'\b\d+\b', "number")
        ]

        for pattern, tag in rules:
            for match in re.finditer(pattern, content, re.MULTILINE):
                start = f"1.0 + {match.start()} chars"
                end = f"1.0 + {match.end()} chars"
                self.text_area.tag_add(tag, start, end)

# Псевдонім для сумісності з іншими модулями проєкту
CodeEditor = SyntaxCodeEditor