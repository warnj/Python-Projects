from PIL import Image
from os import walk
from datetime import datetime as dt

# prints the photos that have been deleted from the given directory, assumes they should be in strictly increasing order
SOURCE_PATH = '/Users/justin.warner/Pictures/412_0426/'

_, _, filenames = next(walk(SOURCE_PATH))
filenames = sorted(filenames)
prevnum = None
deleted = []
for name in filenames:
    print(name)
    if name.lower().endswith('.jpg'):
        num = int(name[4:8])
        if prevnum and prevnum + 1 != num:
            while prevnum + 1 != num:
                deleted.append(prevnum + 1)
                prevnum += 1
        prevnum = num

print(deleted)
