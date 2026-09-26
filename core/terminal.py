import tkinter as tk
import customtkinter as ctk
import subprocess
import threading
import queue
import os
from .config import THEME, FONT_CODE, SHELL

class TerminalTab(ctk.CTkFrame):
    def __init__(self, master, close_callback, **kwargs):
        super().__init__(master, fg_color=THEME["bg_panel"], **kwargs)
        self.output_queue = queue.Queue()
        self.process = None
        self.cwd = os.getcwd()
        self.close_callback = close_callback

        # Верхня панелька статусів терміналу (шлях + кнопка закриття)
        self.status_bar = ctk.CTkFrame(self, fg_color=THEME["bg_sidebar"], height=28, corner_radius=0)
        self.status_bar.pack(fill="x")
        
        self.path_lbl = ctk.CTkLabel(self.status_bar, text=f"📁 CWD: {self.cwd}", font=(FONT_CODE[0], 10), text_color=THEME["fg_accent"])
        self.path_lbl.pack(side="left", padx=10)

        # Кнопка закриття самого термінала
        self.close_btn = ctk.CTkButton(
            self.status_bar, text="✕ Закрити термінал", width=110, height=20,
            fg_color="#C42B1C", hover_color="#A82316", text_color="#FFFFFF",
            font=(FONT_CODE[0], 9, "bold"), command=self.terminate_session
        )
        self.close_btn.pack(side="right", padx=5, pady=4)

        self.text_area = tk.Text(
            self, bg=THEME["bg_panel"], fg=THEME["fg_text"],
            insertbackground=THEME["fg_text"], font=FONT_CODE,
            bd=0, highlightthickness=0
        )
        self.text_area.pack(fill="both", expand=True, padx=8, pady=8)
        self.text_area.bind("<Return>", self.on_return)

        self.start_process()
        self.check_queue()

    def start_process(self):
        try:
            self.process = subprocess.Popen(
                [SHELL], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT, text=True, bufsize=1, cwd=self.cwd
            )
            threading.Thread(target=self.read_output, daemon=True).start()
        except Exception as e:
            self.text_area.insert(tk.END, f"Помилка запуску термінала: {e}\n")

    def read_output(self):
        for line in iter(self.process.stdout.readline, ''):
            self.output_queue.put(line)

    def check_queue(self):
        while not self.output_queue.empty():
            line = self.output_queue.get()
            self.text_area.insert(tk.END, line)
            self.text_area.see(tk.END)
        self.after(40, self.check_queue)

    def on_return(self, event):
        lines = self.text_area.get("1.0", tk.END).split("\n")
        command = lines[-2] if len(lines) >= 2 else ""
        for sep in [">", "$", "#", "%"]:
            if sep in command:
                command = command.split(sep, 1)[-1].strip()
                break
        
        if command.startswith("cd "):
            potential_path = command[3:].strip()
            new_path = os.path.abspath(os.path.join(self.cwd, potential_path))
            if os.path.isdir(new_path):
                self.cwd = new_path
                self.path_lbl.configure(text=f"📁 CWD: {self.cwd}")

        if self.process and self.process.poll() is None and command:
            self.process.stdin.write(command + "\n")
            self.process.stdin.flush()
        return "break"

    def terminate_session(self):
        if self.process:
            try:
                self.process.terminate()
                self.process.kill()
            except Exception:
                pass
        if self.close_callback:
            self.close_callback(self)
            
class AdvancedTerminalTab(ctk.CTkFrame):
    def __init__(self, master, cwd=None, **kwargs):
        super().__init__(master, fg_color=THEME["bg_panel"], **kwargs)
        self.cwd = cwd or os.expanduser("~")

        self.status_bar = ctk.CTkFrame(self, fg_color=THEME["bg_sidebar"], height=28)
        self.status_bar.pack(fill="x")

        self.branch_label = ctk.CTkLabel(self.status_bar, text="🌿 git: main", font=(FONT_CODE[0], 11), text_color="#4EC9B0")
        self.branch_label.pack(side="left", padx=10)

        self.status_label = ctk.CTkLabel(self.status_bar, text="🟢 Ready", font=(FONT_CODE[0], 11), text_color="#6A9955")
        self.status_label.pack(side="right", padx=10)

        self.text_area = tk.Text(self, bg=THEME["bg_panel"], fg=THEME["fg_text"], font=FONT_CODE, bd=0)
        self.text_area.pack(fill="both", expand=True, padx=5, pady=5)

        self.update_git_branch()

    def update_git_branch(self):
        try:
            res = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=self.cwd, stderr=subprocess.DEVNULL)
            branch = res.decode().strip()
            self.branch_label.configure(text=f"🌿 git: {branch}")
        except Exception:
            self.branch_label.configure(text="🌿 git: none")