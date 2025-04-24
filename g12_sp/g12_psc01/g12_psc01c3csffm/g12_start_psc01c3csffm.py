from functools import singledispatch
from typing import Optional
from pathlib import Path  # pathlib is preferred to os.path.join
import csv

# Regions
VALID_REGIONS = {"w": "West", "m": "Mountain", "c": "Central", "e": "East"}
# Sales date
DATE_FORMAT = "%Y-%m-%d"
MIN_YEAR, MAX_YEAR = 2000, 2_999
# files
NAMING_CONVENTION = "sales_qn_yyyy_r.csv"
FILEPATH = Path(__file__).parent.parent.parent / 'psc01_files'
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


def input_day(year: int, month: int) -> int:
    max_day = cal_max_day(year, month)
    parameters = {"entry_item": "day", "high": max_day}
    # call input_int() using dictionary as keyword arguments
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


def get_region_code_from_filename(sales_filename: str) -> str:
    return sales_filename[sales_filename.rfind('.') - 1]


def already_imported(filepath_name: Path) -> bool:
    """
    Return True if the given filename is in the IMPORTED_FILES.
    Otherwise, False.
    """
    try:
        with open(FILEPATH / IMPORTED_FILES, 'r') as f:
            imported_files = [line.strip() for line in f.readlines()]
            return filepath_name.name in imported_files
    except FileNotFoundError:
        return False


def add_imported_file(filepath_name: Path) -> None:
    """Add the filepath_name into IMPORTED_FILES"""
    with open(FILEPATH / IMPORTED_FILES, 'a') as f:
        f.write(f"{filepath_name.name}\n")


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


def has_bad_amount(data: dict) -> bool:
    return data["amount"] == "?"  # or data["amount"] < 0


def has_bad_date(data: dict) -> bool:
    return data["sales_date"] == "?"  # or not isinstance(self.sales_date, date)


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
    bad_data_flag = False
    if len(sales_list) == 0:  # sales_list could be [] or None
        print("No sales to view.")
    else:  # not empty
        col1_w, col2_w, col3_w, col4_w, col5_w = 5, 15, 15, 15, 15  # column width
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
    """
     Get the sales data from_input1() which
     asks user to enter sales amount and date by calling following functions
       - input_amount,
       - input_year, input_month, input_day
       - input_region_code
     Add sales data to the sales_list
     Notify the user by displaying a message on the console_
    """
    # get the sales data from_input1()
    sales_list.append(data := from_input1())
    print(f"Sales for {data['sales_date']} is added.")


def add_sales2(sales_list: list) -> None:
    """
     Get the sales data from_input2() which
     asks user to enter sales amount and date by calling following functions
       - input_amount,
       - input_date,
       - input_region_code
     Add sales data to the sales_list
     Notify the user by displaying a message on the console_
    """
    # get the sales data from_input2()
    sales_list.append(data := from_input2())
    print(f"Sales for {data['sales_date']} is added.")


