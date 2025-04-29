import unittest
from g12_2_salesmanager import raise_exception

class TestSalesManager(unittest.TestCase):
    def test_raise_exception(self):
        with self.assertRaises(OSError):
            raise_exception()

if __name__ == "__main__":
    unittest.main()
