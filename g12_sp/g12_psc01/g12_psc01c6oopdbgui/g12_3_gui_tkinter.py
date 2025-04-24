# g07_3_gui_tkinter.py
from g07_1_1salestypes import Sales
from g07_2_2salesdb import SQLiteDBAccess
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox


class SalesFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.db_access = SQLiteDBAccess()
        self.current_sales = None
        self.__init_components()

    def __init_components(self):
        self.pack(fill=tk.BOTH, expand=True)

        # Labels
        ttk.Label(self, text="Enter date and region to get sales amount").grid(row=0, column=0, columnspan=3, pady=5)
        ttk.Label(self, text="Date:").grid(row=1, column=0, sticky=tk.E, padx=5, pady=5)
        ttk.Label(self, text="Region:").grid(row=2, column=0, sticky=tk.E, padx=5, pady=5)
        ttk.Label(self, text="Amount:").grid(row=3, column=0, sticky=tk.E, padx=5, pady=5)
        ttk.Label(self, text="ID:").grid(row=4, column=0, sticky=tk.E, padx=5, pady=5)

        # Entry fields
        self.date_entry = ttk.Entry(self)
        self.region_entry = ttk.Entry(self)
        self.amount_entry = ttk.Entry(self, state='readonly')
        self.id_entry = ttk.Entry(self, state='readonly')

        self.date_entry.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        self.region_entry.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        self.amount_entry.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)
        self.id_entry.grid(row=4, column=1, sticky=tk.W, padx=5, pady=5)

        # Buttons
        ttk.Button(self, text="Get Amount", command=self.__get_amount).grid(row=5, column=0, padx=5, pady=5)
        ttk.Button(self, text="Clear Field", command=self.__clear_field).grid(row=5, column=1, padx=5, pady=5)
        ttk.Button(self, text="Save Changes", command=self.__save_changes, state='disabled').grid(row=5, column=2,
                                                                                                  padx=5, pady=5)
        ttk.Button(self, text="Exit", command=self.quit).grid(row=6, column=1, pady=10)

        self.save_button = self.children['!button3']  # Reference to Save Changes button

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
        date_str = self.date_entry.get()
        region_code = self.region_entry.get().strip().lower()

        # Check if fields are empty
        if not date_str or not region_code:
            messagebox.showerror("Error", "Please enter date and region to get sales amount")
            return False

        # Validate date format
        try:
            sales_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            if not (Sales.MIN_YEAR <= sales_date.year <= Sales.MAX_YEAR):
                messagebox.showerror("Error", f"Year must be between {Sales.MIN_YEAR} and {Sales.MAX_YEAR}")
                return False
        except ValueError:
            messagebox.showerror("Error", f"'{date_str}' is not in a valid date format 'yyyy-mm-dd'")
            return False

        # Validate region code
        regions = self.db_access.retrieve_regions()
        if not regions or not regions.is_valid_region_code(region_code):
            messagebox.showerror("Error", f"'{region_code}' is not a valid region code")
            return False

        return True

    def __get_amount(self):
        if not self.__validate_inputs():
            return

        date_str = self.date_entry.get()
        region_code = self.region_entry.get().strip().lower()
        sales_date = datetime.strptime(date_str, "%Y-%m-%d").date()

        sales = self.db_access.retrieve_sales_by_date_region(sales_date, region_code)
        if sales is None:
            messagebox.showerror("Error", "No sales record found for the given date and region")
            return

        self.current_sales = sales
        self.amount_entry.config(state='normal')
        self.amount_entry.delete(0, tk.END)
        self.amount_entry.insert(0, str(sales['amount']))
        self.id_entry.config(state='normal')
        self.id_entry.delete(0, tk.END)
        self.id_entry.insert(0, str(sales['ID']))
        self.save_button.config(state='normal')

    def __save_changes(self):
        if self.current_sales is None:
            return

        try:
            new_amount = float(self.amount_entry.get())
            if new_amount <= 0:
                messagebox.showerror("Error", "Amount must be greater than 0")
                return

            self.current_sales['amount'] = new_amount
            self.db_access.update_sales(self.current_sales)
            messagebox.showinfo("Success", "Sales record updated successfully")
            self.__clear_field()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount")


def main():
    root = tk.Tk()
    root.title("Edit Sales Amount")
    SalesFrame(root)
    root.mainloop()


if __name__ == "__main__":
    main()
