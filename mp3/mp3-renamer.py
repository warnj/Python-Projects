import os
from os import walk

# helps bulk rename song files

SOURCE_PATH = 'D:/OneDrive/Documents/Favorites Places Contacts Program Backup/youtube/'
prefix_to_add = 'name - '

# renames files of the format consisting only of song title
def renameTitleOnly(filename):
    if filename.endswith('.mp3') and not filename.startswith(prefix_to_add):
        title = filename[:-18]
        return prefix_to_add + title + '.mp3'

# renames file of the format including "(..." by removing the chars after first paren
def renameParen(filename):
    if filename.endswith('.mp3') and filename.startswith(prefix_to_add):  # double check for sanity
        head = filename.partition('(')[0]
        head = head[:-1]
        return head + '.mp3'

_, _, filenames = next(walk(SOURCE_PATH))
for filename in filenames:

    if filename.endswith('.mp3') and filename.startswith(prefix_to_add):
        newName = renameParen(filename)
        print(newName)
        os.rename(SOURCE_PATH + filename, SOURCE_PATH + newName)

    # remove the track number prefix and add artist name
    # if filename.endswith('.mp3') and not filename.startswith(prefix_to_add):
    #     title = filename[3:]
    #     newName = prefix_to_add + title
    #     # print(newName)
    #     os.rename(SOURCE_PATH + filename, SOURCE_PATH + newName)
