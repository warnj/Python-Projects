from os import walk

# prints all files at root level in the given path

SOURCE_PATH = 'D:/Pictures/Underwater/ID Guide Puget Sound/'
# SOURCE_PATH = 'D:/Pictures/Underwater/Identification Guide/'

_, _, filenames = next(walk(SOURCE_PATH))

for name in sorted(filenames):
    print(name)
