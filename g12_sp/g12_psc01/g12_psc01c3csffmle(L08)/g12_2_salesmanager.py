from g12_1_salesinput import cal_quarter, get_region_name, has_bad_data, from_input1, from_input2, is_valid_region
from pathlib import Path
import csv
import re
from decimal import Decimal, ROUND_HALF_UP
import locale as lc
import g12_1_salesfile as sf
from g12_1_salesfile import import_sales as file_import, is_valid_filename_format, already_imported, add_imported_file

lc.setlocale(lc.LC_ALL, "en_US")

NAMING_CONVENTION = "sales_qn_yyyy_r.csv"
SALES_FILE = Path("all_sales.csv")
IMPORTED_FILES = "imported_files.txt"

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

    print(f"{'Date':>10} {'Quarter':>12} {'Region':>15} {'Amount':>20}")
    print("-" * 65)
    total = Decimal('0.00')
    for i, sale in enumerate(sales_list, 1):
        amount = Decimal(str(sale['amount'])).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        date = sale['sales_date']
        quarter = cal_quarter(int(date[5:7]))
        region_name = get_region_name(sale['region'])
        print(f"{i:>2}. {date:>10} {quarter:>12} {region_name:>15} {amount:>20,.2f}")
        total += amount
    print("-" * 65)
    print(f"{'TOTAL':>52} {total:>13,.2f}")
    return True

def import_sales(sales_list: list) -> None:
    file_name = input("Enter name of file to import: ").strip()
    file_path = Path(__file__).parent.parent.parent / 'psc01_files' / file_name

    match = re.match(r"^sales_q([1-4])_(\d{4})_([a-z])\.csv$", file_name)
    if not match:
        print(f"Filename '{file_name}' doesn't follow the expected format of {NAMING_CONVENTION}.")
        return

    region_code = match.group(3)
    valid_codes = ('w', 'm', 'c', 'e')
    if region_code not in valid_codes:
        print(f"Filename '{file_name}' doesn't include one of the following region codes: {list(valid_codes)}.")
        return

    if already_imported(file_path):
        print(f"File '{file_name}' has already been imported.")
        return

    try:
        new_sales = file_import(file_path)
        if new_sales:
            sales_list.extend(new_sales)
            add_imported_file(file_path)
            print("Imported sales added to list.")
        else:
            print("No valid sales to import.")
    except Exception as e:
        print(type(e), f". Fail to import sales from '{file_name}'.")

def import_all_sales() -> list:
    sales = []
    if SALES_FILE.exists():
        try:
            with SALES_FILE.open("r", newline="") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    try:
                        row['amount'] = float(row['amount'])
                        if not has_bad_data(row):
                            sales.append(row)
                    except:
                        continue
        except Exception as e:
            print(f"Error reading sales file: {e}")
    return sales

def save_all_sales(sales_list: list, delimiter: str = ',') -> None:
    try:
        with SALES_FILE.open("w", newline="") as file:
            fieldnames = ["amount", "sales_date", "region"]
            writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=delimiter)
            writer.writeheader()
            for sale in sales_list:
                writer.writerow(sale)
    except Exception as e:
        print(f"Error saving sales file: {e}")

def initialize_content_of_files(delimiter: str = ',') -> None:
    if not SALES_FILE.exists():
        try:
            with SALES_FILE.open("w", newline="") as file:
                fieldnames = ["amount", "sales_date", "region"]
                writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=delimiter)
                writer.writeheader()
        except Exception as e:
            print(f"Error initializing file: {e}")

def raise_exception() -> None:
    try:
        with open(sf.SALES_FILE, 'w', newline='') as csvfile:
            raise OSError("Artificial OSError raised for test.")
    except OSError as e:
        print("Is the file closed yet?", csvfile.closed)
        print(type(e))
        raise
    finally:
        print("Confirm if the file is closed.", csvfile.closed)
