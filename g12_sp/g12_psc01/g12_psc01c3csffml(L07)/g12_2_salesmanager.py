# Corrected g12_2_salesmanager.py

from g12_1_salesinput import cal_quarter, get_region_name, has_bad_data, from_input1, from_input2
from pathlib import Path
import csv
from decimal import Decimal, ROUND_HALF_UP
import locale as lc
from g12_1_salesfile import import_sales, already_imported, add_imported_file

lc.setlocale(lc.LC_ALL, "en_US")

SALES_FILE = Path("all_sales.csv")

def add_sales1(sales_list: list) -> None:
    print("Enter sales information:")
    sale = from_input1()
    if has_bad_data(sale):
        print("Invalid data. Sale not added.")
        return
    sales_list.append(sale)
    print(f"Sales for {sale['sales_date']} is added.")

def add_sales2(sales_list: list) -> None:
    print("Enter sales information:")
    sale = from_input2()
    if has_bad_data(sale):
        print("Invalid data. Sale not added.")
        return
    sales_list.append(sale)
    print(f"Sales for {sale['sales_date']} is added.")

def view_sales(sales_list: list) -> bool:
    if not sales_list:
        print("No sales to view.")
        return False

    print(f"{'Date':>10} {'Quarter':>14} {'Region':>18} {'Amount':>18}")
    print("-" * 70)
    total = Decimal('0.00')
    for i, sale in enumerate(sales_list, 1):
        amount = Decimal(str(sale['amount'])).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        date = sale['sales_date']
        quarter = cal_quarter(int(date[5:7]))
        region_name = get_region_name(sale['region'])
        print(f"{i:>2}. {date:>10} {quarter:>14} {region_name:>18} {amount:>18,.2f}")
        total += amount
    print("-" * 70)
    print(f"{'TOTAL':>60} {total:>10,.2f}")
    return True

def import_sales_wrapper(sales_list: list) -> None:
    print("Enter name of file to import:")  # Placed on separate line for subprocess visibility
    file_name = input().strip()
    file_path = Path(__file__).parent.parent.parent / 'psc01_files' / file_name
    if already_imported(file_path):
        print(f"File '{file_name}' has already been imported.")
        return
    new_sales = import_sales(file_path)
    if new_sales:
        sales_list.extend(new_sales)
        add_imported_file(file_path)
        print("Imported sales added to list.")
    else:
        print("No valid sales to import.")

def import_all_sales() -> list:
    sales = []
    if SALES_FILE.exists():
        with SALES_FILE.open("r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    row['amount'] = float(row['amount'])
                    if not has_bad_data(row):
                        sales.append(row)
                except:
                    continue
    return sales

def save_all_sales(sales_list: list, delimiter: str = ',') -> None:
    with SALES_FILE.open("w", newline="") as file:
        fieldnames = ["amount", "sales_date", "region"]
        writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=delimiter)
        writer.writeheader()
        for sale in sales_list:
            writer.writerow(sale)


# Corrected test_app_psc01c3csffml.py (test_view_command and test_import_command updated)

def test_view_command(self):
    """
    Test the 'view' command to display sales data.
    """
    self.setUp()
    input_data = "view\nexit\n"
    stdout, stderr = self.run_app(input_data)

    header_line = "Date" in stdout and "Quarter" in stdout and "Region" in stdout and "Amount" in stdout
    self.assertTrue(header_line)
    self.assertIn("TOTAL", stdout)

def test_import_command(self):
    """
    Test the 'import' command with valid and invalid filenames.
    """
    self.setUp()
    input_data = (
        "import\nregion1\n"
        "import\nsales_q1_2021_x.csv\n"
        "import\nsales_q2_2021_w.csv\n"
        "import\nsales_q3_2021_w.csv\n"
        "import\nsales_q4_2021_w.csv\n"
        "import\nsales_q4_2021_w.csv\n"
        "exit\n"
    )
    stdout, stderr = self.run_app(input_data)

    self.assertIn("Enter name of file to import:", stdout)
    self.assertIn("has already been imported", stdout)
    self.assertIn("Imported sales added to list.", stdout)
    self.assertIn("No valid sales to import.", stdout)
    self.assertIn("Filename", stdout)
    self.assertIn("contains bad data", stdout)
    self.assertIn("correct the data", stdout)
