from typing import Optional
import calendar

def input_amount() -> float:
    while True:
        try:
            amount = float(input("Amount:             "))
            if amount > 0:
                return amount
            else:
                print("Amount must be greater than zero.")
        except ValueError:
            print("Invalid number. Please try again.")

def input_int(entry_item: str, high: int, low: int = 1, fmt_width: int = 20) -> int:
    while True:
        try:
            prompt = f"{entry_item.capitalize()} ({low}-{high}):"
            while True:
                entry = int(input(f"{prompt:{fmt_width}}"))
                if low <= entry <= high:
                    return entry
                else:
                    print(f"{entry_item.capitalize()} must be between {low} and {high}.")
        except ValueError:
            print(f"Invalid {entry_item}. Please enter an integer.")

def input_year() -> int:
    return input_int("Year", 2999, 2000)

def input_month() -> int:
    return input_int("Month", 12, 1)

def input_day(year: int, month: int) -> int:
    max_day = cal_max_day(year, month)
    return input_int("Day", max_day, 1)

def input_date() -> str:
    while True:
        entry = input(f"{'Date (yyyy-mm-dd):':20}").strip()
        if len(entry) == 10 and entry[4] == '-' and entry[7] == '-' \
                and entry[:4].isdigit() and entry[5:7].isdigit() \
                and entry[8:].isdigit():
            yyyy, mm, dd = int(entry[:4]), int(entry[5:7]), int(entry[8:])
            if (1 <= mm <= 12) and (1 <= dd <= cal_max_day(yyyy, mm)):
                if 2000 <= yyyy <= 2999:
                    return entry
                else:
                    print(f"Year of the date must be between 2000 and 2999.")
            else:
                print(f"{entry} is not in a valid date format.")
        else:
            print(f"{entry} is not in a valid date format.")

def input_region_code() -> Optional[str]:
    valid_codes = ('w', 'm', 'c', 'e')
    while True:
        region = input("Region ('w', 'm', 'c', 'e'):").lower()  # Ensure the prompt format is correct
        if region in valid_codes:
            return region
        else:
            print(f"Region must be one of the following: {valid_codes}.")

def is_leap_year(year: int) -> bool:
    return calendar.isleap(year)

def cal_max_day(year: int, month: int) -> int:
    return calendar.monthrange(year, month)[1]

def cal_quarter(month: int) -> int:
    return (month - 1) // 3 + 1

def get_region_name(region_code: str) -> str:
    mapping = {'w': 'West', 'm': 'Mountain', 'c': 'Central', 'e': 'East'}
    return mapping.get(region_code, "Unknown")

def is_valid_region(region_code: str) -> bool:
    return region_code in {'w', 'm', 'c', 'e'}

def has_bad_amount(data: dict) -> bool:
    return not isinstance(data.get("amount"), (int, float)) or data["amount"] <= 0

def has_bad_date(data: dict) -> bool:
    try:
        year, month, day = map(int, data.get("sales_date").split("-"))
        return day > cal_max_day(year, month)
    except:
        return True

def has_bad_data(data: dict) -> bool:
    return has_bad_amount(data) or has_bad_date(data)

def from_input1() -> dict:
    amount = input_amount()
    year = input_year()
    month = input_month()
    day = input_day(year, month)
    date = f"{year:04d}-{month:02d}-{day:02d}"
    region = input_region_code()
    return {"amount": amount, "sales_date": date, "region": region}

def from_input2() -> dict:
    amount = input_amount()
    date = input_date()
    region = input_region_code()
    return {"amount": amount, "sales_date": date, "region": region}
