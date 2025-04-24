from g07_1_salesinput import cal_quarter, get_region_name, has_bad_data, from_input1, from_input2, is_valid_region
from pathlib import Path
from g07_1_salesinput import *
import csv
import re
from pickle import FALSE
import g07_1_salesinput

NAMING_CONVENTION = "sales_qn_yyyy_r.csv"
SALES_FILE = Path("all_sales.csv")
IMPORTED_FILES = "imported_files.txt"

def has_bad_amount(data: dict) -> bool:
    return data["amount"] == "?"

def has_bad_date(data: dict) -> bool:
    return data["sales_date"] == "?"

def has_bad_data(data: dict) -> bool:
    return has_bad_amount(data) or has_bad_date(data)

def correct_data_types(row) -> None:
    """
    Try to convert valid amount to float type
    and mark invalid amount or sales date as '?'
    """
    try:  # amount
        row[0] = float(row[0])  # convert to float
    except ValueError:
        row[0] = "?"  # Mark invalid amount as bad
    # date
    if len(row[1]) == 10 and row[1][4] == '-' and row[1][7] == '-' \
            and row[1][:4].isdigit() and row[1][5:7].isdigit() and row[1][8:10].isdigit():
        yyyy, mm, dd = int(row[1][:4]), int(row[1][5:7]), int(row[1][8:10])
        if not (1 <= mm <= 12) or not (1 <= dd <= cal_max_day(yyyy, mm)):
            row[1] = "?"  # Mark invalid date as bad
    else:
        row[1] = "?"  # Mark invalid date as bad

def view_sales(sales_list: list) -> bool:
    col1_w, col2_w, col3_w, col4_w, col5_w = 5, 15, 15, 15, 15
    bad_data_flag = False
    if len(sales_list) == 0:
        print("No sales to view.")
    else:
        total_w = col1_w + col2_w + col3_w + col4_w + col5_w
        print(f"{' ':{col1_w}}"
              f"{'Date':{col2_w}}"
              f"{'Quarter':{col3_w}}"
              f"{'Region':{col4_w}}"
              f"{'Amount':>{col5_w}}")
        print(horizontal_line := f"{'-' * total_w}")
        total = 0.0

        for idx, sales in enumerate(sales_list, start=1):
            if has_bad_data(sales):
                bad_data_flag = True
                num = f"{idx}.*"
            else:
                num = f"{idx}."

            amount = sales["amount"]
            if not has_bad_amount(sales):
                total += amount

            sales_date = sales["sales_date"]
            if has_bad_date(sales):
                bad_data_flag = True
                month = 0
            else:
                month = int(sales_date.split("-")[1])

            region = get_region_name(sales["region"])
            quarter = f"{cal_quarter(month)}"
            print(f"{num:<{col1_w}}"
                  f"{sales_date:{col2_w}}"
                  f"{quarter:<{col3_w}}"
                  f"{region:{col4_w}}"
                  f"{amount:>{col5_w}}")

        print(horizontal_line)
        print(f"{'TOTAL':{col1_w}}"
              f"{' ':{col2_w + col3_w + col4_w}}"
              f"{total:>{col5_w}}\n")
    return bad_data_flag

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

def get_region_code(sales_filename: str) -> str:
    try:
        return sales_filename.split("_")[3].split(".")[0].lower()
    except IndexError:
        return ""

def is_valid_filename_format(filename: str) -> bool:
    pattern = r"^sales_q[1-4]_\d{4}_[wmce]\.csv$"
    return re.match(pattern, filename) is not None

def already_imported(file_path: Path) -> bool:
    try:
        with open(IMPORTED_FILES, 'r') as file:
            return file_path.name in file.read().splitlines()
    except FileNotFoundError:
        return False

def add_imported_file(filepath_name: Path) -> None:
    with open(IMPORTED_FILES, 'a') as file:
        file.write(filepath_name.name + "\n")

def import_sales(sales_list: list) -> None:
    from g07_1_salesfile import import_sales as file_import

    file_name = input("Enter name of file to import: ").strip()
    file_path = Path(__file__).parent.parent.parent / 'psc01_files' / file_name

    match = re.match(r"^sales_q([1-4])_(\d{4})_([a-z])\.csv$", file_name)
    if not match:
        print(f"Filename '{file_name}' doesn't follow the expected format of {NAMING_CONVENTION}.\n")
        return

    # Step 2: Check if region code is valid
    region_code = match.group(3)
    valid_codes = ('w', 'm', 'c', 'e')
    if region_code not in valid_codes:
        print(f"Filename '{file_name}' doesn't include one of the following region codes: {list(valid_codes)}.\n")
        return

    # Step 3: Check if file already imported
    if already_imported(file_path):
        print(f"File '{file_name}' has already been imported.")
        return

    # Step 4: Import
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
    with SALES_FILE.open(mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["amount", "sales_date", "region"])
        writer.writeheader()
        writer.writerows(sales_list)