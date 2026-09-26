import sys
import customtkinter as ctk

ctk.set_appearance_mode("Dark")

DEFAULT_THEME = {
    "bg_activity": "#2C2C2C",
    "bg_sidebar": "#252526",
    "bg_editor": "#1E1E1E",
    "bg_panel": "#181818",
    "bg_tab_active": "#1E1E1E",
    "bg_tab_inactive": "#2D2D30",
    "fg_text": "#CCCCCC",
    "fg_accent": "#007ACC",
    "fg_muted": "#858585",
    "border": "#3F3F46",
    "hover": "#37373D"
}

# Робоча мутабельна тема для оновлення в реальному часі
THEME = DEFAULT_THEME.copy()

if sys.platform == "darwin":
    FONT_CODE = ("Menlo", 13)
    FONT_UI = ("SF Pro Text", 12)
    SHELL = "/bin/zsh"
elif sys.platform == "win32":
    FONT_CODE = ("Cascadia Code", 11)
    FONT_UI = ("Segoe UI Variable", 11)
    SHELL = "cmd.exe"
else:
    FONT_CODE = ("JetBrains Mono", 11)
    FONT_UI = ("Ubuntu", 11)
    SHELL = "/bin/bash"