import customtkinter as ctk
from db import *
import ui

        
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.after(100, lambda: self.state("zoomed"))

        self.ui = ui.Main(self)
        
        self.mainloop()


app = App()
