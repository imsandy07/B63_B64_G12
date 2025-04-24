from typing import Optional
from pathlib import Path
import csv
from functools import singledispatch

# Regions
VALID_REGIONS = {"w": "West", "m": "Mountain", "c": "Central", "e": "East"}

# Sales date
DATE_FORMAT = "%Y-%m-%d"
MIN_YEAR, MAX_YEAR = 2000, 2999

# Files
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
        else:
            print("Amount must be greater than zero.")


def input_int(entry_item: str, high: int, low: int = 1, fmt_width: int = 20) -> int:
    prompt = f"{entry_item.capitalize()} ({low}-{high}):"
    while True:
        entry = int(input(f"{prompt:{fmt_width}}"))
        if low <= entry <= high:
            return entry
        else:
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
    elif month == 2:
        return 28
    elif month in (4, 6, 9, 11):
        return 30
    else:
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
                else:
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
    """Return True if the filename is in the IMPORTED_FILES. Otherwise, False."""
    pass


def add_imported_file(filepath_name: Path) -> None:
    """Add the filepath_name into IMPORTED_FILES"""
    pass


@singledispatch
def import_sales(filepath_name: Path, delimiter: str = ',') -> list:
    with open(filepath_name, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=delimiter)
        filename = filepath_name.name
        region_code = filename[filename.rfind('.') - 1]
        imported_sales_list = []
        for amount_sales_date in reader:
            amount, sales_date = amount_sales_date[0], amount_sales_date[1]
            data = {"amount": amount, "sales_date": sales_date, "region": region_code}
            imported_sales_list.append(data)
        return imported_sales_list


def view_sales(sales_list: list) -> bool:
    """Display sales data"""
    if not sales_list:
        print("No sales to view.")
        return False
    print("\nSALES DATA")
    print(f"{'Date':<15} {'Region':<10} {'Amount':>10}")
    print("-" * 40)
    for sales in sales_list:
        print(f"{sales['sales_date']:<15} {sales['region']:<10} {sales['amount']:>10.2f}")
    return True


def add_sales1(sales_list: list) -> None:
    sales_list.append(data := from_input1())
    print(f"Sales for {data['sales_date']} is added.")


def add_sales2(sales_list: list) -> None:
    sales_list.append(data := from_input2())
    print(f"Sales for {data['sales_date']} is added.")


def initialize_content_of_files(delimiter: str = ',') -> None:
    """Initialize sales data files"""
    pass


def import_all_sales() -> list:
    """Import sales data"""
    pass


def save_all_sales(sales_list, delimiter: str = ',') -> None:
    """Save all sales data"""
    pass


# Console Menu
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
    commands = {
        "import": import_sales,
        "add1": add_sales1,
        "add2": add_sales2,
        "view": view_sales,
        "menu": display_menu,  # ❌ FIX: Don't pass sales_list to display_menu()
    }
    while True:
        try:
            action = input("\nPlease enter a command: ").strip().lower()
            if action == "exit":
                save_all_sales(sales_list)
                print("Exiting program...")
                break
            elif action in commands:
                if action == "menu":
                    commands[action]()  # ✅ FIX: Call display_menu() with no arguments
                else:
                    commands[action](sales_list)  # Keep arguments for other functions
            else:
                print("Invalid command. Please try again.\n")
                display_menu()  # ✅ Call display_menu() correctly
        except KeyboardInterrupt:
            print("\n⚠️ KeyboardInterrupt detected. Exiting safely.")
            break


# Main Entry
def main():
    display_title()
    display_menu()
    sales_list = []
    execute_command(sales_list)
    print("Bye!")


if __name__ == '__main__':
    main()