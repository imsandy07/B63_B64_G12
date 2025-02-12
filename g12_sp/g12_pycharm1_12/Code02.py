def get_integer(prompt, min_value, max_value):
    while True:
        user_input = input(prompt.ljust(20))
        try:
            value = int(user_input)
            if min_value <= value <= max_value:
                return value
            else:
                print(f"{prompt.strip()} must be between {min_value} and {max_value}.")
        except ValueError:
            print(f"{prompt.strip()} must be between {min_value} and {max_value}.")


year = get_integer("Year (2000-2999): ", 2000, 2999)
print(f"Year entered: {year}")

month = get_integer("Month (1-12): ", 1, 12)
print(f"Month entered: {month}")