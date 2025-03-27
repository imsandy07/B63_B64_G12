from salesinput import cal_quarter, get_region_name, has_bad_data, from_input1, from_input2

def view_sales(sales_list: list) -> bool:
    if not sales_list:
        print("No sales to view.")
        return False
    print("\n  Date        Quarter   Region     Amount")
    total = 0
    for i, sale in enumerate(sales_list, 1):
        year, month, _ = map(int, sale["sales_date"].split("-"))
        quarter = cal_quarter(month)
        region = get_region_name(sale["region"])
        amount = sale["amount"]
        total += amount
        print(f"{i:>2}. {sale['sales_date']}     {quarter:<2}      {region:<9} {amount:>8.1f}")
    print("\nTOTAL".rjust(40), f"{total:.1f}")
    return True

def add_sales1(sales_list: list) -> None:
    data = from_input1()
    if not has_bad_data(data):
        sales_list.append(data)
        print(f"Sales for {data['sales_date']} is added.")

def add_sales2(sales_list: list) -> None:
    data = from_input2()
    if not has_bad_data(data):
        sales_list.append(data)
        print(f"Sales for {data['sales_date']} is added.")

def import_sales(sales_list: list) -> None:
    from salesfile import is_valid_filename_format, already_imported, import_sales as file_import, add_imported_file
    from pathlib import Path

    file_name = input("Enter name of file to import: ")
    if not is_valid_filename_format(file_name):
        print("Filename doesn't follow the expected format of sales_qn_yyyy_r.csv.")
        return

    file_path = Path("psc01_files") / file_name

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
