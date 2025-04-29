from pathlib import Path

class FileType:
    def __init__(self, f_name: str='', d_path: Path = None):
        self._dirpath: Path = Path(__file__).parent.parent.parent / 'psc01_files' if d_path is None else d_path
        self._filename: str = f_name

    @property
    def dirpath(self) -> Path:
        return self._dirpath

    @property
    def filename(self) -> str:
        return self._filename

class SalesFile(FileType):
    def __init__(self, f_name: str = "", d_path: Path = None, n_convention: str = "sales_qn_yyyy_r.csv") -> None:
        super().__init__(f_name, d_path)
        self._name_convention = n_convention

    @property
    def is_valid_filename_format(self) -> bool:
        if len(self.filename) == len(self._name_convention) and \
           self.filename[:7] == self._name_convention[:7] and \
           self.filename[8] == self._name_convention[8] and \
           self.filename[13] == self._name_convention[-6] and \
           self.filename[-4:] == self._name_convention[-4:]:
            return True
        return False

    def get_region_code_from_filename(self) -> str:
        return self.filename[self.filename.rfind('.') - 1]

class ImportedFile(FileType):
    def __init__(self, f_name: str = 'imported_files.txt', d_path: Path = None) -> None:
        super().__init__(f_name, d_path)

    def already_imported(self, dpath_fname: Path) -> bool:
        try:
            with open(self.dirpath / self.filename) as file:
                files = [line.strip() for line in file.readlines()]
                return str(dpath_fname) in files
        except FileNotFoundError:
            return False

    def add_imported_file(self, dpath_fname: Path) -> None:
        try:
            with open(self.dirpath / self.filename, "a") as file:
                file.write(f"{dpath_fname}\n")
        except Exception as e:
            print(f"{type(e)} - The imported file could not be documented.")

def main():
    pass