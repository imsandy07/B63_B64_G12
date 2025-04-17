from g12_1_1salestypes import Sales
from g12_2_2salesdb import SQLiteDBAccess

from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, Toplevel, Label, Button
from PIL import Image, ImageTk

class SalesFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.grid(padx=20, pady=20)
        parent.configure(bg='white')
        self.configure(style='Custom.TFrame')

        self.db_access = SQLiteDBAccess()
        self.sales_obj = None

        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TLabel', font=('Helvetica', 10), background='white')
        style.configure('TEntry', font=('Helvetica', 10))
        style.configure('TButton', font=('Helvetica', 10), padding=5)
        style.configure('Custom.TFrame', background='white')

        self.__init_components()

    def __init_components(self):
        title = ttk.Label(self, text="Enter date and region to get sales amount", font=("Helvetica", 14, "bold"))
        title.grid(row=0, column=0, columnspan=2, pady=(0, 15))

        ttk.Label(self, text="Date (yyyy-mm-dd):").grid(row=1, column=0, sticky="w", pady=5)
        self.date_entry = ttk.Entry(self)
        self.date_entry.grid(row=1, column=1, sticky="ew", pady=5)

        ttk.Label(self, text="Region Code:").grid(row=2, column=0, sticky="w", pady=5)
        self.region_entry = ttk.Entry(self)
        self.region_entry.grid(row=2, column=1, sticky="ew", pady=5)

        ttk.Label(self, text="Amount:").grid(row=3, column=0, sticky="w", pady=5)
        self.amount_entry = ttk.Entry(self)
        self.amount_entry.grid(row=3, column=1, sticky="ew", pady=5)
        self.amount_entry.config(state="disabled")

        btn_frame = ttk.Frame(self, style='Custom.TFrame')
        btn_frame.grid(row=4, column=0, columnspan=2, pady=20)

        self.get_button = ttk.Button(btn_frame, text="Get Amount", command=self.__get_amount)
        self.get_button.grid(row=0, column=0, padx=5)

        self.clear_button = ttk.Button(btn_frame, text="Clear Field", command=self.__clear_field)
        self.clear_button.grid(row=0, column=1, padx=5)

        self.save_button = ttk.Button(btn_frame, text="Save Changes", command=self.__save_changes)
        self.save_button.grid(row=0, column=2, padx=5)
        self.save_button.state(["disabled"])

        self.exit_button = ttk.Button(btn_frame, text="Exit", command=self.quit)
        self.exit_button.grid(row=0, column=3, padx=5)

        self.columnconfigure(1, weight=1)

    def __clear_field(self):
        self.date_entry.delete(0, tk.END)
        self.region_entry.delete(0, tk.END)
        self.amount_entry.config(state="normal")
        self.amount_entry.delete(0, tk.END)
        self.amount_entry.config(state="disabled")
        self.save_button.state(["disabled"])

    def __show_rocket_alert(self, title, message):
        win = Toplevel()
        win.title(title)
        win.configure(bg="white")
        win.geometry("350x200")
        Label(win, text=message, font=("Helvetica", 11), bg="white").pack(pady=(20, 10))

        try:
            img = Image.open("rocket.png").resize((50, 50))
            rocket_img = ImageTk.PhotoImage(img)
            image_label = Label(win, image=rocket_img, bg="white")
            image_label.image = rocket_img
            image_label.pack()
        except:
            pass

        Button(win, text="OK", command=win.destroy, font=("Helvetica", 10)).pack(pady=10)

    def __get_amount(self):
        date_str = self.date_entry.get().strip()
        region_code = self.region_entry.get().strip().lower()

        if not date_str or not region_code:
            self.__show_rocket_alert("Missing Input", "Please enter date and region to get sales amount")
            return

        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
            if not (2000 <= date_obj.year <= 2999):
                raise ValueError("Invalid year")
        except ValueError:
            self.__show_rocket_alert("Invalid Date", f"{date_str} is not in a valid date format 'yyyy-mm-dd'")
            return

        if not self.db_access.retrieve_regions().is_valid_region_code(region_code):
            self.__show_rocket_alert("Invalid Region", f"{region_code} is not a valid region code.")
            return

        self.sales_obj = self.db_access.retrieve_sales_by_date_region(date_obj, region_code)

        if not self.sales_obj:
            self.__show_rocket_alert("Not Found", "No sales record found.")
            return

        self.amount_entry.config(state="normal")
        self.amount_entry.delete(0, tk.END)
        self.amount_entry.insert(0, str(self.sales_obj["amount"]))
        self.save_button.state(["!disabled"])

    def __save_changes(self):
        try:
            new_amount = float(self.amount_entry.get())
            self.sales_obj["amount"] = new_amount
            self.db_access.update_sales(self.sales_obj)
            self.__show_rocket_alert("Success", "Sales record updated successfully.")
        except ValueError:
            self.__show_rocket_alert("Invalid Input", "Please enter a valid amount.")

def main():
    root = tk.Tk()
    root.title("Edit Sales Amount")
    root.geometry("430x300")
    SalesFrame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
