
from g12_1_salesinput import cal_quarter, get_region_name, has_bad_data, from_input1, from_input2, is_valid_region
from pathlib import Path
import csv
import re
from g12_1_salesfile import import_sales as file_import, already_imported, add_imported_file

NAMING_CONVENTION = "sales_qn_yyyy_r.csv"
SALES_FILE = Path("all_sales.csv")
IMPORTED_FILES = "imported_files.txt"

def view_sales(sales_list: list) -> bool:
    if not sales_list:
        print("No sales to view.")
        return False

    print("     Date           Quarter        Region                  Amount")
    print("-----------------------------------------------------------------")
    total = 0
    for idx, sale in enumerate(sales_list, start=1):
        date = sale['sales_date']
        quarter = cal_quarter(int(date[5:7]))
        region = get_region_name(sale['region'])
        amount = sale['amount']
        print(f"{idx:<5}{date:<15}{quarter:<15}{region:<25}{amount:>10.1f}")
        total += amount
    print("-----------------------------------------------------------------")
    print(f"TOTAL{total:>61.1f}\n")
    return True

def add_sales1(sales_list: list) -> None:
    sale = from_input1()
    sales_list.append(sale)
    print(f"Sales for {sale['sales_date']} is added.")

def add_sales2(sales_list: list) -> None:
    sale = from_input2()
    sales_list.append(sale)
    print(f"Sales for {sale['sales_date']} is added.")

def import_all_sales() -> list:
    sales_list = []
    if not SALES_FILE.exists():
        return sales_list
    with SALES_FILE.open("r") as file:
        reader = csv.reader(file)
        for row in reader:
            try:
                amount = float(row[0])
                sales_date = row[1]
                region = row[2]
                sales_list.append({"amount": amount, "sales_date": sales_date, "region": region})
            except:
                continue
    return sales_list

def import_sales(sales_list: list) -> None:
    file_name = input("Enter name of file to import: ").strip()
    file_path = Path(__file__).parent.parent.parent / 'psc01_files' / file_name

    match = re.match(r"^sales_q([1-4])_(\d{4})_([a-z])\.csv$", file_name)
    if not match:
        print(f"Filename '{file_name}' doesn't follow the expected format of {NAMING_CONVENTION}.\n")
        return

    region_code = match.group(3)
    valid_codes = ('w', 'm', 'c', 'e')
    if region_code not in valid_codes:
        print(f"Filename '{file_name}' doesn't include one of the following region codes: {list(valid_codes)}.\n")
        return

    if already_imported(file_path):
        print(f"File '{file_name}' has already been imported.")
        return

    new_sales = file_import(file_path)
    if new_sales:
        sales_list.extend(new_sales)
        add_imported_file(file_path)
        print("Imported sales added to list.")
    else:
        print("No valid sales to import.")

def save_all_sales(sales_list, delimiter: str = ',') -> None:
    with SALES_FILE.open("w", newline="") as file:
        writer = csv.writer(file, delimiter=delimiter)
        for sale in sales_list:
            writer.writerow([sale['amount'], sale['sales_date'], sale['region']])
