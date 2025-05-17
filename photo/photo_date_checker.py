from PIL import Image
from os import walk
from datetime import datetime as dt

TIMEPARSEFMT = '%Y:%m:%d %H:%M:%S'  # example: 2019-01-18 22:36:01
DATEFMT = '%Y-%m-%d'  # example 2019-01-18

SOURCE_PATH = 'D:/Pictures/Underwater/ID Guide Puget Sound/'
# SOURCE_PATH = 'D:/Pictures/'

allDates = set()
_, _, filenames = next(walk(SOURCE_PATH))
for filename in filenames:
    if filename.lower().endswith('jpg'):
        exif = Image.open(SOURCE_PATH + filename).getexif()
        earliestTime = None
        for num, val in exif.items():
            if isinstance(val, str):
                try:
                    time = dt.strptime(val, TIMEPARSEFMT)
                    earliestTime = time if not earliestTime or time < earliestTime else earliestTime
                except ValueError:
                    pass
        # print('image {} date {}'.format(filename, earliestTime))
        if not earliestTime:
            print('image {} has no date, exif = {}'.format(filename, exif))
        else:
            allDates.add(dt.strftime(earliestTime, DATEFMT))
    else:
        print('NOT A JPG: ', filename)

for day in sorted(allDates):
    print(day)