def import_all_sales() -> list:
    """
    Read each row of sales data from the file ALL_SALES into a dictionary
    data = {"amount": amount,
            "sales_date": sales_date,
            "region": region_code}
    Return a list of dictionaries.
    """
    sales_list = []
    try:
        with open(FILEPATH / ALL_SALES, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for line in reader:
                if len(line) > 0:
                    amount_sales_date = [line[0], line[1]]
                    region_code = line[2]
                    correct_data_types(amount_sales_date)
                    amount, sales_date = amount_sales_date[0], amount_sales_date[1]
                    data = {
                        "amount": amount,
                        "sales_date": sales_date,
                        "region": region_code,
                    }
                    sales_list.append(data)
    except FileNotFoundError:
        pass
    return sales_list


@import_sales.register
def _(sales_list: list) -> None:
    filename = input("Enter name of file to import: ")
    filepath_name = FILEPATH / filename
    if not is_valid_filename_format(filename):
        print(f"Filename '{filename}' doesn't follow the expected",
              f"format of {NAMING_CONVENTION}.")
    elif not is_valid_region(get_region_code_from_filename(filename)):
        print(f"Filename '{filename}' doesn't include one of",
              f"the following region codes: {list(VALID_REGIONS.keys())}.")
    elif already_imported(filepath_name):
        filename = filename.replace("\n", "")
        print(f"File '{filename}' has already been imported.")
    else:
        imported_sales_list = import_sales(filepath_name)
        if imported_sales_list is None:
            print(f"Fail to import sales from '{filename}'.")
        else:
            bad_data_flag = view_sales(imported_sales_list)
            if bad_data_flag:
                print(f"File '{filename}' contains bad data.\n"
                      "Please correct the data in the file and try again.")
            elif len(imported_sales_list) > 0:
                sales_list.extend(imported_sales_list)
                print("Imported sales added to list.")
                add_imported_file(filepath_name)


def save_all_sales(sales_list, delimiter: str = ',') -> None:
    """
    Convert each sales data dictionary in the sales_list into a list
    Save the converted sales list which now is a list of lists into the file ALL_SALES.
    """
    with open(FILEPATH / ALL_SALES, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=delimiter)
        for sale in sales_list:
            writer.writerow([sale['amount'], sale['sales_date'], sale['region']])


def initialize_content_of_files(delimiter: str = ',') -> None:
    """
    Make sure the SALES_ALL contains the same content of SALES_ALL_COPY.
    Make sure the IMPORTED_FILES is empty
    """
    # Copy content from ALL_SALES_COPY to ALL_SALES
    try:
        with open(FILEPATH / ALL_SALES_COPY, 'r') as src, \
                open(FILEPATH / ALL_SALES, 'w') as dst:
            dst.write(src.read())
    except FileNotFoundError:
        pass

    # Clear IMPORTED_FILES
    try:
        with open(FILEPATH / IMPORTED_FILES, 'w') as f:
            f.write('')
    except FileNotFoundError:
        pass


# -----------------Console Menu (Presentation) -----------------------
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


def execute_command() -> None:
    # initial content of the files all_sales.csv and imported_files.txt
    initialize_content_of_files()
    # initial content of sales_list
    sales_list = import_all_sales()  # when application is started

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
            print("Saved sales records.")
            break
        if action == "import":
            commands[action](sales_list)
        elif action in ("add1", "add2"):
            commands[action](sales_list)
        elif action == "view":
            commands[action](sales_list)
        elif action == "menu":
            commands[action]()
        else:
            print("Invalid command. Please try again.\n")
            display_menu()


# --------------- Main -----------------
# main using console menu
def main():
    display_title()
    display_menu()
    execute_command()
    print("Bye!")


if __name__ == '__main__':
    main()
from functools import singledispatch
from typing import Optional
from pathlib import Path  # pathlib is preferred to os.path.join
import csv

# Regions
VALID_REGIONS = {"w": "West", "m": "Mountain", "c": "Central", "e": "East"}
# Sales date
DATE_FORMAT = "%Y-%m-%d"
MIN_YEAR, MAX_YEAR = 2000, 2_999
# files
NAMING_CONVENTION = "sales_qn_yyyy_r.csv"
FILEPATH = Path(__file__).parent.parent.parent / 'psc01_files'
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


def input_day(year: int, month: int) -> int:
    max_day = cal_max_day(year, month)
    parameters = {"entry_item": "day", "high": max_day}
    # call input_int() using dictionary as keyword arguments
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


def get_region_code_from_filename(sales_filename: str) -> str:
    return sales_filename[sales_filename.rfind('.') - 1]


def already_imported(filepath_name: Path) -> bool:
    """
    Return True if the given filename is in the IMPORTED_FILES.
    Otherwise, False.
    """
    try:
        with open(FILEPATH / IMPORTED_FILES, 'r') as f:
            imported_files = [line.strip() for line in f.readlines()]
            return filepath_name.name in imported_files
    except FileNotFoundError:
        return False


def add_imported_file(filepath_name: Path) -> None:
    """Add the filepath_name into IMPORTED_FILES"""
    with open(FILEPATH / IMPORTED_FILES, 'a') as f:
        f.write(f"{filepath_name.name}\n")


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


def has_bad_amount(data: dict) -> bool:
    return data["amount"] == "?"  # or data["amount"] < 0


def has_bad_date(data: dict) -> bool:
    return data["sales_date"] == "?"  # or not isinstance(self.sales_date, date)


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
    bad_data_flag = False
    if len(sales_list) == 0:  # sales_list could be [] or None
        print("No sales to view.")
    else:  # not empty
        col1_w, col2_w, col3_w, col4_w, col5_w = 5, 15, 15, 15, 15  # column width
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
    """
     Get the sales data from_input1() which
     asks user to enter sales amount and date by calling following functions
       - input_amount,
       - input_year, input_month, input_day
       - input_region_code
     Add sales data to the sales_list
     Notify the user by displaying a message on the console_
    """
    # get the sales data from_input1()
    sales_list.append(data := from_input1())
    print(f"Sales for {data['sales_date']} is added.")


def add_sales2(sales_list: list) -> None:
    """
     Get the sales data from_input2() which
     asks user to enter sales amount and date by calling following functions
       - input_amount,
       - input_date,
       - input_region_code
     Add sales data to the sales_list
     Notify the user by displaying a message on the console_
    """
    # get the sales data from_input2()
    sales_list.append(data := from_input2())
    print(f"Sales for {data['sales_date']} is added.")


def import_all_sales() -> list:
    """
    Read each row of sales data from the file ALL_SALES into a dictionary
    data = {"amount": amount,
            "sales_date": sales_date,
            "region": region_code}
    Return a list of dictionaries.
    """
    sales_list = []
    try:
        with open(FILEPATH / ALL_SALES, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for line in reader:
                if len(line) > 0:
                    amount_sales_date = [line[0], line[1]]
                    region_code = line[2]
                    correct_data_types(amount_sales_date)
                    amount, sales_date = amount_sales_date[0], amount_sales_date[1]
                    data = {
                        "amount": amount,
                        "sales_date": sales_date,
                        "region": region_code,
                    }
                    sales_list.append(data)
    except FileNotFoundError:
        pass
    return sales_list


@import_sales.register
def _(sales_list: list) -> None:
    filename = input("Enter name of file to import: ")
    filepath_name = FILEPATH / filename
    if not is_valid_filename_format(filename):
        print(f"Filename '{filename}' doesn't follow the expected",
              f"format of {NAMING_CONVENTION}.")
    elif not is_valid_region(get_region_code_from_filename(filename)):
        print(f"Filename '{filename}' doesn't include one of",
              f"the following region codes: {list(VALID_REGIONS.keys())}.")
    elif already_imported(filepath_name):
        filename = filename.replace("\n", "")
        print(f"File '{filename}' has already been imported.")
    else:
        imported_sales_list = import_sales(filepath_name)
        if imported_sales_list is None:
            print(f"Fail to import sales from '{filename}'.")
        else:
            bad_data_flag = view_sales(imported_sales_list)
            if bad_data_flag:
                print(f"File '{filename}' contains bad data.\n"
                      "Please correct the data in the file and try again.")
            elif len(imported_sales_list) > 0:
                sales_list.extend(imported_sales_list)
                print("Imported sales added to list.")
                add_imported_file(filepath_name)


def save_all_sales(sales_list, delimiter: str = ',') -> None:
    """
    Convert each sales data dictionary in the sales_list into a list
    Save the converted sales list which now is a list of lists into the file ALL_SALES.
    """
    with open(FILEPATH / ALL_SALES, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=delimiter)
        for sale in sales_list:
            writer.writerow([sale['amount'], sale['sales_date'], sale['region']])


def initialize_content_of_files(delimiter: str = ',') -> None:
    """
    Make sure the SALES_ALL contains the same content of SALES_ALL_COPY.
    Make sure the IMPORTED_FILES is empty
    """
    # Copy content from ALL_SALES_COPY to ALL_SALES
    try:
        with open(FILEPATH / ALL_SALES_COPY, 'r') as src, \
                open(FILEPATH / ALL_SALES, 'w') as dst:
            dst.write(src.read())
    except FileNotFoundError:
        pass

    # Clear IMPORTED_FILES
    try:
        with open(FILEPATH / IMPORTED_FILES, 'w') as f:
            f.write('')
    except FileNotFoundError:
        pass


# -----------------Console Menu (Presentation) -----------------------
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


def execute_command() -> None:
    # initial content of the files all_sales.csv and imported_files.txt
    initialize_content_of_files()
    # initial content of sales_list
    sales_list = import_all_sales()  # when application is started

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
            print("Saved sales records.")
            break
        if action == "import":
            commands[action](sales_list)
        elif action in ("add1", "add2"):
            commands[action](sales_list)
        elif action == "view":
            commands[action](sales_list)
        elif action == "menu":
            commands[action]()
        else:
            print("Invalid command. Please try again.\n")
            display_menu()

from functools import singledispatch
from typing import Optional
from pathlib import Path  # pathlib is preferred to os.path.join
import csv

# Regions
VALID_REGIONS = {"w": "West", "m": "Mountain", "c": "Central", "e": "East"}
# Sales date
DATE_FORMAT = "%Y-%m-%d"
MIN_YEAR, MAX_YEAR = 2000, 2_999
# files
NAMING_CONVENTION = "sales_qn_yyyy_r.csv"
FILEPATH = Path(__file__).parent.parent.parent / 'psc01_files'
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


def input_day(year: int, month: int) -> int:
    max_day = cal_max_day(year, month)
    parameters = {"entry_item": "day", "high": max_day}
    # call input_int() using dictionary as keyword arguments
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


def get_region_code_from_filename(sales_filename: str) -> str:
    return sales_filename[sales_filename.rfind('.') - 1]


def already_imported(filepath_name: Path) -> bool:
    """
    Return True if the given filename is in the IMPORTED_FILES.
    Otherwise, False.
    """
    try:
        with open(FILEPATH / IMPORTED_FILES, 'r') as f:
            imported_files = [line.strip() for line in f.readlines()]
            return filepath_name.name in imported_files
    except FileNotFoundError:
        return False


def add_imported_file(filepath_name: Path) -> None:
    """Add the filepath_name into IMPORTED_FILES"""
    with open(FILEPATH / IMPORTED_FILES, 'a') as f:
        f.write(f"{filepath_name.name}\n")


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


def has_bad_amount(data: dict) -> bool:
    return data["amount"] == "?"  # or data["amount"] < 0


def has_bad_date(data: dict) -> bool:
    return data["sales_date"] == "?"  # or not isinstance(self.sales_date, date)


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
    bad_data_flag = False
    if len(sales_list) == 0:  # sales_list could be [] or None
        print("No sales to view.")
    else:  # not empty
        col1_w, col2_w, col3_w, col4_w, col5_w = 5, 15, 15, 15, 15  # column width
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
    """
     Get the sales data from_input1() which
     asks user to enter sales amount and date by calling following functions
       - input_amount,
       - input_year, input_month, input_day
       - input_region_code
     Add sales data to the sales_list
     Notify the user by displaying a message on the console_
    """
    # get the sales data from_input1()
    sales_list.append(data := from_input1())
    print(f"Sales for {data['sales_date']} is added.")


def add_sales2(sales_list: list) -> None:
    """
     Get the sales data from_input2() which
     asks user to enter sales amount and date by calling following functions
       - input_amount,
       - input_date,
       - input_region_code
     Add sales data to the sales_list
     Notify the user by displaying a message on the console_
    """
    # get the sales data from_input2()
    sales_list.append(data := from_input2())
    print(f"Sales for {data['sales_date']} is added.")


def import_all_sales() -> list:
    """
    Read each row of sales data from the file ALL_SALES into a dictionary
    data = {"amount": amount,
            "sales_date": sales_date,
            "region": region_code}
    Return a list of dictionaries.
    """
    sales_list = []
    try:
        with open(FILEPATH / ALL_SALES, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for line in reader:
                if len(line) > 0:
                    amount_sales_date = [line[0], line[1]]
                    region_code = line[2]
                    correct_data_types(amount_sales_date)
                    amount, sales_date = amount_sales_date[0], amount_sales_date[1]
                    data = {
                        "amount": amount,
                        "sales_date": sales_date,
                        "region": region_code,
                    }
                    sales_list.append(data)
    except FileNotFoundError:
        pass
    return sales_list


@import_sales.register
def _(sales_list: list) -> None:
    filename = input("Enter name of file to import: ")
    filepath_name = FILEPATH / filename
    if not is_valid_filename_format(filename):
        print(f"Filename '{filename}' doesn't follow the expected",
              f"format of {NAMING_CONVENTION}.")
    elif not is_valid_region(get_region_code_from_filename(filename)):
        print(f"Filename '{filename}' doesn't include one of",
              f"the following region codes: {list(VALID_REGIONS.keys())}.")
    elif already_imported(filepath_name):
        filename = filename.replace("\n", "")
        print(f"File '{filename}' has already been imported.")
    else:
        imported_sales_list = import_sales(filepath_name)
        if imported_sales_list is None:
            print(f"Fail to import sales from '{filename}'.")
        else:
            bad_data_flag = view_sales(imported_sales_list)
            if bad_data_flag:
                print(f"File '{filename}' contains bad data.\n"
                      "Please correct the data in the file and try again.")
            elif len(imported_sales_list) > 0:
                sales_list.extend(imported_sales_list)
                print("Imported sales added to list.")
                add_imported_file(filepath_name)


def save_all_sales(sales_list, delimiter: str = ',') -> None:
    """
    Convert each sales data dictionary in the sales_list into a list
    Save the converted sales list which now is a list of lists into the file ALL_SALES.
    """
    with open(FILEPATH / ALL_SALES, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=delimiter)
        for sale in sales_list:
            writer.writerow([sale['amount'], sale['sales_date'], sale['region']])


def initialize_content_of_files(delimiter: str = ',') -> None:
    """
    Make sure the SALES_ALL contains the same content of SALES_ALL_COPY.
    Make sure the IMPORTED_FILES is empty
    """
    # Copy content from ALL_SALES_COPY to ALL_SALES
    try:
        with open(FILEPATH / ALL_SALES_COPY, 'r') as src, \
                open(FILEPATH / ALL_SALES, 'w') as dst:
            dst.write(src.read())
    except FileNotFoundError:
        pass

    # Clear IMPORTED_FILES
    try:
        with open(FILEPATH / IMPORTED_FILES, 'w') as f:
            f.write('')
    except FileNotFoundError:
        pass


# -----------------Console Menu (Presentation) -----------------------
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


def execute_command() -> None:
    # initial content of the files all_sales.csv and imported_files.txt
    initialize_content_of_files()
    # initial content of sales_list
    sales_list = import_all_sales()  # when application is started

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
            print("Saved sales records.")
            break
        if action == "import":
            commands[action](sales_list)
        elif action in ("add1", "add2"):
            commands[action](sales_list)
        elif action == "view":
            commands[action](sales_list)
        elif action == "menu":
            commands[action]()
        else:
            print("Invalid command. Please try again.\n")
            display_menu()


# --------------- Main -----------------
# main using console menu
def main():
    display_title()
    display_menu()
    execute_command()
    print("Bye!")


if __name__ == '__main__':
    main()
# --------------- Main -----------------
# main using console menu
def main():
    display_title()
    display_menu()
    execute_command()
    print("Bye!")


if __name__ == '__main__':
    main()