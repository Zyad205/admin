import customtkinter as ctk
from tkinter.ttk import Treeview, Style
from settings import *

class CTreeview(Treeview):
    def __init__(
            self,
            master: ctk.CTk,
            name: str,
            columns: tuple,
            browse_mode: str = "browse",
            *args, **kwargs):
        
        """The init func
        Parameters:
        - Master (ctk.CTk): the master of this widget
        - Name (str): any random unique name
        - Columns (tuple[str]): a tuple that contains the name of the columns
        - Browse_mode (str): ---
        """        

        super().__init__(
            master,
            style=f"{name}.Treeview",
            show="headings",
            columns=columns,
            selectmode=browse_mode,
            *args, **kwargs)
        
        self.name = name
        self.columns = columns
        self.create_style()
        for column in columns:
            self.heading(column, text=column)
            self.column(column, stretch=False)


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
        
        """Select the needed attributes to change
        Parameters:
        - Font (str): the font of text inside rows
        - H_font (str): the font of text inside the headers
        - Relief (str): the style of headers
        - Rowheight (int): the height of each row
        - Bg (str): the background color of rows
        - Fg (str): the color of the text inside the rows
        - Sl (str): the selected highlight color 
        - H_bg (str): the background color of the headers
        - H_fg (str): the text color inside the headers
        """
        
        self.style = Style()
        self.style.theme_use("default")
        name = f"{self.name}.Treeview"
        self.style.configure(
            name,
            background=bg,
            foreground=fg,
            fieldbackground=bg,
            borderwidth=0,
            font = font,
            rowheight=rowheight)
        self.style.map(name, background=[("selected", sl)])

        self.style.configure(
            f'{name}.Heading',
            foreground=h_fg,
            background=h_bg,
            font=h_font,
            relief=relief,
            padding=5)
        
    def create_scroll_bar(self, master) -> None:

        """Create scroll bars and the for the scroll bar is needed
        saved as a attribute y_scroll_bar and x_scroll_bar
        Parameters:
        - Master (-): the master of the scroll bars"""
        
        self.y_scroll_bar = ctk.CTkScrollbar(master=master, command=self.yview)
        self.configure(yscrollcommand=self.y_scroll_bar.set)

        self.x_scroll_bar = ctk.CTkScrollbar(master=master, command=self.xview)
        self.configure(xscrollcommand=self.x_scroll_bar.set)


    def column_size(self, sizes: tuple, width: int):
        """Changes the size of the columns by the given ratios
        Parameters:
        - Size (tuple[int]): a tuple that contains the ratio of each column
        - Width (int): the width of this treeview"""

        sizes = sizes[0:len(self.columns)]
    
        one_block = int(width / sum(sizes))

        for index, size in enumerate(sizes):
            column = self.columns[index]
            self.column(
                column=column,
                width=one_block*size,
                stretch=False)
    

class CTopLevel(ctk.CTkToplevel):
    def __init__(self, frame:ctk.CTkFrame = None, title: str="Window", *args, **kwargs):
        """This classed is used as a toplevel that you change the frame inside it only

        Parameters:
        - Frame (ctk.CTkFrame): the starting frame
        - Title (str): the title of this top level"""

        super().__init__(*args, **kwargs)


        self.geometry("400x250")
        self.attributes("-topmost", True)
        self.title(title)
        if frame is not None:
            self.frame = frame
        else:
            self.frame = ctk.CTkFrame(self)

        self.frame.pack(fill="both", expand=True)

    def close(self):
        """Closes the window by withdrawing it and releasing the grab"""
        self.grab_release()
        self.withdraw()

    def change_frame(self, new_frame: ctk.CTkFrame):
        """Changes the drawn frame
        Parameters:
        - New_frame (ctk.CTkFrame): the new frame"""
        
        self.frame.pack_forget()
        self.frame = new_frame
        self.frame.pack(fill="both", expand=True)
