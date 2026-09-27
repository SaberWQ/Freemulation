import os
import subprocess
import threading
import customtkinter as ctk
from core.config import THEME, FONT_CODE, FONT_UI


class CodeRunnerPanel(ctk.CTkFrame):
    """Нижня панель консолі запуску коду"""
    def __init__(self, master, **kwargs):
        super().__init__(master, height=200, fg_color=THEME["bg_sidebar"], **kwargs)

        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        # Панель управління
        top = ctk.CTkFrame(self, fg_color="transparent")
        top.grid(row=0, column=0, sticky="ew", padx=8, pady=4)

        ctk.CTkLabel(top, text="КОНСОЛЬ ВИВОДУ", font=(FONT_UI[0], 11, "bold"), text_color=THEME["fg_muted"]).pack(side="left")
        ctk.CTkButton(top, text="🧹 Очистити", width=70, height=22, fg_color="transparent", border_width=1, command=self.clear).pack(side="right")

        # Текстова консоль
        self.console = ctk.CTkTextbox(self, font=FONT_CODE, fg_color=THEME["bg_editor"], text_color="#E0E0E0")
        self.console.grid(row=1, column=0, sticky="nsew", padx=5, pady=(0, 5))

    def write(self, text: str):
        self.console.insert("end", text)
        self.console.see("end")

    def clear(self):
        self.console.delete("1.0", "end")

    def run_file(self, file_path: str):
        if not file_path or not os.path.exists(file_path):
            self.write("❌ Помилка: Файл не збережено або він відсутній на диску.\n")
            return

        self.clear()
        self.write(f"🚀 Запуск {file_path}...\n" + "─"*50 + "\n")

        def _worker():
            ext = os.path.splitext(file_path)[1].lower()
            if ext == ".py":
                cmd = ["python3", "-u", file_path]
            elif ext in [".cpp", ".c"]:
                out_bin = file_path + ".bin"
                cmd = f"g++ '{file_path}' -o '{out_bin}' && '{out_bin}'"
            else:
                self.after(0, lambda: self.write(f"⚠️ Непідтримуваний тип файлу: {ext}\n"))
                return

            try:
                process = subprocess.Popen(
                    cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    text=True, shell=isinstance(cmd, str)
                )
                
                for line in process.stdout:
                    self.after(0, self.write, line)
                for line in process.stderr:
                    self.after(0, self.write, f"❌ {line}")

                process.wait()
                self.after(0, lambda: self.write(f"\n" + "─"*50 + f"\n✅ Процес завершено з кодом {process.returncode}\n"))
            except Exception as e:
                self.after(0, lambda: self.write(f"\n❌ Помилка виконання: {e}\n"))

        threading.Thread(target=_worker, daemon=True).start()