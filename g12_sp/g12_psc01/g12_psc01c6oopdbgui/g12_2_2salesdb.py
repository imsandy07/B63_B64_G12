# g07_2_2salesdb.py
from g07_1_1filetypes import FileType
from g07_1_1salestypes import Sales, Regions, Region
from typing import Optional
from pathlib import Path
from datetime import date
import sqlite3


class SQLiteDBAccess:
    def __init__(self, db_name: str = '', db_path: Path = None):
        self._valid_regions = Regions.from_dict()
        fname: str = db_name if db_name else 'sales_db.sqlite'
        fpath: Path = db_path if db_path else Path(__file__).parent.parent.parent / 'psc01_db'
        self._sqlite_sales_db = FileType(fname, fpath)

    def __connect(self) -> sqlite3.Connection:
        """Connect to the SQLite database and return the connection object."""
        try:
            conn = sqlite3.connect(self._sqlite_sales_db.dirpath / self._sqlite_sales_db.filename)
            conn.row_factory = sqlite3.Row
            return conn
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            raise

    def retrieve_sales_by_date_region(self, sales_date: date, region_code: str) -> Optional[Sales]:
        """Retrieve sales record by date and region code."""
        try:
            with self.__connect() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT * FROM Sales WHERE salesDate = ? AND region = ?",
                    (sales_date.isoformat(), region_code)
                )
                row = cursor.fetchone()
                if row:
                    region = self._valid_regions.get_region_by_code(row['region'])
                    return Sales(
                        amount=row['amount'],
                        sales_date=date.fromisoformat(row['salesDate']),
                        region=region,
                        id=row['ID'])
                else:
                    return None  # Explicitly return None if no row found
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        return None

    def update_sales(self, sales: Sales) -> None:
        """Update sales record in the database."""
        try:
            with self.__connect() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE Sales SET amount = ? WHERE ID = ?",
                    (sales['amount'], sales['ID']))
                conn.commit()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            raise

    def retrieve_regions(self) -> Optional[Regions]:
        """Retrieve all regions from the database."""
        try:
            with self.__connect() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM Region")
                rows = cursor.fetchall()
                if rows:
                    codes = [row['code'] for row in rows]
                    names = [row['name'] for row in rows]
                    return Regions(codes, names)
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        return None


def main():
    pass