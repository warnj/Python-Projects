import os, pathlib

# prints all files and directories (including subfiles and directories) in the given path indented by depth

# SOURCE_PATH = 'D:/Pictures/All/Special/'
SOURCE_PATH = 'D:/Pictures/'
SOURCE_PATH = '/Users/justin.warner/Pictures/2023_09_15 Vancouver Island Port Hardy Diving/'

def printContents(directory):
    dirCount = 0
    fileCount = 0
    for root, dirs, files in sorted(os.walk(directory)):
        level = root.replace(directory, '').count(os.sep)
        indent = "    " * level
        print(f"{indent}{pathlib.PureWindowsPath(root)}")
        dirCount += 1
        fileCount += len(files)
        for file in sorted(files):
            print(f"{indent}    {file}")
    print('{} directories (including root) and {} files'.format(dirCount, fileCount))

printContents(SOURCE_PATH)
