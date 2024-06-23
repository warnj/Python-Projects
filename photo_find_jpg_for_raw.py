import os, pathlib
import shutil
from os import walk

# given dir with raw files will search for the corresponding jpg and copy it

DIR_WITH_RAW = 'D:/Pictures/All/Vacation/2024/2024_06 Socorro/top'
DIR_WITH_RAW = 'D:/Pictures/All/Vacation/2024/2024_06 Socorro/top/justin-send-to-people'

_, _, filenames = next(walk(DIR_WITH_RAW))

def get_directories_os(path):
    directories = [name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name)) and not name.startswith('top')]
    return directories

def copyfile(src, dest):
    try:
        shutil.copy2(src, dest)
    except Exception as e:
        print('Exception while copying {} to {}, err: {}'.format(src, dest, e))

dirs = get_directories_os('D:/Pictures/All/Vacation/2024/2024_06 Socorro/')
print(dirs)

for name in filenames:
    if name.endswith('CR2'):
        targetname = name.replace('CR2', 'JPG')
        print('looking for file: ', targetname)
        for d in dirs:
            _, _, files = next(walk('D:/Pictures/All/Vacation/2024/2024_06 Socorro/'+d))
            for f in files:
                if f == targetname:
                    ogpath = 'D:/Pictures/All/Vacation/2024/2024_06 Socorro/'+d+'/'+f
                    print('found the jpg at ' + ogpath)
                    if not os.path.isfile(DIR_WITH_RAW + '/' + f):
                        print('copying file', ogpath)
                        copyfile(ogpath, DIR_WITH_RAW)
