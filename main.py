import customtkinter as ctk
import db
import ui
from settings import *
ctk.set_default_color_theme("./dark-blue.json")

        
class App(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color=VERY_LIGHT_GREEN)
        self.after(100, lambda: self.state("zoomed"))
        db.check()    
        
        self.ui = ui.Main(self)
        self.mainloop()

   
app = App()
