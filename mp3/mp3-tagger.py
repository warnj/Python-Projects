from os import walk
import eyed3

'''
Files follow naming conventions:
    Artist - Title.mp3
    Artist - Movie - Title.mp3
    Artist - Album - Title.mp3
'''

# SOURCE_PATH = 'D:/Music/Int/Country/'
SOURCE_PATH = 'D:/Music/Int/Movie/'
# SOURCE_PATH = 'D:/Music/Int/'
# SOURCE_PATH = 'D:/OneDrive/Documents/Favorites Places Contacts Program Backup/youtube/'

ALBUM = ''
GENRE = 'Soundtrack'  # examples: Country / Soundtrack - https://eyed3.readthedocs.io/en/latest/plugins/genres_plugin.html


# artist is always the first token before delimiter string " - "
def getArtistName(filename):
    try:
        i = filename.index(' - ')
    except ValueError:
        print('no " - " in file {}'.format(filename))
        return None
    return filename[:i]


# title is always the last token after final delimiter string " - "
def getTitleName(filename):
    try:
        i = filename.rindex(' - ')
    except ValueError:
        print('no " - " in file {}'.format(filename))
        return None
    return filename[i + 3:-4]


# https://stackoverflow.com/questions/4664850/how-to-find-all-occurrences-of-a-substring
def find_all(a_str, sub):
    indexes = []
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1:
            return indexes
        else:
            indexes.append(start)
        start += len(sub)  # use start += 1 to find overlapping matches


# album is only present when two delimiter strings " - " are present and it's the middle value
def getAlbumName(filename):
    idxs = find_all(filename, ' - ')
    if len(idxs) != 2:
        return None
    return filename[idxs[0] + 3: idxs[1]]


# basic unit tests
# filename = 'A Artist - A Title.mp3'
# assert getArtistName(filename) == 'A Artist'
# assert getAlbumName(filename) is None
# assert getTitleName(filename) == 'A Title'
# filename = 'A Artist - A Album - A Title.mp3'
# assert getArtistName(filename) == 'A Artist'
# assert getAlbumName(filename) == 'A Album'
# assert getTitleName(filename) == 'A Title'
# exit(1)

updateCount = 0
_, _, filenames = next(walk(SOURCE_PATH))
for filename in filenames:
    if filename.endswith('.mp3'):
        # print(filename)
        audiofile = eyed3.load(SOURCE_PATH + filename)
        if not audiofile or not audiofile.tag:
            print('error loading audiofile {}'.format(filename))
            # continue
            break

        updated = False
        fArtist = getArtistName(filename)
        if fArtist != audiofile.tag.artist:
            print('artist from ({}) file ({}) does not match metadata ({})'.format(filename, fArtist, audiofile.tag.artist))
            audiofile.tag.artist = fArtist
            updated = True

        fTitle = getTitleName(filename)
        if fTitle != audiofile.tag.title:
            print('title from ({}) file ({}) does not match metadata ({})'.format(filename, fTitle, audiofile.tag.title))
            audiofile.tag.title = fTitle
            updated = True

        fAlbum = getAlbumName(filename)
        if ALBUM and ALBUM != audiofile.tag.album:
            print('album ({}) does not match metadata ({})'.format(ALBUM, audiofile.tag.album))
            audiofile.tag.album = ALBUM
            updated = True
        elif fAlbum and fAlbum != audiofile.tag.album:
            print('album from ({}) file ({}) does not match metadata ({})'.format(filename, fAlbum, audiofile.tag.album))
            audiofile.tag.album = fAlbum
            updated = True

        if GENRE and GENRE != audiofile.tag.genre:
            print('genre ({}) does not match metadata ({})'.format(GENRE, audiofile.tag.genre))
            audiofile.tag.genre = GENRE
            updated = True

        # if updated:  # actually do the update
        #     print('updating...')
        #     audiofile.tag.save()
        #     updateCount += 1

print('updated {} files'.format(updateCount))
