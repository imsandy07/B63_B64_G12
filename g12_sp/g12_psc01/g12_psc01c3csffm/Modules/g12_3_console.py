from g07_2_salesmanager import view_sales, add_sales1, add_sales2, import_sales, import_all_sales, save_all_sales

def display_title() -> None:
    print("SALES DATA IMPORTER")

def display_menu() -> None:
    print("""
COMMAND MENU
view   - View all sales
add1   - Add sales by typing sales, year, month, day, and region
add2   - Add sales by typing sales, date (YYYY-MM-DD), and region
import - Import sales from file
menu   - Show menu
exit   - Exit program
""")

def execute_command() -> None:
    sales_list = import_all_sales()
    display_title()
    display_menu()

    while True:
        command = input("Please enter a command: ").lower()
        if command == "view":
            view_sales(sales_list)
        elif command == "add1":
            add_sales1(sales_list)
        elif command == "add2":
            add_sales2(sales_list)
        elif command == "import":
            import_sales(sales_list)
        elif command == "menu":
            display_menu()
        elif command == "exit":
            save_all_sales(sales_list)
            print("Saved sales records.\nBye!")
            break
        else:
            print("    Invalid command. Please try again.")
            display_menu()  # Assuming you have a function to show the command menu