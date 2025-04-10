# Provides the tools for creating and running tests.
import unittest

# Allows running external processes (like your console application)
# and interacting with their input/output.
import subprocess

from pathlib import Path
FILEPATH: Path = Path(__file__).parent.parent / 'data'
ALL_SALES: Path = FILEPATH / 'all_sales.csv'
ALL_SALES_COPY: Path = FILEPATH / 'all_sales_copy.csv'
IMPORTED_FILES: Path = FILEPATH / 'imported_files.txt'
GID = '12'
TEST_APP_LOG: Path = Path('./test_app_log.txt')


class TestSalesDataImporter(unittest.TestCase):

    def setUp(self):
        """Set up the required content for testing"""
        with open(ALL_SALES, "w", newline='') as f:
            f.write("12493.0,2020-12-22,w\n"
                    "13761.0,2021-09-15,e\n"
                    "9710.0,2021-05-15,e\n"
                    "8934.0,2021-08-08,c\n"
                    "18340.0,2020-12-22,c\n"
                    "12345.0,2020-04-17,m\n"
                    "2929.0,2021-04-10,w\n"
                    )
        with open(IMPORTED_FILES, "w") as f:
            f.write("")

    def test_raise_exception(self):
        input_data = "test\nexit\n"
        stdout, stderr = self.run_app(input_data)

        self.assertIn("Is the file closed yet? No", stdout)
        self.assertIn("Confirm if the file is closed. Yes", stdout)
        self.assertIn("<class 'OSError'>", stdout)

    def run_app(self, input_data):
        entry_point: str = 'g12_main.py'
        print(f"{entry_point=}")
        # Start the process
        process = subprocess.Popen(
             ["python", entry_point],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
         )
        stdout, stderr = process.communicate(input=input_data)
        return stdout, stderr

    def test_exit_command(self):
        input_data = "exit\n"
        stdout, stderr = self.run_app(input_data)
        self.assertIn("Saved sales records.\nBye!\n", stdout)

    def test_menu_command(self):
        input_data = "menu\nexit\n"
        stdout, stderr = self.run_app(input_data)
        self.assertIn("COMMAND MENU\n", stdout)

    def test_invalid_menu_command(self):
        input_data = "mmm\nexit\n"
        stdout, stderr = self.run_app(input_data)
        self.assertIn("Invalid command. Please try again.\n\nCOMMAND MENU\n", stdout)

    def test_view_command(self):
        self.setUp()
        input_data = "view\nexit\n"
        stdout, stderr = self.run_app(input_data)
        self.assertIn("Date", stdout)
        self.assertIn("TOTAL", stdout)

    def test_add1_command(self):
        self.setUp()
        input_data = ("add1\n"
                      "0\n3245\n"
                      "3000\n2021\n"
                      "0\n13\n2\n"
                      "0\n40\n14\n"
                      "x\nc\n"
                      "exit\n")
        stdout, stderr = self.run_app(input_data)
        self.assertIn("Sales for 2021-02-14 is added.\n", stdout)

    def test_add2_command(self):
        self.setUp()
        input_data = ("add2\n"
                      "3245\n"
                      "2021-08-14\n"
                      "e\n"
                      "exit\n")
        stdout, stderr = self.run_app(input_data)
        self.assertIn("Sales for 2021-08-14 is added.\n", stdout)

    def test_import_command(self):
        self.setUp()
        input_data = ("import\n"
                      "sales_q4_2021_w.csv\n"
                      "exit\n")
        stdout, stderr = self.run_app(input_data)
        self.assertIn("Imported sales added to list.", stdout)


def run_tests(group):
    with open(TEST_APP_LOG, "w") as f:
        header = "\n" + "~" * 10 + f" GROUP {group} REPORT " + "~" * 10 + "\n"
        f.write(header)
        runner = unittest.TextTestRunner(stream=f, verbosity=2)
        unittest.main(testRunner=runner, exit=False)

if __name__ == "__main__":
    import sys
    custom_args = []
    remaining_args = []
    for arg in sys.argv:
        if arg.startswith("--"):
            custom_args.append(arg)
        else:
            remaining_args.append(arg)
    sys.argv = remaining_args
    group = custom_args[0].replace('--', '') if custom_args else '12'
    GID = group
    print(f"{GID=}, {group=}")

    run_tests(group)
