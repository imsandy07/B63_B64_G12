from typing import Optional
from pathlib import Path
import re

VALID_REGIONS = {"w": "West", "m": "Mountain", "c": "Central", "e": "East"}
DATE_FORMAT = "%Y-%m-%d"
MIN_YEAR, MAX_YEAR = 2000, 2999

FILEPATH = Path(__file__).parent.parent / 'psc01_files'
NAMING_CONVENTION = r"sales_qn_\d{4}_[wmce]\.csv"

def input_amount() -> float:
    while True:
        try:
            entry = float(input("Enter amount: "))
            if entry > 0:
                return entry
            else:
                print("Amount must be greater than zero.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def input_int(entry_item: str, high: int, low: int = 1) -> int:
    while True:
        try:
            entry = int(input(f"Enter {entry_item} ({low}-{high}): "))
            if low <= entry <= high:
                return entry
            else:
                print(f"{entry_item.capitalize()} must be between {low} and {high}.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

def is_leap_year(year: int) -> bool:
    return (year % 400 == 0) or (year % 4 == 0 and year % 100 != 0)

def cal_max_day(year: int, month: int) -> int:
    if month == 2:
        return 29 if is_leap_year(year) else 28
    return 30 if month in [4, 6, 9, 11] else 31

def input_year() -> int:
    return input_int("year", MAX_YEAR, MIN_YEAR)

def input_month() -> int:
    return input_int("month", 12, 1)

def input_day(year: int, month: int) -> int:
    max_day = cal_max_day(year, month)
    return input_int("day", max_day, 1)

def input_region_code() -> Optional[str]:
    while True:
        region_code = input("Enter region code (w/m/c/e): ").strip().lower()
        if region_code in VALID_REGIONS:
            return region_code
        print("Invalid region code. Please enter one of: w, m, c, e.")

def from_input1():
    amount = input_amount()
    year = input_year()
    month = input_month()
    day = input_day(year, month)
    sales_date = f"{year}-{month:02}-{day:02}"
    region_code = input_region_code()
    return {"amount": amount, "sales_date": sales_date, "region": region_code}

def input_date() -> str:
    year = input_year()
    month = input_month()
    day = input_day(year, month)
    return f"{year}-{month:02}-{day:02}"

def from_input2():
    amount = input_amount()
    sales_date = input_date()
    region_code = input_region_code()
    return {"amount": amount, "sales_date": sales_date, "region": region_code}

def is_valid_filename_format(filename: str) -> bool:
    return bool(re.fullmatch(NAMING_CONVENTION, filename))

def get_region_code(sales_filename: str) -> str:
    return sales_filename[-5]

def is_valid_region(region_code: str) -> bool:
    return region_code in VALID_REGIONS

def get_region_name(region_code: str) -> str:
    return VALID_REGIONS.get(region_code, "Unknown")

def main():
    sales_list = []
    sales_data1 = from_input1()
    sales_data2 = from_input2()
    sales_list.append(sales_data1)
    sales_list.append(sales_data2)
    print("Sales Data 1:", sales_data1)
    print("Sales Data 2:", sales_data2)

if __name__ == "__main__":
    main()
