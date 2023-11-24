import db
import customtkinter as ctk
from tkinter.messagebox import *
from widgets import CTreeview, CTopLevel
from settings import *
from toplevel_frames import *


class Main:
    def __init__(self, app: ctk.CTk):

        # Top_levels

        self.top_level = CTopLevel(master=app)
        self.top_level.withdraw()
        self.top_level.wm_protocol("WM_DELETE_WINDOW", self.top_level.close)

        self.add_frame = AddFrame(master=self.top_level, add_to_treeview_fun=self.add)
        self.renew_frame = RenewFrame(master=self.top_level, alter_treeview_func=self.alter)

        self.app = app
        self.create_main_treeview()

        self.add_btn = ctk.CTkButton(
            app,
            text="Add",
            command=self.open_add,
            fg_color=ORANGE,
            hover_color=HIGHLIGHTED_ORANGE,
            font=SMALL_FONT)
        
        self.renew_btn = ctk.CTkButton(
            app,
            text="Renew",
            command=self.open_renew,
            fg_color=ORANGE,
            hover_color=HIGHLIGHTED_ORANGE,
            font=SMALL_FONT)



        self.main_treeview.place(x=0, rely=0.02, relwidth=0.35, relheight=0.35)
        self.main_treeview.y_scroll_bar.place(relx=0.35, rely=0.02, relheight=0.35, anchor="nw")
        self.add_btn.place(relx=0.01, rely=0.4, relwidth=0.07, relheight=0.05)
        self.renew_btn.place(relx=0.01, rely=0.5, relwidth=0.07, relheight=0.05)

    def create_main_treeview(self):
        self.main_treeview = CTreeview(self.app, "main", columns=("Name", "Latest subscription", "Next subscription"))
        self.main_treeview.create_style()
        self.main_treeview.column_size((2, 2, 2), width= 35 * self.app.winfo_screenwidth() / 100)
        self.main_treeview.create_scroll_bar(self.app)

        self.fetch()
        

    def open_add(self):
        self.top_level.deiconify()

        self.top_level.change_frame(self.add_frame)
        self.add_frame.increment_month()

    def open_renew(self):
        name = self.main_treeview.selection()

        if len(name) == 1:
            name = name[0]
            self.top_level.deiconify()

            self.top_level.change_frame(self.renew_frame)
             
            next_sub = self.main_treeview.item(name)["values"][2] 
            self.renew_frame.get_name(name, next_sub)

        else:
            showerror(title="Invalid selection", message="Please select a member")




    def fetch(self):
        data = db.fetch()

        for name, last_sub, next_sub in data:
            self.add(name=name, latest_sub=last_sub, next_sub=next_sub)

    def add(self, name: str, latest_sub: str, next_sub: str):
        self.main_treeview.insert(parent="", index="0", iid=name, values=(name, latest_sub, next_sub))

    def alter(self, name: str, latest_sub: str, next_sub: str):
        self.main_treeview.item(name, values=(name, latest_sub, next_sub))
    