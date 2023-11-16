import db
import customtkinter as ctk
from widgets import CTreeview, CTopLevel
from settings import *
from datetime import date



class Main:
    def __init__(self, app: ctk.CTk):

        # Top_levels

        self.top_level = CTopLevel(master=app)
        self.top_level.withdraw()
        self.top_level.wm_protocol("WM_DELETE_WINDOW", self.top_level.close)

        self.add_frame = AddFrame(self.top_level)

        self.app = app
        self.create_main_treeview()

        self.add_btn = ctk.CTkButton(
            app,
            text="Add",
            command=self.open_add,
            fg_color=ORANGE,
            hover_color=HIGHLIGHTED_ORANGE,
            font=SMALL_FONT)



        self.main_treeview.place(x=0, rely=0.02, relwidth=0.35, relheight=0.35)
        self.main_treeview.y_scroll_bar.place(relx=0.35, rely=0.02, relheight=0.35, anchor="nw")
        self.add_btn.place(relx=0.01, rely=0.4, relwidth=0.07, relheight=0.05)


    def create_main_treeview(self):
        self.main_treeview = CTreeview(self.app, "main", columns=("Name", "Latest subscription", "Next subscription"))
        self.main_treeview.create_style()
        self.main_treeview.column_size((2, 2, 2), width= 35 * self.app.winfo_screenwidth() / 100)
        self.main_treeview.create_scroll_bar(self.app)

        self.fetch()
        

    def open_add(self):
        self.top_level.deiconify()

        self.top_level.change_frame(self.add_frame)



    def fetch(self):
        names = db.fetch()

        for name, latest_sub, next_sub in names:
            self.main_treeview.insert(parent="", index="end", iid=name, values=(name, latest_sub, next_sub))


    def add(self):
        name = self.entry.get().strip()
        latest_sub = date.today()
        next_sub = date.today()
        
        db.add(name=name, last_sub=latest_sub, next_sub=next_sub)
        self.main_treeview.insert(parent="", index="end", iid=name, values=(name, latest_sub, next_sub))

class AddFrame(ctk.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master=master, *args, **kwargs)

        # Row configuration
        self.columnconfigure(tuple(range(4)), uniform="a", weight=1)        
        self.rowconfigure(tuple(range(10)), uniform="a", weight=1)        

        self.name_label = ctk.CTkLabel(self, text="Name", font=MEDIUM_FONT)
        self.name_entry = ctk.CTkEntry(self, font=SMALL_FONT)

        self.today = date.today()
        if self.today.month == 2 and self.today.day == 29:
            self.today.replace(day=28)



        self.years = [str(year) for year in range(self.today.year, self.today.year + 10)]
        self.month = [str(month) for month in range(1, 13)]
        self.days = [str(day) for day in range(1, 32)]

        self.year_var = ctk.StringVar(value=str(self.today.year))
        self.year_widget = ctk.CTkComboBox(self, values=self.years, variable=self.year_var)

        self.month_var = ctk.StringVar(value=str(self.today.month))
        self.month_widget = ctk.CTkComboBox(
            self,
            values=self.month,
            variable=self.month_var,
            command=self.change_days)

        self.day_var = ctk.StringVar(value=str(self.today.day))
        self.day_widget = ctk.CTkComboBox(self, values=self.days, variable=self.day_var)


        self.name_label.grid(column=0, row=0, columnspan=4, sticky="w", padx=5)
        self.name_entry.grid(column=0, row=1, columnspan=4, sticky="w", padx=5)
        self.year_widget.grid(column=0, row=3, columnspan=2, sticky="w", padx=5)
        self.month_widget.grid(column=3, row=3, stick="e", padx=5)
        self.day_widget.grid(column=0, row=5, sticky="w", padx=5)

    def change_days(self, _):
        month = int(self.month_var.get())

        if month == 2:
            days = self.days[0:28]
        elif month % 2:
            days = self.days[0:31]
        else:
            days = self.days[0:30]

            
        
        self.day_widget.configure(values=days)

        


