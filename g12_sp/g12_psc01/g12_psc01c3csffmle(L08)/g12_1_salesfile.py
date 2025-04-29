from pathlib import Path
import csv
import re
from datetime import datetime

IMPORTED_FILE = Path(__file__).parent.parent.parent / 'psc01_files' / 'imported_files.txt'
REGIONS = ('w', 'm', 'c', 'e')
DATE_FORMAT = "%Y-%m-%d"

def is_valid_filename_format(filename: str) -> bool:
    pattern = r'^sales_q[1-4]_\d{4}_[wmce]\.csv$'
    return re.match(pattern, filename) is not None

def get_region_code_from_filename(sales_filename: str) -> str:
    match = re.match(r"^sales_q[1-4]_\d{4}_([wmce])\.csv$", sales_filename)
    return match.group(1) if match else ""

def already_imported(file_path: Path) -> bool:
    try:
        if not IMPORTED_FILE.exists():
            return False
        with IMPORTED_FILE.open("r") as file:
            imported_files = [line.strip() for line in file.readlines()]
        return str(file_path.name) in imported_files
    except Exception as e:
        print(f"Error checking import status: {e}")
        return False

def add_imported_file(file_path: Path) -> None:
    try:
        with IMPORTED_FILE.open("a") as file:
            file.write(f"{file_path.name}\n")
    except Exception as e:
        print(f"Error logging imported file: {e}")

def correct_data_types(row) -> None:
    try:
        row[0] = float(row[0])
    except ValueError:
        row[0] = "?"
    try:
        sales_date = datetime.strptime(row[1], DATE_FORMAT)
        row[1] = sales_date.date().isoformat()
    except ValueError:
        row[1] = "?"

def import_sales(file_path: Path, delimiter: str = ',') -> list:
    sales = []
    if not file_path.exists():
        print(f"File {file_path} not found.")
        return sales

    with file_path.open("r", newline="") as file:
        reader = csv.reader(file, delimiter=delimiter)
        for i, row in enumerate(reader, start=1):
            if len(row) != 3:
                print(f"Skipping row {i}: wrong number of fields.")
                continue
            correct_data_types(row)
            amount, sales_date, region = row
            if amount == "?" or sales_date == "?" or region not in REGIONS:
                print(f"Skipping row {i}: invalid data.")
                continue
            sales.append({"amount": amount, "sales_date": sales_date, "region": region})
    return sales
