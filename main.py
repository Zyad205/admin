import customtkinter as ctk
from tkinter import TclError
import db
import ui
from settings import *

# Theme manger
ctk.set_default_color_theme("./dark-blue.json")

        
class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(fg_color=VERY_LIGHT_GREEN, *args, **kwargs)

        # Tries the state zoomed because it only works on win
        try:
            self.state("zoomed")
            self.after(100, lambda: self.state("zoomed"))
        except TclError:
            pass

        self.geometry("1000x600")
        
        # Checks for the tables inside the db
        db.check()    
        
        self.ui = ui.Main(self)
        self.mainloop()

   
app = App()
