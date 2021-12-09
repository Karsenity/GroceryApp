import os
from pathlib import Path
import re


class Config:

    def __init__(self):
        try:
            import DoNotRemoveThis as beacon
            # print(f"'import beacon' -> {os.path.dirname(os.path.abspath(beacon.__file__))}")  # only for demo purposes
            # print(f"'import beacon' -> {Path(beacon.__file__).parent.resolve()}")  # only for demo purposes
        except ModuleNotFoundError as e:
            print(f"ModuleNotFoundError: import beacon failed with {e}. "
                  f"Please. create a file called DoNotRemove.py and place it to the project root directory.")
            raise Exception("Cannot Find Root Of Project Due To Missing File")

        self.project_root = Path(beacon.__file__).parent.resolve()

    def getPath(self, path):
        if isinstance(path, list):
            totalPath = '\\'
            test = [partPath.replace('/', '\\') for partPath in path]
            totalPath = "\\" + totalPath.join(test)
            return str(self.project_root) + totalPath
        else:
            path = path.replace('/', '\\')
            return str(self.project_root) + "\\" + path


if __name__ == '__main__':
    c = Config()
    print(f"Config.project_root: {c.project_root}")


