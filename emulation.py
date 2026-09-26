import tkinter as tk

class MenuManager:
    """Клас для керування всім верхнім меню програми"""
    def __init__(self, root):
        self.root = root
        self.menubar = tk.Menu(self.root)
        
        self._create_file_menu()
        self._create_edit_menu()
        self._create_view_menu()
        self._create_run_menu()
        self._create_terminal_menu()
        
        # Застосування меню до головного вікна
        self.root.config(menu=self.menubar)

    def _create_file_menu(self):
        file_menu = tk.Menu(self.menubar, tearoff=0)
        file_menu.add_command(label="New Text File", accelerator="Cmd+N")
        file_menu.add_command(label="New Window", accelerator="Shift+Cmd+N")
        file_menu.add_separator()
        file_menu.add_command(label="Open...", accelerator="Cmd+O")
        file_menu.add_command(label="Open Folder...")
        file_menu.add_separator()
        file_menu.add_command(label="Save", accelerator="Cmd+S")
        file_menu.add_command(label="Save As...", accelerator="Shift+Cmd+S")
        file_menu.add_command(label="Auto Save")
        file_menu.add_separator()
        file_menu.add_command(label="Close Editor", accelerator="Cmd+W")
        file_menu.add_command(label="Close Window", accelerator="Shift+Cmd+W", command=self.root.destroy)
        self.menubar.add_cascade(label="File", menu=file_menu)

    def _create_edit_menu(self):
        edit_menu = tk.Menu(self.menubar, tearoff=0)
        edit_menu.add_command(label="Undo", accelerator="Cmd+Z")
        edit_menu.add_command(label="Redo", accelerator="Shift+Cmd+Z")
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", accelerator="Cmd+X")
        edit_menu.add_command(label="Copy", accelerator="Cmd+C")
        edit_menu.add_command(label="Paste", accelerator="Cmd+V")
        edit_menu.add_separator()
        edit_menu.add_command(label="Find", accelerator="Cmd+F")
        edit_menu.add_command(label="Replace", accelerator="Alt+Cmd+F")
        edit_menu.add_separator()
        edit_menu.add_command(label="Toggle Line Comment", accelerator="Cmd+/")
        self.menubar.add_cascade(label="Edit", menu=edit_menu)

    def _create_view_menu(self):
        view_menu = tk.Menu(self.menubar, tearoff=0)
        view_menu.add_command(label="Command Palette...", accelerator="Shift+Cmd+P")
        view_menu.add_separator()
        view_menu.add_command(label="Explorer", accelerator="Shift+Cmd+E")
        view_menu.add_command(label="Search", accelerator="Shift+Cmd+F")
        view_menu.add_separator()
        view_menu.add_command(label="Problems", accelerator="Shift+Cmd+M")
        view_menu.add_command(label="Output", accelerator="Shift+Cmd+U")
        view_menu.add_command(label="Debug Console", accelerator="Shift+Cmd+Y")
        view_menu.add_command(label="Terminal", accelerator="Ctrl+`")
        self.menubar.add_cascade(label="View", menu=view_menu)

    def _create_run_menu(self):
        run_menu = tk.Menu(self.menubar, tearoff=0)
        run_menu.add_command(label="Start Debugging", accelerator="F5")
        run_menu.add_command(label="Run Without Debugging", accelerator="Ctrl+F5")
        run_menu.add_separator()
        run_menu.add_command(label="Toggle Breakpoint", accelerator="F9")
        self.menubar.add_cascade(label="Run", menu=run_menu)

    def _create_terminal_menu(self):
        terminal_menu = tk.Menu(self.menubar, tearoff=0)
        terminal_menu.add_command(label="New Terminal")
        terminal_menu.add_command(label="Split Terminal", accelerator="Cmd+\\")
        terminal_menu.add_separator()
        terminal_menu.add_command(label="Run Active File")
        terminal_menu.add_command(label="Run Selected Text")
        self.menubar.add_cascade(label="Terminal", menu=terminal_menu)