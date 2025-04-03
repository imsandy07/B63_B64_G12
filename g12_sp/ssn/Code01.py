def get_sales_amount():
    while True:
        user_input = input("Amount: ".ljust(20))
        try:
            amount = float(user_input)
            if amount > 0:
                return amount
            else:
                print("Amount must be greater than zero.")
        except ValueError:
            print("Amount must be greater than zero.")

sales_amount = get_sales_amount()
print(f"Sales amount entered: {sales_amount}")