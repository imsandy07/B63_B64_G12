from typing import Optional
from pathlib import Path
import csv
from functools import singledispatch

# Regions
VALID_REGIONS = {"w": "West", "m": "Mountain", "c": "Central", "e": "East"}
# Sales date
DATE_FORMAT = "%Y-%m-%d"
MIN_YEAR, MAX_YEAR = 2000, 2_999
# files
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
            print(f"Amount must be greater than zero.")


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
    if is_leap_year(year) and month == 2:  # short-circuit
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
                and entry[:4].isdigit() and entry[5:7].isdigit() \
                and entry[8:].isdigit():
            yyyy, mm, dd = int(entry[:4]), int(entry[5:7]), int(entry[8:])
            if (1 <= mm <= 12) and (1 <= dd <= cal_max_day(yyyy, mm)):
                if MIN_YEAR <= yyyy <= MAX_YEAR:
                    return entry
                else:
                    print(f"Year of the date must be between {MIN_YEAR} and {MAX_YEAR}.")
            else:
                print(f"{entry} is not in a valid date format.")
        else:
            print(f"{entry} is not in a valid date format.")


def input_region_code() -> Optional[str]:
    while True:
        fmt = 20
        valid_codes = tuple(VALID_REGIONS.keys())
        prompt = f"{f'Region {valid_codes}:':{fmt}}"
        code = input(prompt)
        if valid_codes.count(code) == 1:
            return code
        else:
            print(f"Region must be one of the following: {valid_codes}.")


def from_input1() -> dict:
    amount = input_amount()
    year = input_year()
    month = input_month()
    day = input_day(year, month)
    sales_date = f"{year}-{str(month).zfill(2)}-{day:02}"
    region_code = input_region_code()
    return {"amount": amount,
            "sales_date": sales_date,
            "region": region_code,
            }


def from_input2() -> dict:
    amount = input_amount()
    sales_date = input_date()
    region_code = input_region_code()
    return {"amount": amount,
            "sales_date": sales_date,
            "region": region_code,
            }


def is_valid_filename_format(filename: str) -> bool:
    if len(filename) == len(NAMING_CONVENTION) and \
            filename[:7] == NAMING_CONVENTION[:7] and \
            filename[8] == NAMING_CONVENTION[8] and \
            filename[13] == NAMING_CONVENTION[-6] and \
            filename[-4:] == NAMING_CONVENTION[-4:]:
        return True
    else:
        return False


def get_region_code(sales_filename: str) -> str:
    return sales_filename[sales_filename.rfind('.') - 1]


def already_imported(filepath_name: Path) -> bool:
    """
    Return True if the filename is in the IMPORTED_FILES.
    Otherwise, False.
    """
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
            correct_data_types(amount_sales_date)
            amount, sales_date = amount_sales_date[0], amount_sales_date[1]
            data = {"amount": amount,
                    "sales_date": sales_date,
                    "region": region_code,
                    }
            imported_sales_list.append(data)
        return imported_sales_list  # within with statement


def cal_quarter(month: int) -> int:
    if month in (1, 2, 3):
        quarter = 1
    elif month in (4, 5, 6):
        quarter = 2
    elif month in (7, 8, 9):
        quarter = 3
    elif month in (10, 11, 12):
        quarter = 4
    else:
        quarter = 0
    return quarter


def get_region_name(region_code: str) -> str:
    return VALID_REGIONS[region_code]


def is_valid_region(region_code: str) -> bool:
    return tuple(VALID_REGIONS.keys()).count(region_code) == 1


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


def has_bad_amount(data: dict) -> bool:
    return data["amount"] == "?"


def has_bad_date(data: dict) -> bool:
    return data["sales_date"] == "?"


def has_bad_data(data: dict) -> bool:
    return has_bad_amount(data) or has_bad_date(data)


def view_sales(sales_list: list) -> bool:
    """
    Display "No sles to view" if there is no sales data in the sales_list.
    Otherwise, calculate the total amount and display sales data and the
    total amount on the console.
    """
    col1_w, col2_w, col3_w, col4_w, col5_w = 5, 15, 15, 15, 15  # column width
    # complete the code
    bad_data_flag = False
    if len(sales_list) == 0:  # sales_list could be [] or None
        print("No sales to view.")
    else:  # not empty
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
                num = f"{idx}.*"  # add period and asterisk
            else:
                num = f"{idx}."  # add period only

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
    sales_list.append(data := from_input1())
    print(f"Sales for {data["sales_date"]} is added.")


