class LanguageManager:
    _instance = None

    TRANSLATIONS = {
        "uk": {
            "file": "Файл", "new_file": "Новий файл", "open_file": "Відкрити файл...",
            "save": "Зберегти", "save_as": "Зберегти як...", "exit": "Вихід",
            "edit": "Редагування", "undo": "Скасувати", "redo": "Повторити",
            "cut": "Вирізати", "copy": "Скопіювати", "paste": "Вставити", "select_all": "Виділити все",
            "tools": "Інструменти", "translator": "Відкрити перекладач...", "translate_sel": "Перекласти виділений текст",
            "run": "Запуск", "analyze": "Аналіз коду (C++ / Cython)",
            "terminal": "Термінал", "clear_terminal": "Очистити термінал",
            "palette": "Палітра й Теми", "presets": "Готові теми (Пресети)", "custom_colors": "Налаштувати кольори вручну...",
            "language": "Мова інтерфейсу",
            "explorer": "ПРОВІДНИК",
            "tab_problems": "ПРОБЛЕМИ", "tab_output": "ВИВІД", "tab_debug": "КОНСОЛЬ НАЛАГОДЖЕННЯ",
            "tab_terminal": "ТЕРМІНАЛ", "tab_ports": "ПОРТИ"
        },
        "en": {
            "file": "File", "new_file": "New File", "open_file": "Open File...",
            "save": "Save", "save_as": "Save As...", "exit": "Exit",
            "edit": "Edit", "undo": "Undo", "redo": "Redo",
            "cut": "Cut", "copy": "Copy", "paste": "Paste", "select_all": "Select All",
            "tools": "Tools", "translator": "Open Translator...", "translate_sel": "Translate Selected Text",
            "run": "Run", "analyze": "Code Analysis (C++ / Cython)",
            "terminal": "Terminal", "clear_terminal": "Clear Terminal",
            "palette": "Palette & Themes", "presets": "Preset Themes", "custom_colors": "Customize Colors...",
            "language": "Interface Language",
            "explorer": "EXPLORER",
            "tab_problems": "PROBLEMS", "tab_output": "OUTPUT", "tab_debug": "DEBUG CONSOLE",
            "tab_terminal": "TERMINAL", "tab_ports": "PORTS"
        },
        "de": {
            "file": "Datei", "new_file": "Neue Datei", "open_file": "Datei öffnen...",
            "save": "Speichern", "save_as": "Speichern unter...", "exit": "Beenden",
            "edit": "Bearbeiten", "undo": "Rückgängig", "redo": "Wiederholen",
            "cut": "Ausschneiden", "copy": "Kopieren", "paste": "Einfügen", "select_all": "Alles auswählen",
            "tools": "Werkzeuge", "translator": "Übersetzer öffnen...", "translate_sel": "Ausgewählten Text übersetzen",
            "run": "Ausführen", "analyze": "Code-Analyse (C++ / Cython)",
            "terminal": "Terminal", "clear_terminal": "Terminal löschen",
            "palette": "Palette & Themen", "presets": "Voreingestellte Themen", "custom_colors": "Farben anpassen...",
            "language": "Sprache",
            "explorer": "EXPLORER",
            "tab_problems": "PROBLEME", "tab_output": "AUSGABE", "tab_debug": "DEBUG-KONSOLE",
            "tab_terminal": "TERMINAL", "tab_ports": "PORTS"
        },
        "es": {
            "file": "Archivo", "new_file": "Nuevo archivo", "open_file": "Abrir archivo...",
            "save": "Guardar", "save_as": "Guardar como...", "exit": "Salir",
            "edit": "Editar", "undo": "Deshacer", "redo": "Rehacer",
            "cut": "Cortar", "copy": "Copiar", "paste": "Pegar", "select_all": "Seleccionar todo",
            "tools": "Herramientas", "translator": "Abrir traductor...", "translate_sel": "Traducir texto seleccionado",
            "run": "Ejecutar", "analyze": "Análisis de código (C++ / Cython)",
            "terminal": "Terminal", "clear_terminal": "Limpiar terminal",
            "palette": "Paleta y Temas", "presets": "Temas preestablecidos", "custom_colors": "Personalizar colores...",
            "language": "Idioma de interfaz",
            "explorer": "EXPLORADOR",
            "tab_problems": "PROBLEMAS", "tab_output": "SALIDA", "tab_debug": "CONSOLA DE DEPURACIÓN",
            "tab_terminal": "TERMINAL", "tab_ports": "PUERTOS"
        },
        "pt": {
            "file": "Arquivo", "new_file": "Novo arquivo", "open_file": "Abrir arquivo...",
            "save": "Salvar", "save_as": "Salvar como...", "exit": "Sair",
            "edit": "Editar", "undo": "Desfazer", "redo": "Refazer",
            "cut": "Recortar", "copy": "Copiar", "paste": "Colar", "select_all": "Selecionar tudo",
            "tools": "Ferramentas", "translator": "Abrir tradutor...", "translate_sel": "Traduzir texto selecionado",
            "run": "Executar", "analyze": "Análise de código (C++ / Cython)",
            "terminal": "Terminal", "clear_terminal": "Limpar terminal",
            "palette": "Paleta e Temas", "presets": "Temas predefinidos", "custom_colors": "Personalizar cores...",
            "language": "Idioma da interface",
            "explorer": "EXPLORADOR",
            "tab_problems": "PROBLEMAS", "tab_output": "SAÍDA", "tab_debug": "CONSOLE DE DEPURAÇÃO",
            "tab_terminal": "TERMINAL", "tab_ports": "PORTAS"
        },
        "ro": {
            "file": "Fișier", "new_file": "Fișier nou", "open_file": "Deschide fișier...",
            "save": "Salvează", "save_as": "Salvează ca...", "exit": "Ieșire",
            "edit": "Editare", "undo": "Anulează", "redo": "Refă",
            "cut": "Taie", "copy": "Copiază", "paste": "Lipește", "select_all": "Selectează tot",
            "tools": "Instrumente", "translator": "Deschide traducător...", "translate_sel": "Tradu textul selectat",
            "run": "Rulare", "analyze": "Analiză cod (C++ / Cython)",
            "terminal": "Terminal", "clear_terminal": "Curăță terminalul",
            "palette": "Paletă și Teme", "presets": "Teme predefinite", "custom_colors": "Personalizează culorile...",
            "language": "Limba interfeței",
            "explorer": "EXPLORATOR",
            "tab_problems": "PROBLEME", "tab_output": "IEȘIRE", "tab_debug": "CONSOLĂ DEBUGARE",
            "tab_terminal": "TERMINAL", "tab_ports": "PORTURI"
        },
        "zh": {
            "file": "文件", "new_file": "新建文件", "open_file": "打开文件...",
            "save": "保存", "save_as": "另存为...", "exit": "退出",
            "edit": "编辑", "undo": "撤销", "redo": "重做",
            "cut": "剪切", "copy": "复制", "paste": "粘贴", "select_all": "全选",
            "tools": "工具", "translator": "打开翻译器...", "translate_sel": "翻译所选文本",
            "run": "运行", "analyze": "代码分析 (C++ / Cython)",
            "terminal": "终端", "clear_terminal": "清空终端",
            "palette": "调色板与主题", "presets": "预设主题", "custom_colors": "自定义颜色...",
            "language": "界面语言",
            "explorer": "资源管理器",
            "tab_problems": "问题", "tab_output": "输出", "tab_debug": "调试控制台",
            "tab_terminal": "终端", "tab_ports": "端口"
        }
    }

    LANG_NAMES = {
        "Українська": "uk",
        "English": "en",
        "Deutsch": "de",
        "Español": "es",
        "Português": "pt",
        "Română": "ro",
        "中文": "zh"
    }

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LanguageManager, cls).__new__(cls)
            cls._instance.current_lang = "uk"
            cls._instance.subscribers = []
        return cls._instance

    def subscribe(self, callback):
        if callback not in self.subscribers:
            self.subscribers.append(callback)

    def set_language(self, lang_code):
        if lang_code in self.TRANSLATIONS:
            self.current_lang = lang_code
            for cb in self.subscribers:
                cb()

    def get(self, key, default=""):
        return self.TRANSLATIONS.get(self.current_lang, {}).get(key, default or key)

lang_mgr = LanguageManager()