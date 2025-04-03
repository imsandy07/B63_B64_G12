from typing import Optional
from pathlib import Path
import csv
from functools import singledispatch

VALID_REGIONS = {"w": "West", "m": "Mountain", "c": "Central", "e": "East"}
DATE_FORMAT = "%Y-%m-%d"
MIN_YEAR, MAX_YEAR = 2000, 2999
FILEPATH = Path(__file__).parent.parent.parent / 'psc01_files'
NAMING_CONVENTION = "sales_qn_yyyy_r.csv"
ALL_SALES = 'all_sales.csv'
ALL_SALES_COPY = 'all_sales_copy.csv'
IMPORTED_FILES = 'imported_files.txt'

def input_amount() -> float:
    while True:
        entry = float(input(f"{'Amount:':20}"))
        if entry > 0:
            return entry
        print("Amount must be greater than zero.")

def input_int(entry_item: str, high: int, low: int = 1, fmt_width: int = 20) -> int:
    prompt = f"{entry_item.capitalize()} ({low}-{high}):"
    while True:
        entry = int(input(f"{prompt:{fmt_width}}"))
        if low <= entry <= high:
            return entry
        print(f"{entry_item.capitalize()} must be between {low} and {high}.")

def input_year() -> int:
    return input_int('year', MAX_YEAR, MIN_YEAR)

def input_month() -> int:
    return input_int("month", 12, fmt_width=20)

def is_leap_year(year: int) -> bool:
    return (year % 400 == 0) or (year % 4 == 0 and year % 100 != 0)

def cal_max_day(year: int, month: int) -> int:
    if is_leap_year(year) and month == 2:
        return 29
    if month == 2:
        return 28
    if month in (4, 6, 9, 11):
        return 30
    return 31

def input_day(year: int, month: int) -> int:
    max_day = cal_max_day(year, month)
    parameters = {"entry_item": "day", "high": max_day}
    return input_int(**parameters)

def input_date() -> str:
    while True:
        entry = input(f"{'Date (yyyy-mm-dd):':20}").strip()
        if len(entry) == 10 and entry[4] == '-' and entry[7] == '-' \
                and entry[:4].isdigit() and entry[5:7].isdigit() and entry[8:].isdigit():
            yyyy, mm, dd = int(entry[:4]), int(entry[5:7]), int(entry[8:])
            if (1 <= mm <= 12) and (1 <= dd <= cal_max_day(yyyy, mm)):
                if MIN_YEAR <= yyyy <= MAX_YEAR:
                    return entry
                print(f"Year of the date must be between {MIN_YEAR} and {MAX_YEAR}.")
        print(f"{entry} is not in a valid date format.")

def input_region_code() -> Optional[str]:
    while True:
        fmt = 20
        valid_codes = tuple(VALID_REGIONS.keys())
        prompt = f"{f'Region {valid_codes}:':{fmt}}"
        code = input(prompt)
        if code in valid_codes:
            return code
        print(f"Region must be one of the following: {valid_codes}.")

def from_input1() -> dict:
    amount = input_amount()
    year = input_year()
    month = input_month()
    day = input_day(year, month)
    sales_date = f"{year}-{str(month).zfill(2)}-{day:02}"
    region_code = input_region_code()
    return {"amount": amount, "sales_date": sales_date, "region": region_code}

def from_input2() -> dict:
    amount = input_amount()
    sales_date = input_date()
    region_code = input_region_code()
    return {"amount": amount, "sales_date": sales_date, "region": region_code}

def already_imported(filepath_name: Path) -> bool:
    if not Path(IMPORTED_FILES).exists():
        return False
    with open(IMPORTED_FILES, "r") as file:
        return filepath_name.name in file.read().splitlines()

def add_imported_file(filepath_name: Path) -> None:
    with open(IMPORTED_FILES, "a") as file:
        file.write(filepath_name.name + "\n")

@singledispatch
def import_sales(filepath_name, delimiter: str = ',') -> list:
    if not isinstance(filepath_name, (str, Path)):
        raise TypeError("Expected a string or Path object for filepath_name.")

    filepath = Path(filepath_name)
    imported_sales_list = []
    try:
        with open(filepath, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=delimiter)
            filename = filepath.name
            region_code = filename[filename.rfind('.') - 1]
            for row in reader:
                if len(row) == 2:
                    amount, sales_date = row
                    imported_sales_list.append({"amount": float(amount), "sales_date": sales_date, "region": region_code})
        return imported_sales_list
    except FileNotFoundError:
        print(f"⚠️ ERROR: File '{filepath}' not found.")
        return []

def import_all_sales() -> list:
    sales_list = []
    try:
        with open(ALL_SALES, newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 3:
                    amount, sales_date, region = row
                    sales_list.append({"amount": float(amount), "sales_date": sales_date, "region": region})
        return sales_list
    except FileNotFoundError:
        print("⚠️ ERROR: No sales file found.")
        return []

def save_all_sales(sales_list, delimiter: str = ',') -> None:
    with open(ALL_SALES, "w", newline='') as file:
        writer = csv.writer(file, delimiter=delimiter)
        for sale in sales_list:
            writer.writerow([sale["amount"], sale["sales_date"], sale["region"]])
    print("✅ Sales data saved successfully.")

def display_title() -> None:
    print("SALES DATA IMPORTER\n")

def display_menu() -> None:
    print("COMMAND MENU")
    print("view   - View all sales")
    print("add1   - Add sales by typing sales, year, month, day, and region")
    print("add2   - Add sales by typing sales, date (YYYY-MM-DD), and region")
    print("import - Import sales from file")
    print("menu   - Show menu")
    print("exit   - Exit program")

def execute_command(sales_list) -> None:
    while True:
        try:
            action = input("\nPlease enter a command: ").strip().lower()
            if action == "exit":
                save_all_sales(sales_list)
                print("Exiting program...")
                break
            elif action == "import":
                filename = input("Enter name of file to import: ").strip()
                filepath = FILEPATH / filename
                if not filepath.exists():
                    print(f"⚠️ ERROR: File '{filename}' not found.")
                else:
                    imported_sales = import_sales(filepath)
                    if imported_sales:
                        sales_list.extend(imported_sales)
                        add_imported_file(filepath)
                        print(f"✅ Successfully imported {len(imported_sales)} records.")
            elif action == "menu":
                display_menu()
             else:
               print(f"⚠️ ERROR: File '{filepath}' not found.")
        return []

