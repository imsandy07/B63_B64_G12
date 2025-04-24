from pathlib import Path
import csv
import re
import g07_2_salesmanager

IMPORTED_FILE = Path(__file__).parent.parent.parent / 'psc01_files' / 'imported_files.txt'


REGIONS = ('w', 'm', 'c', 'e')

def is_valid_filename_format(filename: str) -> bool:
    pattern = r'^sales_q[1-4]_\d{4}_[wmce]\.csv$'
    return re.match(pattern, filename) is not None

def already_imported(file_path: Path) -> bool:
    if not IMPORTED_FILE.exists():
        return False
    with IMPORTED_FILE.open("r") as file:
        imported_files = [line.strip() for line in file.readlines()]
    return str(file_path.name) in imported_files

def add_imported_file(file_path: Path) -> None:
    with IMPORTED_FILE.open("a") as file:
        file.write(f"{file_path.name}\n")

def import_sales(file_path: Path) -> list:
    sales = []
    if not file_path.exists():
        print(f"File {file_path} not found.")
        return sales

    with file_path.open("r", newline="") as file:
        reader = csv.reader(file)
        for i, row in enumerate(reader, start=1):
            if len(row) != 3:
                print(f"Skipping row {i}: wrong number of fields.")
                continue
            try:
                amount = float(row[0])
                sales_date = row[1]
                region = row[2]
                if amount <= 0 or region not in REGIONS:
                    print(f"Skipping row {i}: invalid data.")
                    continue
                sales.append({"amount": amount, "sales_date": sales_date, "region": region})
            except ValueError:
                print(f"Skipping row {i}: unable to convert values.")
                continue
    return sales
