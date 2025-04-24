from pathlib import Path

class FileType:
    def __init__(self, f_name: str='', d_path: Path = None):
        self._dirpath: Path = Path(__file__).parent.parent / 'psc01' if d_path is None else d_path
        self._filename: str = f_name

    @property
    def dirpath(self) -> Path:
        return self._dirpath

    @property
    def filename(self) -> str:
        return self._filename
