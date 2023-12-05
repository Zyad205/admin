import db
from settings import *
from datetime import date, datetime
import customtkinter as ctk
from tkinter.messagebox import *
from sqlite3 import IntegrityError

# ----- #
# Functions
def is_leap_year(year):
    """Determine whether a year is a leap year."""
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

def get_max_day_for_month(year: int, month: int) -> int:
        """Get a the last day number in a month"""
        
        if month == 2: # For Feb
            max_day = 28  + int(is_leap_year(year))
        elif month % 2: # Odd months 
            max_day = 31
        else:           # Even months
            max_day = 30

        return max_day




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
        date_label = ctk.CTkLabel(self, text=f"Date: {str(self.today)}", font=SMALL_FONT)

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
            text_color=GREY,
            corner_radius=5)
        
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

        date_label.grid(column=3, row=0, sticky="w", pady=2)
        # ----- #
        # Increment the next sub by one month

        self.increment_month()

        # Change the value for the days combobox according to the month
        self.change_days("")
    

    def change_days(self, _) -> None:
        """Change the value for the days combobox according to the month"""
        
        year = int(self.year_var.get())
        month = int(self.month_var.get())


        days = self.days[0:get_max_day_for_month(year, month)]

        self.day_widget.configure(values=days)
        if int(self.day_var.get()) > int(days[-1]):
            self.day_var.set(days[-1])

    def increment_month(self):
        self.today = date.today() # Update the date
        if self.today.month == 12: # Jump to the next year
            next_date = self.today.replace(year=self.today.year + 1, month=1)

        else:
            month = self.today.month
            month += 1
            max_day = get_max_day_for_month(self.today.year, month)
            # If the next month has lesser days set the day to the last day in the month
            if self.today.day > max_day: 
                next_date = date(self.today.year, month, max_day)
            else: # Jump to next month
                next_date = date(self.today.year, month, self.today.day)
                    
        self.year_var.set(str(next_date.year))
        self.month_var.set(str(next_date.month))
        self.day_var.set(str(next_date.day))

    def add(self):
        """Adds the name to the db"""
        name = self.name_entry.get()

        if name != "":
            name = name.strip() # Strips tailing whitespaces
            year = self.year_var.get()
            month = self.month_var.get()
            day = self.day_var.get()
            try:
                db.add(name, str(self.today), f"{year}-{month}-{day}")
                # Adds the name to the treeview
                self.add_to_treeview_func(name, str(self.today), f"{year}-{month}-{day}")
                
            except IntegrityError: # If name is already in the db
                showerror("Can't add", "Name is already registered")


