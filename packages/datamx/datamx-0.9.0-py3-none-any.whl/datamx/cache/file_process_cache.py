import glob
import os
from pathlib import Path
from typing import List


class FileProcessCache:

    def __init__(self, cache_dir: Path, processed_dir: Path, extension: str = "json", entries: List[Path] = None):
        self.entries = entries if entries is not None else []
        self.extension = extension
        self.store_dir = processed_dir
        self.cache_dir = cache_dir

    def size(self) -> int:
        return len(self.entries)

    def get_entries(self) -> List[Path]:
        return self.entries

    def load_cache(self) -> List[Path]:
        self.create_dir(self.cache_dir)
        self.entries = [Path(f) for f in glob.glob(str(self.cache_dir) + "\*." + self.extension)]
        self.entries.sort()
        return self.entries

    def move_to_processed(self, entry: Path) -> Path:
        self.entries.remove(entry)
        dest = Path(self.store_dir, entry.name)
        os.rename(str(entry), dest)
        return dest

    @staticmethod
    def create_dir(path):
        os.makedirs(path, exist_ok=True)
