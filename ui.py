from db import add
import customtkinter as ctk
from widgets import CTreeview

class Main:
    def __init__(self, app):
        self.app = app
        logo = ctk.CTkLabel(app, text="logo")
        delete_btn = ctk.CTkButton(
            app,
            text="delete member",
            fg_color="#990000",
            hover="#660000")
        add_member_entry = ctk.CTkEntry(app)
        added_to_council = ctk.CTkButton(
            app,
            text="add member",
            fg_color="#009900",
            hover="#006600")
        
        tr = CTreeview(app, "jUnKy sEtuPs", ("NAme", "Nma"), ())
        tr.create_style()
        tr.pack()
        