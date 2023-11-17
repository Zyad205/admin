import db
import customtkinter as ctk
from tkinter.messagebox import *
from widgets import CTreeview, CTopLevel
from settings import *
from datetime import date
from sqlite3 import IntegrityError

def is_leap_year(year):
    """Determine whether a year is a leap year."""

    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


class Main:
    def __init__(self, app: ctk.CTk):

        # Top_levels

        self.top_level = CTopLevel(master=app)
        self.top_level.withdraw()
        self.top_level.wm_protocol("WM_DELETE_WINDOW", self.top_level.close)

        self.add_frame = AddFrame(master=self.top_level, add_to_treeview_fun=self.add)

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


    def add(self, name: str, latest_sub: str, next_sub: str):
        self.main_treeview.insert(parent="", index="end", iid=name, values=(name, latest_sub, next_sub))

class AddFrame(ctk.CTkFrame):
    def __init__(self, master, add_to_treeview_fun, *args, **kwargs):
        super().__init__(master=master, *args, **kwargs)

        self.add_to_treeview_func = add_to_treeview_fun

        # Row configuration
        self.columnconfigure(tuple(range(4)), uniform="a", weight=1)        
        self.rowconfigure(tuple(range(9)), uniform="a", weight=1)        

        self.name_label = ctk.CTkLabel(self, text="Name", font=MEDIUM_FONT)
        self.name_entry = ctk.CTkEntry(self, font=SMALL_FONT)

        self.today = date.today()
        if self.today.month == 2 and self.today.day == 29:
            self.today.replace(day=28)

        # Values for comboboxes
        self.years = [str(year) for year in range(self.today.year, self.today.year + 10)]
        self.month = [str(month) for month in range(1, 13)]
        self.days = [str(day) for day in range(1, 32)]

        # Vars for the comboboxes
        self.year_var = ctk.StringVar(value=str(self.today.year))
        self.month_var = ctk.StringVar(value=str(self.today.month))
        self.day_var = ctk.StringVar(value=str(self.today.day))

        # ----- #
        # Labels

        label = ctk.CTkLabel(self, text="Next subscription:", font=MEDIUM_FONT)
        year_label = ctk.CTkLabel(self, text="Year:", font=SMALL_FONT)
        month_label = ctk.CTkLabel(self, text="Month:", font=SMALL_FONT)
        day_label = ctk.CTkLabel(self, text="Day:", font=SMALL_FONT)

        # ----- #
        # Comboboxes

        self.year_widget = ctk.CTkComboBox(
            self,
            values=self.years,
            variable=self.year_var,
            command=self.change_days,
            state="readonly")

        self.month_widget = ctk.CTkComboBox(
            self,
            values=self.month,
            variable=self.month_var,
            command=self.change_days,
            state="readonly")

        self.day_widget = ctk.CTkComboBox(
            self,
            values=self.days,
            variable=self.day_var,
            state="readonly")

        # ----- #
        # Add button

        add_btn = ctk.CTkButton(
            self,
            text="Add",
            fg_color=LIGHT_LIME,
            hover_color=HIGHLIGHTED_LIGHT_LIME,
            command=self.add,
            text_color=GREY)
        
        # ----- #
        # Placing widgets

        self.name_label.grid(column=0, row=0, columnspan=4, sticky="w", padx=5)
        self.name_entry.grid(column=0, row=1, columnspan=2, sticky="we", padx=5)

        label.grid(column=1, columnspan=2, row=3, sticky="n")

        year_label.grid(column=0, row=4, sticky="w")
        self.year_widget.grid(column=0, row=5, columnspan=2, sticky="w", padx=5)

        month_label.grid(column=2, row=4, sticky="w")
        self.month_widget.grid(column=2, row=5, stick="w", padx=5)

        day_label.grid(column=0, row=6, sticky="w")
        self.day_widget.grid(column=0, row=7, sticky="w", padx=5)

        add_btn.grid(column=3, row=8, padx=3, pady=2)

        # ----- #
        # Increment the next sub by one month

        if self.today.month == 12:
            next_date = self.today.replace(year=self.today.year + 1, month=1)

        elif self.today.month == 1 and self.today.day == 31: # Because feb doesn't have enough days 
            next_date = self.today.replace(month=3, day=int(not is_leap_year(self.today.year)) + 1)


        else:
            remaining_days = 30

            num_of_days = self.get_days_for_month(0, self.today.month)

            remaining_days -= num_of_days - self.today.day

            next_date = self.today.replace(month=self.today.month + 1, day=remaining_days)

        self.year_var.set(str(next_date.year))
        self.month_var.set(str(next_date.month))
        self.day_var.set(str(next_date.day))

        # Change the value for the days combobox according to the month
        self.change_days("")
    

    def change_days(self, _) -> None:
        """Change the value for the days combobox according to the month"""
        
        year = int(self.year_var.get())
        month = int(self.month_var.get())


        days = self.days[0:self.get_days_for_month(year, month)]

        self.day_widget.configure(values=days)
        if int(self.day_var.get()) > int(days[-1]):
            self.day_var.set(days[-1])


    def get_days_for_month(self, year, month):
        """Get a the last day number in a month"""
        
        if month == 2: # For Feb
            max_day = 28  + int(is_leap_year(year))
        elif month % 2: # Odd months 
            max_day = 31
        else:           # Even months
            max_day = 30

        return max_day

    def add(self):
        name = self.name_entry.get()

        if name != "":
            name = name.strip()

            year = self.year_var.get()
            month = self.month_var.get()
            day = self.day_var.get()
            try:
                db.add(name, str(self.today), f"{year}-{month}-{day}")
            except IntegrityError:
                showerror("Can't add", "Name is already registered")
                return

        else:
            showerror("Invalid name", "Please insert a name")
            return
        
        showinfo("Added successfully", "Member added successfully")
        self.name_entry.delete("0", "end")
        self.add_to_treeview_func(name, str(self.today), f"{year}-{month}-{day}")
        


