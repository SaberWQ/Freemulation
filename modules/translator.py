import os
import tkinter as tk
from tkinter import ttk
from core.config import THEME


class FileExplorerPanel(tk.Frame):
    def __init__(self, parent, on_file_select=None, **kwargs):
        super().__init__(parent, bg=THEME["sidebar_bg"], **kwargs)
        self.on_file_select = on_file_select

        self.tree = ttk.Treeview(self, show="tree")
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<Double-1>", self._on_double_click)

    def load_directory(self, path):
        self.tree.delete(*self.tree.get_children())
        root_node = self.tree.insert(
            "",
            "end",
            text=os.path.basename(path) or path,
            open=True,
            values=[path],
        )
        self._process_directory(root_node, path)

    def _process_directory(self, parent_node, path):
        try:
            for item in sorted(os.listdir(path)):
                if item.startswith("."):
                    continue
                full_path = os.path.join(path, item)
                is_dir = os.path.isdir(full_path)
                node = self.tree.insert(
                    parent_node,
                    "end",
                    text=item,
                    open=False,
                    values=[full_path],
                )
                if is_dir:
                    self._process_directory(node, full_path)
        except PermissionError:
            pass

    def _on_double_click(self, event):
        item_id = self.tree.selection()
        if not item_id:
            return
        values = self.tree.item(item_id[0], "values")
        if values and os.path.isfile(values[0]):
            if self.on_file_select:
                self.on_file_select(values[0])