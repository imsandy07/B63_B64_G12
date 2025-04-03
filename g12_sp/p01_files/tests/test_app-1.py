
# Provides the tools for creating and running tests.
import unittest

# Allows running external processes (like your console application)
# and interacting with their input/output.
import subprocess

from pathlib import Path
FILEPATH: Path = Path(__file__).parent.parent.parent / 'psc01_files'
ALL_SALES: Path = FILEPATH / 'all_sales.csv'
ALL_SALES_COPY: Path = FILEPATH / 'all_sales_copy.csv'
IMPORTED_FILES: Path = FILEPATH / 'imported_files.txt'
GID = '##'
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


    # def tearDown(self):
    #     """Tear down the environment for testing"""


    def run_app(self, input_data):
        """
        Simulates running the console application with user input.
        """
        entry_point: str = f'g{GID}_4_main.py'
        print(f"{entry_point=}")
        # Start the process
        process = subprocess.Popen(
             ["python", entry_point],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True # ensures that input/output is handled as text (not bytes).
         )
        # Send input and get output
        # sends the simulated user input (via stdin) to the console app.
        stdout, stderr = process.communicate(input=input_data)
        return stdout, stderr


    def test_exit_command(self):
        """
        Test the 'exit' command to terminate the application.
        """
        input_data = "exit\n"
        stdout, stderr = self.run_app(input_data)
        print(f"{input_data=}\n{stdout=}\n{stderr=}\n")

        self.assertIn("Saved sales records.\nBye!\n", stdout)


    def test_menu_command(self):
        """
        Test the 'menu' command to redisplay the menu.
        """
        input_data = "menu\nexit\n"
        stdout, stderr = self.run_app(input_data)
        print(f"{input_data=}\n{stdout=}\n{stderr=}\n")
        # Check that key parts of the expected output are present
        key_expected_output = (
            "COMMAND MENU\n"
        )
        # Assert that the key expected output appears in the stdout
        self.assertIn(key_expected_output, stdout)


    def test_invalid_menu_command(self):
        """
        Test an invalid command to redisplay the menu.
        """
        input_data = "mmm\nexit\n"
        stdout, stderr = self.run_app(input_data)
        print(f"{input_data=}\n{stdout=}\n{stderr=}\n")
        # Check that key parts of the expected output are present
        key_expected_output = (
            "Invalid command. Please try again.\n\nCOMMAND MENU\n"
        )
        # Assert that the key expected output appears in the stdout
        self.assertIn(key_expected_output, stdout)


    def test_view_command(self):
        """
        Test the 'view' command to display sales data.
        """
        self.setUp()
        input_data = "view\nexit\n"  # Simulates input
        stdout, stderr = self.run_app(input_data)
        print(f"{input_data=}\n{stdout=}\n{stderr=}\n")
        # Check that key parts of the expected output are present
        key_expected_output = (
            "     Date           Quarter        Region                  Amount\n"
            "-----------------------------------------------------------------\n"
            "1."
        )
        # Assert that the key expected output appears in the stdout
        self.assertIn(key_expected_output, stdout)  # self.assertEqual(stdout, key_expected_output)
        self.assertIn("-----------------------------------------------------------------\n"
                      "TOTAL", stdout)


    def test_add1_command(self):
        """
        Test the 'add1' command for adding sales with detailed input validation.
        """
        self.setUp()
        input_data = ("add1\n"
                      "0\n3245\n"
                      "0\n3000\n2021\n"
                      "0\n20\n2\n"
                      "0\n40\n14\n"
                      "x\nc\n"
                      "exit\n"
                      )
        stdout, stderr = self.run_app(input_data)
        print(f"{input_data=}\n{stdout=}\n{stderr=}\n")
        expected_steps = [ # "add1"
            "Amount:             ",  # "0\n"
            "Amount must be greater than zero.\nAmount:             ",  # "3245\n"
            "Year (2000-2999):   ",  # "0\n" or # "3000\n"
            "Year must be between 2000 and 2999.\nYear (2000-2999):   ",  # "2021\n"
            "Month (1-12):       ",  # "0\n" or # "20\n"
            "Month must be between 1 and 12.\nMonth (1-12):       ",  # "2\n"
            "Day (1-28):         ",  # "0\n" or # "40\n"
            "Day must be between 1 and 28.\nDay (1-28):         ",  # "14\n"
            "Region ('w', 'm', 'c', 'e'):",  # "x\n"
            "Region must be one of the following: ('w', 'm', 'c', 'e').\nRegion ('w', 'm', 'c', 'e'):",  # "c\n"
            "Sales for 2021-02-14 is added.\n",
        ]
        for i, step in enumerate(expected_steps, start=1):
            if i == len(expected_steps):
                break # no need to check the last step 'exit'
            else:
                self.assertIn(step, stdout)


    def test_add2_command(self):
        """
        Test the 'add2' command for adding sales with detailed input validation.
        """
        self.setUp()
        input_data = ("add2\n"
                      "3245\n"
                      "202a\n0021-08-14\n2021-8-14\n2021-08-14\n"
                      "e\n"
                      "exit\n"
                      )
        stdout, stderr = self.run_app(input_data)
        print(f"{input_data=}\n{stdout=}\n{stderr=}\n")
        expected_steps = [ # "add2"
            "Amount:             ",  # "3245\n"
            "Date (yyyy-mm-dd):  ",  # "202a\n"
            "202a is not in a valid date format.\nDate (yyyy-mm-dd):  ",  # "0021-08-14\n"
            "Year of the date must be between 2000 and 2999.\nDate (yyyy-mm-dd):  ",  # "2021-8-14\n"
            "2021-8-14 is not in a valid date format.\nDate (yyyy-mm-dd):  ", # "2021-08-14\n"
            "Region ('w', 'm', 'c', 'e'):",  # "e\n"
            "Sales for 2021-08-14 is added.\n",
        ]

        for i, step in enumerate(expected_steps, start=1):
            if i == len(expected_steps):
                break # no need to check the last step 'exit'
            else:
                self.assertIn(step, stdout)


    def test_import_command(self):
        """
        Test the 'import' command with valid and invalid filenames.
        """
        self.setUp()
        input_data = ("import\n"
            "region1\n"
            "import\nsales_q1_2021_x.csv\n"
            # "import\nsales_q1_2021_w.csv\n"
            "import\nsales_q2_2021_w.csv\n"
            "import\nsales_q3_2021_w.csv\n"
            "import\nsales_q4_2021_w.csv\n"
            "import\nsales_q4_2021_w.csv\n"
            "exit\n"
        )
        stdout, stderr = self.run_app(input_data)
        print(f"{input_data=}\n{stdout=}\n{stderr=}\n")
        expected_steps = [ # "import\n"
            "Enter name of file to import: ",  # "region1\n",
            "Filename 'region1' doesn't follow the expected format of sales_qn_yyyy_r.csv.\n"
            "\nPlease enter a command: ",  # "import\n", # "sales_q1_2021_x.csv\n"
            "Filename 'sales_q1_2021_x.csv' doesn't include one of the following region codes:"
            " ['w', 'm', 'c', 'e'].\n\nPlease enter a command: ",  # "import\n", # "sales_q2_2021_w.csv\n"
            "No sales to view.\n\nPlease enter a command: ",  # "import\n", "sales_q3_2021_w.csv\n"
            "     Date           Quarter        Region                  Amount\n"
            "-----------------------------------------------------------------\n"
            "1.*  ?              0              West                   13761.0\n"
            "2.*  ?              0              West                    9710.0\n"
            "3.*  ?              0              West                         ?\n"
            "-----------------------------------------------------------------\n"
            "TOTAL                                                     23471.0\n"
            "\nFile 'sales_q3_2021_w.csv' contains bad data.\n"
            "Please correct the data in the file and try again.\n"
            "\nPlease enter a command: ",  # "import\n", # "sales_q4_2021_w.csv\n"
            "     Date           Quarter        Region                  Amount\n"
            "-----------------------------------------------------------------\n"
            "1.   2021-10-15     4              West                   13761.0\n"
            "2.   2021-11-15     4              West                    9710.0\n"
            "3.   2021-12-15     4              West                    8934.0\n"
            "-----------------------------------------------------------------\n"
            "TOTAL                                                     32405.0\n"
            "\nImported sales added to list.\n"
            "\nPlease enter a command: ",  # "import\n", "sales_q4_2021_w.csv\n"
            "File 'sales_q4_2021_w.csv' has already been imported.\n"
            "\nPlease enter a command: ",  # "exit\n"
        ]

        for i, step in enumerate(expected_steps, start=1):
            if i == len(expected_steps):
                break # no need to check the last step
            else:
                self.assertIn(step, stdout)


def run_tests(group):
    # Open the log file for writing test results
    with open(TEST_APP_LOG, "w") as f:
        header = "\n" + "~" * 10 + f" GROUP {group} REPORT " + "~" * 10 + "\n"
        f.write(header)
        # Create a test runner with the log file as the output stream
        runner = unittest.TextTestRunner(stream=f, verbosity=2)
        # Run all tests
        unittest.main(testRunner=runner, exit=False)


if __name__ == "__main__":
    import sys
    # Parse custom arguments
    custom_args = []
    remaining_args = []
    for arg in sys.argv:
        if arg.startswith("--"):
            custom_args.append(arg)
        else:
            remaining_args.append(arg)
    # Set the remaining arguments back to sys.argv
    sys.argv = remaining_args
    group = custom_args[0].replace('--', '')
    GID = group
    print(f"{GID=}, {group=}")

    run_tests(group)

# Run test_app.py
# '''To redirect the test result to a file (e.g. test_log.txt)
# you need to use command line to run test_app.py file.
# - Launch a terminal (command prompt) and activate the project's virtual environment
# - Got to the directory where the test_app.py file is located.
# - use command python test_app.py --## to run the unit test,
# '''
