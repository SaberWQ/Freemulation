import customtkinter as ctk
from core.menus import MenuManager
from modules.layout import MainLayout

class FreemulationIDE(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Freemulation IDE")
        self.geometry("1080x720")

        self.layout = MainLayout(self)
        self.menu_manager = MenuManager(self, layout_ref=self.layout)

if __name__ == "__main__":
    app = FreemulationIDE()
    app.mainloop()