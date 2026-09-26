import json
import ssl
import threading
import urllib.parse
import urllib.request
import tkinter as tk
import customtkinter as ctk
from modules.language_manager import lang_mgr

LANGUAGES = {
    "Українська": "uk",
    "English": "en",
    "Deutsch (Німецька)": "de",
    "Español (Іспанська)": "es",
    "Português (Португальська)": "pt",
    "Română (Румунська)": "ro",
    "中文 (Китайська)": "zh-CN"
}

def translate_api(text: str, src_code: str, tgt_code: str) -> str:
    """Виконує переклад з автоматичним перемиканням на резервний сервер при 429"""
    if not text.strip():
        return ""

    ctx = ssl._create_unverified_context()
    
    # Спроба 1: Google Translate
    try:
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&dt=t&sl={src_code}&tl={tgt_code}&q={urllib.parse.quote(text)}"
        req = urllib.request.Request(
            url, 
            headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}
        )
        with urllib.request.urlopen(req, timeout=4, context=ctx) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            return "".join([part[0] for part in data[0] if part[0]])
    except Exception:
        pass

    # Спроба 2: Резервний API (MyMemory) у випадку заблокованого Google
    try:
        langpair = f"{src_code}|{tgt_code}"
        url = f"https://api.mymemory.translated.net/get?q={urllib.parse.quote(text)}&langpair={langpair}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5, context=ctx) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            if "responseData" in data and "translatedText" in data["responseData"]:
                return data["responseData"]["translatedText"]
    except Exception as e:
        return f"[Помилка сервісу перекладу: {e}]"

    return "[Сервіси перекладу тимчасово недоступні, спробуйте пізніше]"


class TranslatorWindow(ctk.CTkToplevel):
    def __init__(self, parent, initial_text="", on_insert_callback=None):
        super().__init__(parent)
        self.title("Центр Перекладу та Локалізації")
        self.geometry("660x520")
        self.on_insert_callback = on_insert_callback
        self.attributes("-topmost", True)

        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)

        self.tab_code = self.tabview.add("Переклад коду / тексту")
        self.tab_app = self.tabview.add("Мова всієї програми (UI)")

        self._build_code_translator_tab(initial_text)
        self._build_app_language_tab()

    def _build_code_translator_tab(self, initial_text):
        lang_names = list(LANGUAGES.keys())

        frame_top = ctk.CTkFrame(self.tab_code)
        frame_top.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(frame_top, text="З мови:").pack(side="left", padx=5)
        self.src_combo = ctk.CTkComboBox(frame_top, values=lang_names)
        self.src_combo.set("Українська")
        self.src_combo.pack(side="left", padx=5)

        ctk.CTkLabel(frame_top, text="На мову:").pack(side="left", padx=5)
        self.tgt_combo = ctk.CTkComboBox(frame_top, values=lang_names)
        self.tgt_combo.set("English")
        self.tgt_combo.pack(side="left", padx=5)

        self.txt_source = ctk.CTkTextbox(self.tab_code, height=120)
        self.txt_source.pack(fill="both", expand=True, padx=10, pady=5)
        if initial_text:
            self.txt_source.insert("1.0", initial_text)

        self.btn_translate = ctk.CTkButton(self.tab_code, text="Перекласти текст", command=self.start_translation)
        self.btn_translate.pack(pady=5)

        self.txt_target = ctk.CTkTextbox(self.tab_code, height=120)
        self.txt_target.pack(fill="both", expand=True, padx=10, pady=5)

        frame_bottom = ctk.CTkFrame(self.tab_code)
        frame_bottom.pack(fill="x", padx=10, pady=10)

        if self.on_insert_callback:
            self.btn_insert = ctk.CTkButton(
                frame_bottom, text="Замінити виділений текст у редакторі",
                fg_color="#2b8a3e", hover_color="#237032",
                command=self._insert_to_editor
            )
            self.btn_insert.pack(side="right", padx=5)

    def _build_app_language_tab(self):
        lbl = ctk.CTkLabel(
            self.tab_app, 
            text="Оберіть мову для перекладу інтерфейсу всієї програми:",
            font=("Arial", 13, "bold")
        )
        lbl.pack(anchor="w", padx=20, pady=(15, 10))

        frame_langs = ctk.CTkFrame(self.tab_app)
        frame_langs.pack(fill="both", expand=True, padx=20, pady=10)

        for name, code in lang_mgr.LANG_NAMES.items():
            btn = ctk.CTkButton(
                frame_langs,
                text=f"Перекласти програму на: {name}",
                font=("Arial", 12),
                height=32,
                command=lambda c=code: self._change_app_language(c)
            )
            btn.pack(fill="x", padx=15, pady=4)

    def start_translation(self):
        text = self.txt_source.get("1.0", "end-1c")
        src_lang = LANGUAGES.get(self.src_combo.get(), "uk")
        tgt_lang = LANGUAGES.get(self.tgt_combo.get(), "en")

        self.btn_translate.configure(state="disabled", text="Перекладаю...")

        def _worker():
            res = translate_api(text, src_lang, tgt_lang)
            self.after(0, lambda: self._finish_translation(res))

        threading.Thread(target=_worker, daemon=True).start()

    def _finish_translation(self, result_text):
        self.txt_target.delete("1.0", "end")
        self.txt_target.insert("1.0", result_text)
        self.btn_translate.configure(state="normal", text="Перекласти текст")

    def _insert_to_editor(self):
        result = self.txt_target.get("1.0", "end-1c")
        if result and self.on_insert_callback:
            self.on_insert_callback(result)
            self.destroy()

    def _change_app_language(self, lang_code):
        lang_mgr.set_language(lang_code)