from os import walk
import os

SOURCE_PATH = 'D:/Pictures/Underwater/Identification Guide/'

for dirpath, _, filenames in walk(SOURCE_PATH):
    for name in sorted(filenames):
        file_path = os.path.join(dirpath, name).replace(SOURCE_PATH, '').replace('\\', '/')
        print(file_path)
