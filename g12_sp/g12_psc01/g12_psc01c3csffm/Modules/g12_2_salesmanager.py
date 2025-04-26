from g12_1_salesinput import cal_quarter, get_region_name, has_bad_data, from_input1, from_input2, is_valid_region
from pathlib import Path
from g12_1_salesinput import *
import csv
import re
from pickle import FALSE
import g12_1_salesinput

NAMING_CONVENTION = "sales_qn_yyyy_r.csv"
SALES_FILE = Path("all_sales.csv")
IMPORTED_FILES = "imported_files.txt"

# (functions same as before...)

def import_sales(sales_list: list) -> None:
    from g12_1_salesfile import import_sales as file_import

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
