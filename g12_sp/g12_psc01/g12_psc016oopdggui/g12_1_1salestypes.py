from typing import Optional, Self, Iterator
from datetime import date
from dataclasses import dataclass

@dataclass
class Region:
    code: str
    name: str

class Regions:
    def __init__(self, c_list: list, n_list: list) -> None:
        self._regions: list[Region] = [Region(c, n) for c, n in zip(c_list, n_list)]

    @classmethod
    def from_dict(cls, r_dict: dict = {"w": "West", "e": "East", "n": "North", "s": "South"}) -> Self:
        return cls(list(r_dict.keys()), list(r_dict.values()))

    @property
    def regions(self) -> list:
        return self._regions

    def __str__(self) -> str:
        return "\n".join([f"{r.code}: {r.name}" for r in self._regions])

    def __iter__(self):
        return iter(self._regions)

    def get_region_by_code(self, code: str) -> Optional[Region]:
        for region_obj in self._regions:
            if code == region_obj.code:
                return region_obj
        return None

    def get_region_code_list(self) -> list:
        return [region_obj.code for region_obj in self._regions]

    def is_valid_region_code(self, code: str) -> bool:
        return any(code == region_obj.code for region_obj in self._regions)

    def add_region(self, region: Region = None) -> None:
        if region:
            self._regions.append(region)

class Sales:
    DATE_FORMAT = "%Y-%m-%d"
    MIN_YEAR, MAX_YEAR = 2000, 2999

    def __init__(self, amount: float = 0.0, sales_date: date = None, region: Region = None, id: int = 0) -> None:
        self._salesdata = {
            "ID": id,
            "amount": amount,
            "sales_date": sales_date,
            "region": region
        }

    def __str__(self) -> str:
        return f"Sales(ID={self._salesdata['ID']}, amount={self._salesdata['amount']}, date={self._salesdata['sales_date']}, region={self._salesdata['region']})"

    def __getitem__(self, key):
        return self._salesdata[key]

    def __setitem__(self, key, value):
        self._salesdata[key] = value

    @property
    def has_bad_amount(self) -> bool:
        return self._salesdata["amount"] == "?"

    @property
    def has_bad_date(self) -> bool:
        return self._salesdata["sales_date"] == "?"

    @property
    def has_bad_data(self) -> bool:
        return self.has_bad_amount or self.has_bad_date

    @staticmethod
    def is_leap_year(year: int) -> bool:
        return (year % 400 == 0) or (year % 4 == 0 and year % 100 != 0)

    @staticmethod
    def cal_max_day(year: int, month: int) -> int:
        if Sales.is_leap_year(year) and month == 2:
            return 29
        elif month == 2:
            return 28
        elif month in (4, 6, 9, 11):
            return 30
        else:
            return 31

    @staticmethod
    def cal_quarter(month: int) -> int:
        if month in (1, 2, 3):
            return 1
        elif month in (4, 5, 6):
            return 2
        elif month in (7, 8, 9):
            return 3
        elif month in (10, 11, 12):
            return 4
        else:
            return 0

class SalesList:
    def __init__(self):
        self._sales_list: list[Sales] = []
        self._sales_id: int = 0

    @classmethod
    def from_list(cls, alist: list) -> Self:
        a_sales_list = cls()
        for sales in alist:
            a_sales_list.add(sales)
        return a_sales_list

    def __iter__(self) -> Iterator[Sales]:
        return iter(self._sales_list)

    @property
    def count(self) -> int:
        return len(self._sales_list)

    @property
    def sales_id(self) -> int:
        return self._sales_id

    @sales_id.setter
    def sales_id(self, id: int) -> None:
        self._sales_id = id

    def __getitem__(self, index) -> Sales:
        return self._sales_list[index]

    def add(self, sales_obj: Sales) -> None:
        self._sales_id += 1
        sales_obj["ID"] = self._sales_id
        self._sales_list.append(sales_obj)

    def concat(self, other_list: list[Sales] = None) -> None:
        for sales in other_list:
            self.add(sales)
