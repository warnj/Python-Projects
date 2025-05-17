import os, pathlib

# removes all mac files that start with '._'

SOURCE_PATH = 'D:/Pictures/Vacation/'

def deletefile(file):
    try:
        os.unlink(file)
    except Exception as e:
        print('Exception while deleting {}, err: {}'.format(file, e))

def printContents(directory):
    dirCount = 0
    fileCount = 0
    deletedCount = 0
    for root, dirs, files in sorted(os.walk(directory)):
        dirCount += 1
        fileCount += len(files)
        for file in sorted(files):
            absPath = f"{pathlib.PureWindowsPath(root).as_posix()}/{file}"
            if file.startswith('._') or file == '.DS_Store':
                print('deleting', absPath)
                deletedCount += 1
                # deletefile(absPath)

    print('{} directories (including root) and {} files and {} deleted files'.format(dirCount, fileCount, deletedCount))

printContents(SOURCE_PATH)