class RenewFrame(ctk.CTkFrame):
    
    def __init__(self, master, alter_treeview_func, *args, **kwargs):
        super().__init__(master=master, *args, **kwargs)

        self.alter_treeview_func = alter_treeview_func

        # Row configuration
        self.columnconfigure(tuple(range(4)), uniform="a", weight=1)        
        self.rowconfigure(tuple(range(9)), uniform="a", weight=1)        

        self.name_label = ctk.CTkLabel(self, text="", font=MEDIUM_FONT)

        # Values for comboboxes
        self.month = [str(month) for month in range(1, 13)]
        self.days = [str(day) for day in range(1, 32)]

        # Vars for the comboboxes
        self.year_var = ctk.StringVar(value=str(1))
        self.month_var = ctk.StringVar(value=str(1))
        self.day_var = ctk.StringVar(value=str(1))

        # ----- #
        # Labels

        label = ctk.CTkLabel(self, text="Next subscription:", font=MEDIUM_FONT)
        year_label = ctk.CTkLabel(self, text="Year:", font=SMALL_FONT)
        month_label = ctk.CTkLabel(self, text="Month:", font=SMALL_FONT)
        day_label = ctk.CTkLabel(self, text="Day:", font=SMALL_FONT)
        date_label = ctk.CTkLabel(self, text=f"Date: {str(date.today())}", font=SMALL_FONT)
        # ----- #
        # Comboboxes

        self.year_widget = ctk.CTkComboBox(
            self,
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

        renew_btn = ctk.CTkButton(
            self,
            text="Renew",
            fg_color=LIGHT_LIME,
            hover_color=HIGHLIGHTED_LIGHT_LIME,
            command=self.renew,
            text_color=GREY,
            corner_radius=5)
        
        # ----- #
        # Placing widgets

        self.name_label.grid(column=0, row=0, columnspan=4, sticky="w", padx=5)

        label.grid(column=1, columnspan=2, row=3, sticky="n")

        year_label.grid(column=0, row=4, sticky="w")
        self.year_widget.grid(column=0, row=5, columnspan=2, sticky="w", padx=5)

        month_label.grid(column=2, row=4, sticky="w")
        self.month_widget.grid(column=2, row=5, stick="w", padx=5)

        day_label.grid(column=0, row=6, sticky="w")
        self.day_widget.grid(column=0, row=7, sticky="w", padx=5)

        renew_btn.grid(column=3, row=8, padx=3, pady=2)

        date_label.grid(column=3, row=0, sticky="w", pady=2)

        # ----- #
        # Change the value for the days combobox according to the month
        self.change_days("")
    

    def change_days(self, _) -> None:
        """Change the value for the days combobox according to the month"""
        
        year = int(self.year_var.get())
        month = int(self.month_var.get())


        days = self.days[0:get_max_day_for_month(year, month)]

        self.day_widget.configure(values=days)

        # If the next month has lesser days set the day to the last day in the month
        if int(self.day_var.get()) > int(days[-1]):
            self.day_var.set(days[-1])

    def increment_month(self) -> None:
        """Increase the value of the comboboxes to the next month"""
        if self.latest_sub.month == 12: # Jump to the next year
            next_date = self.latest_sub.replace(year=self.latest_sub.year + 1, month=1)

        else:
            month = self.latest_sub.month
            month += 1
            max_day = get_max_day_for_month(self.latest_sub.year, month)

            # If the next month has lesser days set the day to the last day in the month
            if self.latest_sub.day > max_day: 
                next_date = date(self.latest_sub.year, month, max_day)
            else: # Jump to next month
                next_date = date(self.latest_sub.year, month, self.latest_sub.day)

        self.year_var.set(str(next_date.year))
        self.month_var.set(str(next_date.month))
        self.day_var.set(str(next_date.day))

    def set_latest_sub(self, latest_sub: str) -> None:
        # Creates a datetime object that gets converted to a date object
        self.latest_sub = datetime.strptime(latest_sub, '%Y-%m-%d')

        self.latest_sub = date(self.latest_sub.year, self.latest_sub.month, self.latest_sub.day)

        # Values for the year combobox
        self.years = [str(year) for year in range(self.latest_sub.year, self.latest_sub.year + 10)]

        self.year_widget.configure(values=self.years)

        # Vars for the comboboxes
        self.year_var.set(str(self.latest_sub.year))
        self.month_var.set(str(self.latest_sub.month))
        self.day_var.set(str(self.latest_sub.day))

        self.increment_month()


    def set_name(self, name: str) -> None:
        """Set name to the names"""
        self.user_name = name
        self.name_label.configure(text=f"Member: {name}")

    def renew(self) -> None:
        """Changes the last sub and next sub data to the customer in the db"""
        year = self.year_var.get()
        month = self.month_var.get()
        day = self.day_var.get()
        today = str(date.today())

        try:
            db.alter(
                name=self.user_name,
                last_sub=today,
                next_sub=f"{year}-{month}-{day}")
            
        except IntegrityError: # If couldn't find his name
            showerror("Can't alter", "Name is not found")
            return

        # Message to the user
        showinfo("Changed successfully", f"Member renewed successfully \nMEMBER: {self.user_name}")

        # Change values at the treeview
        self.alter_treeview_func(self.user_name, today, f"{year}-{month}-{day}")

     