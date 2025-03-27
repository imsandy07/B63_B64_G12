from pathlib import Path
import csv
import re

FILEPATH = Path("psc01_files")
ALL_SALES = FILEPATH / "all_sales.csv"
ALL_SALES_COPY = FILEPATH / "all_sales_copy.csv"
IMPORTED_FILES = FILEPATH / "imported_files.txt"
NAMING_CONVENTION = r"sales_q\d_\d{4}_[wmce]\.csv"
VALID_REGIONS = {'w': 'West', 'm': 'Mountain', 'c': 'Central', 'e': 'East'}

def is_valid_filename_format(filename: str) -> bool:
    return bool(re.fullmatch(NAMING_CONVENTION, filename))

def get_region_code_from_filename(sales_filename: str) -> str:
    return sales_filename[-5]

def already_imported(filepath_name: Path) -> bool:
    if not IMPORTED_FILES.exists():
        return False
    with open(IMPORTED_FILES, 'r') as file:
        imported = file.read().splitlines()
    return str(filepath_name) in imported

def add_imported_file(filepath_name: Path) -> None:
    with open(IMPORTED_FILES, 'a') as file:
        file.write(f"{filepath_name}\n")

def correct_data_types(row) -> None:
    try:
        row[0] = float(row[0])
    except ValueError:
        row[0] = "?"

def import_all_sales() -> list:
    sales_list = []
    with open(ALL_SALES, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) == 3:
                amount, sales_date, region = row
                sales_list.append({"amount": float(amount), "sales_date": sales_date, "region": region})
    return sales_list

def save_all_sales(sales_list, delimiter: str=',') -> None:
    with open(ALL_SALES, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=delimiter)
        for sale in sales_list:
            writer.writerow([sale['amount'], sale['sales_date'], sale['region']])

def initialize_content_of_files(delimiter: str=',') -> None:
    with open(ALL_SALES_COPY, newline='') as source, open(ALL_SALES, 'w', newline='') as dest:
        dest.write(source.read())
    open(IMPORTED_FILES, 'w').close()

def import_sales(filepath_name: Path, delimiter: str = ',') -> list:
    imported_sales_list = []
    with open(filepath_name, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=delimiter)
        region_code = get_region_code_from_filename(filepath_name.name)
        for row in reader:
            correct_data_types(row)
            if len(row) == 2 and row[0] != "?":
                amount, sales_date = row
                imported_sales_list.append({"amount": float(amount), "sales_date": sales_date, "region": region_code})
    return imported_sales_list
