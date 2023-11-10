import customtkinter as ctk
from tkinter.ttk import Treeview, Style
from settings import *

class CTreeview(Treeview):
    def __init__(
            self,
            master,
            name: str,
            columns: tuple,
            browse_mode: str = "browse"):
        
        super().__init__(
            master,
            style=f"{name}.Treeview",
            show="headings",
            columns=columns,
            selectmode="browse")
        
        self.name = name
        self.create_style()
        for column in columns:
            self.heading(column, text=column)


    def create_style(
            self,
            font: str =SMALL_FONT,
            h_font: str =MEDIUM_FONT,
            relief: str ="flat",
            rowheight: int =25,
            bg: str =LIGHT_GREY,
            fg: str =OFF_WHITE,
            sl: str =HIGHLIGHTED_BLUE,
            h_bg: str =BLUEISH_GREY,
            h_fg: str =OFF_WHITE) -> None:
        
        """Select the needed attribute to change"""
        
        style = Style()
        style.theme_use("default")
        name = f"{self.name}.Treeview"
        style.configure(
            name,
            background=bg,
            foreground=fg,
            fieldbackground=bg,
            borderwidth=0,
            font = font,
            rowheight=rowheight)
        style.map(name, background=[("selected", sl)])

        style.configure(
            f'{name}.Heading',
            foreground=h_fg,
            background=h_bg,
            font=h_font,
            relief=relief,
            padding=5)

