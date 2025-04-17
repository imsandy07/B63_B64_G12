from g12_1_1filetypes import FileType
from g12_1_1salestypes import Sales, Regions, Region

from typing import Optional
from pathlib import Path
from datetime import date

import sqlite3

class SQLiteDBAccess:

    def __init__(self, db_name: str='', db_path: Path=None):
        self._valid_regions = Regions.from_dict()
        fname: str = db_name if db_name else 'sales_db.sqlite'
        fpath: Path = db_path if db_path else Path(__file__).parent.parent / 'psc01_db'
        self._sqlite_sales_db = FileType(fname, fpath)

    def __connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self._sqlite_sales_db.dirpath / self._sqlite_sales_db.filename)

    def retrieve_sales_by_date_region(self, sales_date: date, region_code: str) -> Optional[Sales]:
        con = self.__connect()
        cur = con.cursor()
        query = '''SELECT id, amount, salesDate, region_code FROM Sales WHERE salesDate = ? AND region_code = ?'''
        cur.execute(query, (sales_date.isoformat(), region_code))
        row = cur.fetchone()
        con.close()

        if row:
            region = self._valid_regions.get_region_by_code(row[3])
            return Sales(id=row[0], amount=row[1], sales_date=date.fromisoformat(row[2]), region=region)
        return None

    def update_sales(self, sales: Sales) -> None:
        con = self.__connect()
        cur = con.cursor()
        query = '''UPDATE Sales SET amount = ? WHERE id = ?'''
        cur.execute(query, (sales['amount'], sales['ID']))
        con.commit()
        con.close()

    def retrieve_regions(self) -> Optional[Regions]:
        return self._valid_regions