def add_sales2(sales_list: list) -> None:
    sales_list.append(data := from_input2())
    print(f"Sales for {data["sales_date"]} is added.")


def initialize_content_of_files(delimiter: str = ',') -> None:
    """Copy the content of ALL_SALES_COPY to ALL_SALES.
    (ALL_SALES existing content will be over writen by the content
    of ALL_SALES_COPY)
    Remove the content of IMPORTED_FILES.
     """
    pass


def import_all_sales() -> list:
    """
    Read each row of sales data from the file ALL_SALES into a dictionary
    data = {"amount": amount,
            "sales_date": sales_date,
            "region": region_code}
    Return a list of dictionaries.
    """
    pass


@import_sales.register
def _(sales_list: list) -> None:  # def import_sales(sales_list: list) -> None:
    # get filename from user
    filename = input("Enter name of file to import: ")
    filepath_name = FILEPATH / filename
    # check if filename is valid
    if not is_valid_filename_format(filename):
        print(f"Filename '{filename}' doesn't follow the expected",
              f"format of '{NAMING_CONVENTION}.")
    # check if region code (the 5th character from end) is valid.
    elif not is_valid_region(get_region_code(filename)):
        print(f"Filename '{filename}' doesn't include one of",
              f"the following region codes: {list(VALID_REGIONS.keys())}.")
    # check if file has already been imported
    elif already_imported(filepath_name):
        filename = filename.replace("\n", "")  # remove new line character
        print(f"File '{filename}' has already been imported.")
    else:
        # import sales data from file to a list
        imported_sales_list = import_sales(filepath_name)
        # check if import succeeded (including []). imported_sales_list could be None or []
        if imported_sales_list is None:  # only handle imported_sales_list is None here.
            print(f"Fail to import sales from '{filename}'.")
        else:
            # display imported sales, and also return if there is bad data.
            bad_data_flag = view_sales(imported_sales_list)
            if bad_data_flag:
                print(f"File '{filename}' contains bad data.\n"
                      "Please correct the data in the file and try again.")
            elif len(imported_sales_list) > 0:  # handle imported_sales_list is not [] here.
                sales_list.extend(imported_sales_list)
                print("Imported sales added to list.")
                add_imported_file(filepath_name)


def save_all_sales(sales_list, delimiter: str = ',') -> None:
    """
    Convert each sales data dictionary in the sales_list into a list
    Save the converted sales list which now is a list of lists into the file ALL_SALES.
    """
    # convert the list of dictionaries to a list of lists, using comprehension

    # Save the converted sales list which now is a list of lists into the file ALL_SALES.
    pass


# -----------------Console Menu -----------------------
def display_title() -> None:
    print("SALES DATA IMPORTER\n")


def display_menu() -> None:
    cmd_format = "6"  # ^ center, < is the default for str.
    print("COMMAND MENU",
          f"{'view':{cmd_format}} - View all sales",
          f"{'add1':{cmd_format}} - Add sales by typing sales, year, month, day, and region",
          f"{'add2':{cmd_format}} - Add sales by typing sales, date (YYYY-MM-DD), and region",
          f"{'import':{cmd_format}} - Import sales from file",
          f"{'menu':{cmd_format}} - Show menu",
          f"{'exit':{cmd_format}} - Exit program", sep='\n', end='\n')


def execute_command(sales_list) -> None:
    commands = {"import": import_sales,
                "add1": add_sales1,
                "add2": add_sales2,
                "view": view_sales,
                "menu": display_menu,
                }
    while True:
        action = input("\nPlease enter a command: ").strip().lower()
        if action == "exit":
            save_all_sales(sales_list)
            break
        if action in ("import", "add1", "add2"):
            commands[action](sales_list)
        elif action == 'view':
            if sales_list == []:  # when application is started
                # initial content of the files all_sales.csv and imported_files.txt
                initialize_content_of_files()
                # initial content of sales_list
                sales_list = import_all_sales()
            commands[action](sales_list)
        elif action == "menu":
            commands[action]()
        else:
            print("Invalid command. Please try again.\n")
            display_menu()


# --------------- Main Entry
# main using console menu
# def main():
#     display_title()
#     display_menu()
#
#     sales_list = []
#     execute_command(sales_list)
#
#     print("Bye!")


# --------------- Testing
def main():
    pass


if __name__ == '__main__':
    main()