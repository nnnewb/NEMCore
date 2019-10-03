import json
from collections import UserDict
from os import makedirs
from pathlib import Path


class PersistentDict(UserDict):
    def __init__(self, file_path: str):
        ''' 数据持久化存储
        '''
        super().__init__()
        self.storage_path = Path(file_path)

        if not self.storage_path.exists():
            makedirs(self.storage_path.parent, exist_ok=True)
            self.save()
        else:
            self.load()

    def load(self):
        with open(self.storage_path, 'r', encoding='utf-8') as f:
            self.data = json.loads(f.read())

    def save(self):
        with open(self.storage_path, 'w+', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, sort_keys=True)
