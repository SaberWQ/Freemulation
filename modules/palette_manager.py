class PaletteManager:
    _instance = None

    PRESETS = {
        "VS Code Dark": {
            "bg_main": "#1e1e1e",
            "bg_sidebar": "#252526",
            "bg_panel": "#1e1e1e",
            "fg_text": "#d4d4d4",
            "fg_muted": "#858585",
            "editor_bg": "#1e1e1e",
            "editor_fg": "#d4d4d4",
            "editor_cursor": "#aeafad",
            "editor_select": "#264f78",
            "line_numbers_bg": "#1e1e1e",
            "line_numbers_fg": "#858585"
        },
        "Light": {
            "bg_main": "#f3f3f3",
            "bg_sidebar": "#e8e8e8",
            "bg_panel": "#ffffff",
            "fg_text": "#000000",
            "fg_muted": "#616161",
            "editor_bg": "#ffffff",
            "editor_fg": "#000000",
            "editor_cursor": "#000000",
            "editor_select": "#add6ff",
            "line_numbers_bg": "#f3f3f3",
            "line_numbers_fg": "#237893"
        },
        "Hacker Matrix": {
            "bg_main": "#0d0d0d",
            "bg_sidebar": "#050505",
            "bg_panel": "#0a0a0a",
            "fg_text": "#00ff41",
            "fg_muted": "#008f11",
            "editor_bg": "#000000",
            "editor_fg": "#00ff41",
            "editor_cursor": "#00ff41",
            "editor_select": "#003b00",
            "line_numbers_bg": "#050505",
            "line_numbers_fg": "#008f11"
        },
        "Dracula": {
            "bg_main": "#282a36",
            "bg_sidebar": "#21222c",
            "bg_panel": "#282a36",
            "fg_text": "#f8f8f2",
            "fg_muted": "#6272a4",
            "editor_bg": "#282a36",
            "editor_fg": "#f8f8f2",
            "editor_cursor": "#f8f8f2",
            "editor_select": "#44475a",
            "line_numbers_bg": "#21222c",
            "line_numbers_fg": "#6272a4"
        }
    }

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PaletteManager, cls).__new__(cls)
            cls._instance.colors = dict(cls.PRESETS["VS Code Dark"])
            cls._instance.subscribers = []
        return cls._instance

    def subscribe(self, callback):
        self.subscribers.append(callback)

    def set_preset(self, preset_name):
        if preset_name in self.PRESETS:
            self.colors.update(self.PRESETS[preset_name])
            self.notify()

    def set_color(self, key, value):
        if value:
            self.colors[key] = value
            self.notify()

    def notify(self):
        for callback in self.subscribers:
            callback()

    def get(self, key, default="#ffffff"):
        return self.colors.get(key, default)

palette = PaletteManager()