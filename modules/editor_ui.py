import tkinter as tk
import tkinter.font as tkfont
import customtkinter as ctk
from modules.palette_manager import palette

# Пробуємо імпортувати C++/Cython модуль з fallback на Python
try:
    from fast_core.fast_analyzer import analyze_code_fast
    HAS_CYTHON = True
except ImportError:
    HAS_CYTHON = False

class CodeEditor(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, corner_radius=0, **kwargs)

        # Налаштування красивого моноширинного шрифту для macOS
        self.font = tkfont.Font(family="SF Mono", size=13)
        if "SF Mono" not in tkfont.families():
            self.font = tkfont.Font(family="Menlo", size=13)

        # Права нумерація рядків з відступами
        self.line_numbers = tk.Text(
            self, width=5, padx=8, pady=6, takefocus=0, border=0,
            font=self.font, state="disabled", spacing1=2, spacing3=2
        )
        self.line_numbers.tag_configure("right", justify="right")
        self.line_numbers.pack(side="left", fill="y")

        # Головне текстове поле редактора
        self.text_area = tk.Text(
            self, font=self.font, bd=0, highlightthickness=0,
            undo=True, wrap="none", spacing1=2, spacing3=2,
            padx=10, pady=6, tabs=(self.font.measure("    "),)
        )
        self.text_area.pack(side="right", fill="both", expand=True)

        self.text_area.bind("<KeyRelease>", self._update_line_numbers)
        self.text_area.bind("<MouseWheel>", self._update_line_numbers)

        palette.subscribe(self.apply_colors)
        self.apply_colors()
        self._insert_demo_code()

    def _insert_demo_code(self):
        demo = '# Freemulation IDE\n\ndef main():\n    print("Ласкаво просимо в оновлений Freemulation IDE!")\n\nif __name__ == "__main__":\n    main()\n'
        self.text_area.insert("1.0", demo)
        self._update_line_numbers()

    def _update_line_numbers(self, event=None):
        lines = self.text_area.get("1.0", "end-1c").count("\n") + 1
        line_string = "\n".join(f"{i:3d}" for i in range(1, lines + 1))
        self.line_numbers.config(state="normal")
        self.line_numbers.delete("1.0", "end")
        self.line_numbers.insert("1.0", line_string, "right")
        self.line_numbers.config(state="disabled")

    def run_cpp_analysis(self):
        content = self.text_area.get("1.0", "end-1c")
        if HAS_CYTHON:
            res = analyze_code_fast(content)
            engine = "C++ (Cython)"
        else:
            res = {
                "lines": content.count("\n") + (1 if content else 0),
                "words": len(content.split()),
                "chars": len(content)
            }
            engine = "Python (Fallback)"

        msg = f"Двигун: {engine}\n\nРядків: {res['lines']}\nСлів: {res['words']}\nСимволів: {res['chars']}"
        tk.messagebox.showinfo("Результат аналізу", msg)

    def apply_colors(self):
        bg = palette.get("editor_bg")
        fg = palette.get("editor_fg")
        cursor = palette.get("editor_cursor")
        select_bg = palette.get("editor_select")
        ln_bg = palette.get("line_numbers_bg")
        ln_fg = palette.get("line_numbers_fg")

        self.configure(fg_color=bg)
        self.text_area.config(
            bg=bg, fg=fg,
            insertbackground=cursor,
            selectbackground=select_bg,
            inactiveselectbackground=select_bg
        )
        self.line_numbers.config(bg=ln_bg, fg=ln_fg)