import os, pathlib

# SOURCE_PATH = 'D:/Pictures/All/Special/'
SOURCE_PATH = 'D:/Pictures/'

def printContents(directory):
    dirCount = 0
    fileCount = 0
    for root, dirs, files in os.walk(directory):
        level = root.replace(directory, '').count(os.sep)
        indent = "    " * level
        print(f"{indent}{pathlib.PureWindowsPath(root)}")
        dirCount += 1
        fileCount += len(files)
        for file in files:
            print(f"{indent}    {file}")
    print('{} directories (including root) and {} files'.format(dirCount, fileCount))

printContents(SOURCE_PATH)
