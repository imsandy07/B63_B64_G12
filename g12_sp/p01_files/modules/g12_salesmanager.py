from g12_salesinput import cal_quarter, get_region_name, has_bad_data, from_input1, from_input2
from g12_salesfile import is_valid_filename_format, already_imported, import_sales as file_import, add_imported_file
from pathlib import Path
import csv

# Ensure the 'data' directory exists
data_dir = Path("data")
data_dir.mkdir(parents=True, exist_ok=True)

# Define the sales file path
SALES_FILE = Path("data/all_sales.csv")

def view_sales(sales_list: list) -> bool:
    if not sales_list:
        print("No sales to view.")
        return False
    print("\n  Date        Quarter   Region     Amount")
    total = 0
    for i, sale in enumerate(sales_list, 1):
        year, month, _ = map(int, sale["sales_date"].split("-"))
        quarter = cal_quarter(month)
        region = get_region_name(sale["region"])
        amount = sale["amount"]
        total += amount
        print(f"{i:>2}. {sale['sales_date']}     {quarter:<2}      {region:<9} {amount:>8.1f}")
    print("\nTOTAL".rjust(40), f"{total:.1f}")
    return True

def add_sales1(sales_list: list) -> None:
    data = from_input1()
    if not has_bad_data(data):
        sales_list.append(data)
        print(f"Sales for {data['sales_date']} is added.")

def add_sales2(sales_list: list) -> None:
    data = from_input2()
    if not has_bad_data(data):
        sales_list.append(data)
        print(f"Sales for {data['sales_date']} is added.")

def import_sales(sales_list: list) -> None:
    file_name = input("Enter name of file to import: ")
    if not is_valid_filename_format(file_name):
        print("Filename doesn't follow the expected format of sales_qn_yyyy_r.csv.")
        return

    file_path = Path("data") / file_name  # Ensured file path is pointing to data directory

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

def import_all_sales() -> list:
    sales_list = []
    if not SALES_FILE.exists():
        return sales_list

    with SALES_FILE.open(mode="r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                row["amount"] = float(row["amount"])
                sales_list.append(row)
            except:
                continue
    return sales_list

def save_all_sales(sales_list: list) -> None:
    # Ensure 'data' directory exists before trying to save
    data_dir = Path("data")
    data_dir.mkdir(parents=True, exist_ok=True)

    with SALES_FILE.open(mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["amount", "sales_date", "region"])
        writer.writeheader()
        writer.writerows(sales_list)