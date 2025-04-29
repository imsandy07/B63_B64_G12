from typing import Optional
import calendar
...
def from_input2() -> dict:
    amount = input_amount()
    date = input_date()
    region = input_region_code()
    return {"amount": amount, "sales_date": date, "region": region}