from os import walk

SOURCE_PATH = 'D:/Pictures/All/Underwater/ID Guide Puget Sound/'

_, _, filenames = next(walk(SOURCE_PATH))

for name in sorted(filenames):
    print(name)
