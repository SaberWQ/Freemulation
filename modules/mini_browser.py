import sys
import json
import subprocess
import threading
import urllib.parse
from tkinter import messagebox
import customtkinter as ctk

from core.config import THEME, FONT_UI

# 1. Автоматичне підключення/встановлення tkinterweb у ВІДПОВІДНЕ Python-середовище
HAS_HTML_RENDERER = False
try:
    from tkinterweb import HtmlFrame
    HAS_HTML_RENDERER = True
except ImportError:
    try:
        # Встановлюємо саме в той інтерпретатор, у якому запущено IDE
        subprocess.check_call([sys.executable, "-m", "pip", "install", "tkinterweb", "pillow"])
        from tkinterweb import HtmlFrame
        HAS_HTML_RENDERER = True
    except Exception as e:
        HAS_HTML_RENDERER = False


class AdvancedBrowserEngine:
    def fetch_url(self, url: str) -> str:
        cmd = ["curl", "-s", "-L", "-A", "FreemulationIDE/1.0", url]
        return subprocess.check_output(cmd, stderr=subprocess.DEVNULL).decode("utf-8", errors="ignore")

    def search(self, query: str, mode: str) -> dict:
        encoded_query = urllib.parse.quote_plus(query)
        if mode == "🐙 GitHub":
            url = f"https://api.github.com/search/repositories?q={encoded_query}&per_page=12"
            return {"type": "github", "data": json.loads(self.fetch_url(url))}
        elif mode == "🐍 PyPI":
            encoded_simple = urllib.parse.quote(query.strip())
            url = f"https://pypi.org/pypi/{encoded_simple}/json"
            return {"type": "pypi", "data": json.loads(self.fetch_url(url))}
        elif mode == "💬 StackOverflow":
            url = f"https://api.stackexchange.com/2.3/search/advanced?order=desc&sort=relevance&q={encoded_query}&site=stackoverflow"
            return {"type": "stackoverflow", "data": json.loads(self.fetch_url(url))}
        return {"type": "web", "url": f"https://html.duckduckgo.com/html/?q={encoded_query}"}


class FreemulationBrowserTab(ctk.CTkFrame):
    """Вкладка браузера для вбудовування в існуюче меню/панель IDE"""
    def __init__(self, master, initial_url: str = None, **kwargs):
        super().__init__(master, fg_color=THEME["bg_editor"], **kwargs)

        self.engine = AdvancedBrowserEngine()
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)

        self._build_navbar()

        status_text = "🖥️ Native HTML Engine Active" if HAS_HTML_RENDERER else "⚠️ Помилка завантаження WebKit"
        self.status_bar = ctk.CTkLabel(self, text=status_text, font=(FONT_UI[0], 11), text_color=THEME["fg_muted"])
        self.status_bar.grid(row=1, column=0, sticky="w", padx=15, pady=(0, 2))

        self.content_area = ctk.CTkFrame(self, fg_color="transparent")
        self.content_area.grid(row=2, column=0, sticky="nsew", padx=10, pady=(0, 10))

        if initial_url:
            self.url_entry.insert(0, initial_url)
            self.exec_search()

    def _build_navbar(self):
        nav = ctk.CTkFrame(self, fg_color=THEME["bg_sidebar"], height=45)
        nav.grid(row=0, column=0, sticky="ew", padx=10, pady=8)
        nav.columnconfigure(2, weight=1)

        self.mode_var = ctk.StringVar(value="🌐 Web")
        modes = ["🌐 Web", "🐙 GitHub", "🐍 PyPI", "💬 StackOverflow"]
        
        self.mode_selector = ctk.CTkOptionMenu(
            nav, values=modes, variable=self.mode_var, width=130,
            fg_color=THEME["fg_accent"], button_color=THEME["fg_accent"]
        )
        self.mode_selector.grid(row=0, column=0, padx=(8, 5), pady=6)

        self.url_entry = ctk.CTkEntry(nav, placeholder_text="Введіть URL або запит...", font=FONT_UI)
        self.url_entry.grid(row=0, column=2, sticky="ew", padx=5, pady=6)
        self.url_entry.bind("<Return>", lambda e: self.exec_search())

        ctk.CTkButton(nav, text="🔍 Перейти", width=100, fg_color=THEME["fg_accent"], command=self.exec_search).grid(row=0, column=3, padx=(5, 8), pady=6)

    def exec_search(self):
        query = self.url_entry.get().strip()
        if not query:
            return

        for w in self.content_area.winfo_children():
            w.destroy()

        mode = self.mode_var.get()

        if query.startswith("http://") or query.startswith("https://") or mode == "🌐 Web":
            target_url = query if query.startswith("http") else f"https://html.duckduckgo.com/html/?q={urllib.parse.quote_plus(query)}"
            
            if HAS_HTML_RENDERER:
                self.status_bar.configure(text=f"⏳ Завантаження: {target_url}...", text_color=THEME["fg_text"])
                html_frame = HtmlFrame(self.content_area, messages_enabled=False)
                html_frame.pack(fill="both", expand=True)
                html_frame.load_website(target_url)
                self.status_bar.configure(text=f"✅ Відображено: {target_url}", text_color="#4CAF50")
            else:
                import webbrowser
                webbrowser.open(target_url)
        else:
            # Отримання даних GitHub / PyPI / StackOverflow картками
            def _worker():
                res = self.engine.search(query, mode)
                self.after(0, lambda: self._render_cards(res))
            threading.Thread(target=_worker, daemon=True).start()

    def _render_cards(self, res):
        scroll = ctk.CTkScrollableFrame(self.content_area, fg_color="transparent")
        scroll.pack(fill="both", expand=True)
        items = res.get("data", {}).get("items", []) or [res.get("data", {}).get("info", {})]
        
        for item in items:
            card = ctk.CTkFrame(scroll, fg_color=THEME["bg_sidebar"])
            card.pack(fill="x", padx=5, pady=5)
            name = item.get("full_name") or item.get("name") or item.get("title", "Результат")
            ctk.CTkLabel(card, text=name, font=(FONT_UI[0], 13, "bold"), text_color=THEME["fg_accent"]).pack(anchor="w", padx=10, pady=5)


# Віконна версія (для виклику з меню)
class FreemulationBrowserWindow(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Freemulation Web Browser")
        self.geometry("950x650")
        browser = FreemulationBrowserTab(self)
        browser.pack(fill="both", expand=True)