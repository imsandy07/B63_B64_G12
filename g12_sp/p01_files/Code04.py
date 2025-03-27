import calendar

def get_valid_input(prompt, min_val, max_val):
    while True:
        user_input = input(prompt.ljust(20))  # Ensure 20-character prompt
        try:
            value = int(user_input)
            if min_val <= value <= max_val:
                return value
            else:
                print(f"{prompt.strip()} must be between {min_val} and {max_val}.")
        except ValueError:
            print(f"{prompt.strip()} must be a valid integer.")

def last_day_of_month(year, month):
    return calendar.monthrange(year, month)[1]

year = get_valid_input("Year (1-9999): ", 1, 9999)
month = get_valid_input("Month (1-12): ", 1, 12)
last_day = last_day_of_month(year, month)
print(f"Last day of {month}/{year}: {last_day}")