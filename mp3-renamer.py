import os
from os import walk

SOURCE_PATH = 'D:/OneDrive/Documents/Favorites Places Contacts Program Backup/youtube/'
prefix_to_add = 'name - '

# renames files of the format consisting only of song title
def renameTitleOnly(filename):
    if filename.endswith('.mp3') and not filename.startswith(prefix_to_add):
        title = filename[:-18]
        newName = prefix_to_add + title + '.mp3'
        # print(newName)
        os.rename(SOURCE_PATH+filename, SOURCE_PATH+newName)

# renames file of the format including "(..." by removing the chars after first paren
def renameParen(filename):
    if filename.endswith('.mp3') and filename.startswith(prefix_to_add):
        head = filename.partition('(')[0]
        head = head[:-1]
        newName = head + '.mp3'
        # print(newName)
        os.rename(SOURCE_PATH + filename, SOURCE_PATH + newName)

_, _, filenames = next(walk(SOURCE_PATH))
for filename in filenames:
    renameParen(filename)
