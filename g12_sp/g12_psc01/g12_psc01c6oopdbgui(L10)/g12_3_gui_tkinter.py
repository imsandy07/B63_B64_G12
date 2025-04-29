from g12_1_1salestypes import Sales
from g12_2_2salesdb import SQLiteDBAccess

from datetime import datetime
import tkinter as tk
from tkinter import ttk, Toplevel, messagebox
from PIL import Image, ImageTk

class SalesFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.grid(padx=20, pady=20)

        self.db_access = SQLiteDBAccess()
        self.current_sales = None

        style = ttk.Style()
        if 'clam' in style.theme_names():
            style.theme_use('clam')
        style.configure("TLabel", font=("Helvetica", 10))
        style.configure("TButton", font=("Helvetica", 10))
        style.configure("Header.TLabel", font=("Helvetica", 14, "bold"))

        self.__init_components()

    def __init_components(self):
        ttk.Label(self, text="Edit Sales Record", style="Header.TLabel").grid(row=0, column=0, columnspan=2, pady=(0, 15))

        ttk.Label(self, text="Date (yyyy-mm-dd):").grid(row=1, column=0, sticky="e", pady=5)
        self.date_entry = ttk.Entry(self)
        self.date_entry.grid(row=1, column=1, sticky="ew", pady=5)

        ttk.Label(self, text="Region Code:").grid(row=2, column=0, sticky="e", pady=5)
        self.region_entry = ttk.Entry(self)
        self.region_entry.grid(row=2, column=1, sticky="ew", pady=5)

        ttk.Label(self, text="Amount:").grid(row=3, column=0, sticky="e", pady=5)
        self.amount_entry = ttk.Entry(self, state='readonly')
        self.amount_entry.grid(row=3, column=1, sticky="ew", pady=5)

        ttk.Label(self, text="ID:").grid(row=4, column=0, sticky="e", pady=5)
        self.id_entry = ttk.Entry(self, state='readonly')
        self.id_entry.grid(row=4, column=1, sticky="ew", pady=5)

        button_frame = ttk.Frame(self)
        button_frame.grid(row=5, column=0, columnspan=2, pady=15)

        self.get_button = ttk.Button(button_frame, text="Get Amount", command=self.__get_amount)
        self.get_button.grid(row=0, column=0, padx=5)

        self.clear_button = ttk.Button(button_frame, text="Clear Field", command=self.__clear_field)
        self.clear_button.grid(row=0, column=1, padx=5)

        self.save_button = ttk.Button(button_frame, text="Save Changes", command=self.__save_changes, state='disabled')
        self.save_button.grid(row=0, column=2, padx=5)

        self.exit_button = ttk.Button(button_frame, text="Exit", command=self.quit)
        self.exit_button.grid(row=0, column=3, padx=5)

        self.columnconfigure(1, weight=1)

    def __popup_error(self, title, message):
        win = Toplevel(self)
        win.title(title)
        win.configure(bg="white")
        win.resizable(False, False)
        win.geometry("320x180")
        win.grab_set()

        try:
            img = Image.open("rocket.png").resize((40, 40))
            img = ImageTk.PhotoImage(img)
            logo = ttk.Label(win, image=img, background="white")
            logo.image = img
            logo.pack(pady=(15, 5))
        except Exception:
            pass

        ttk.Label(win, text=message, background="white", font=("Helvetica", 10)).pack(pady=5)
        ttk.Button(win, text="OK", command=win.destroy).pack(pady=(5, 10))

    def __clear_field(self):
        self.date_entry.delete(0, tk.END)
        self.region_entry.delete(0, tk.END)
        self.amount_entry.config(state='normal')
        self.amount_entry.delete(0, tk.END)
        self.amount_entry.config(state='readonly')
        self.id_entry.config(state='normal')
        self.id_entry.delete(0, tk.END)
        self.id_entry.config(state='readonly')
        self.save_button.config(state='disabled')
        self.current_sales = None

    def __validate_inputs(self) -> bool:
        date_str = self.date_entry.get().strip()
        region_code = self.region_entry.get().strip().lower()

        if not date_str or not region_code:
            self.__popup_error("Missing Input", "Please enter date and region.")
            return False

        try:
            sales_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            if not (Sales.MIN_YEAR <= sales_date.year <= Sales.MAX_YEAR):
                self.__popup_error("Invalid Year", "A valid year is between 2000 and 2999.")
                return False
        except ValueError:
            self.__popup_error("Invalid Date", f"{date_str} is not in a valid date format 'yyyy-mm-dd'")
            return False

        regions = self.db_access.retrieve_regions()
        if not regions or not regions.is_valid_region_code(region_code):
            self.__popup_error("Invalid Region", f"{region_code} is not one of the valid region codes.")
            return False

        return True

    def __get_amount(self):
        if not self.__validate_inputs():
            return

        date_str = self.date_entry.get().strip()
        region_code = self.region_entry.get().strip().lower()
        sales_date = datetime.strptime(date_str, "%Y-%m-%d").date()

        sales = self.db_access.retrieve_sales_by_date_region(sales_date, region_code)
        if not sales:
            self.__popup_error("No Record", "No sales found.")
            return

        self.current_sales = sales
        self.amount_entry.config(state='normal')
        self.amount_entry.delete(0, tk.END)
        self.amount_entry.insert(0, str(sales['amount']))
        self.amount_entry.config(state='readonly')

        self.id_entry.config(state='normal')
        self.id_entry.delete(0, tk.END)
        self.id_entry.insert(0, str(sales['ID']))
        self.id_entry.config(state='readonly')

        self.save_button.config(state='normal')

    def __save_changes(self):
        if not self.current_sales:
            return

        try:
            self.amount_entry.config(state='normal')
            new_amount = float(self.amount_entry.get())
            self.amount_entry.config(state='readonly')

            if new_amount <= 0:
                self.__popup_error("Invalid Amount", "Amount must be greater than 0.")
                return

            self.current_sales['amount'] = new_amount
            self.db_access.update_sales(self.current_sales)
            messagebox.showinfo("Success", "Sales record updated.")
            self.__clear_field()

        except ValueError:
            self.__popup_error("Invalid Input", "Please enter a valid number.")

def main():
    root = tk.Tk()
    root.title("Edit Sales Amount")
    root.geometry("460x340")
    SalesFrame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
