from difflib import SequenceMatcher
from os import walk
import eyed3

# Searched music directory and compares song titles against a list of all songs in an album. Prints the missing album
# songs and re-names files to exactly match the album title it is most similar to.

# SOURCE_PATH = 'D:/Music/Int/Country/'
# SOURCE_PATH = 'D:/Music/Int/'
SOURCE_PATH = 'D:/OneDrive/Documents/Favorites Places Contacts Program Backup/yt/'

UPDATE_COUNT = 0

ARTIST = ''
ALBUM = ''
# https://www.cheatsheet.com/entertainment/entire-36-song-track-list-morgan-wallens-one-thing-at-a-time.html
ALBUM_SONGS = []


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def getArtistName(filename):
    try:
        i = filename.index(' - ')
    except ValueError:
        print('no " - " in file {}'.format(filename))
        return None
    artistname = filename[:i]
    return artistname


def getTitleName(filename):
    try:
        i = filename.index(' - ')
    except ValueError:
        print('no " - " in file {}'.format(filename))
        return None
    titlename = filename[i + 3:-4]
    if titlename.endswith('+'):
        titlename = titlename[:-1]
    return titlename


def update(fTitle):
    audiofile = eyed3.load(SOURCE_PATH + filename)
    if not audiofile or not audiofile.tag:
        print('error loading audiofile {}'.format(filename))
        # continue
        exit(1)

    updated = False
    fArtist = getArtistName(filename)
    if fArtist != audiofile.tag.artist:
        print('artist from ({}) file ({}) does not match metadata ({})'.format(filename, fArtist, audiofile.tag.artist))
        audiofile.tag.artist = fArtist
        updated = True

    if fTitle != audiofile.tag.title:
        print('title from ({}) file ({}) does not match metadata ({})'.format(filename, fTitle, audiofile.tag.title))
        audiofile.tag.title = fTitle
        updated = True

    if ALBUM and ALBUM != audiofile.tag.album:
        print('album ({}) does not match metadata ({})'.format(ALBUM, audiofile.tag.album))
        audiofile.tag.album = ALBUM
        updated = True

    if updated:  # actually do the update
        print('updating...')
        audiofile.tag.save()
        global UPDATE_COUNT
        UPDATE_COUNT += 1


def compareToAlbumSongs(fTitle):
    for song in ALBUM_SONGS:
        score = similar(fTitle.upper(), song.upper())
        if song == fTitle or score > 0.85:
            print('file title: {} matches album song: {} with similar score: {}'.format(fTitle, song, score))
            update(fTitle)
            ALBUM_SONGS.remove(song)
            break


_, _, filenames = next(walk(SOURCE_PATH))
for filename in filenames:
    if filename.endswith('.mp3') and filename.startswith(ARTIST):
        fTitle = getTitleName(filename)
        compareToAlbumSongs(fTitle)

print('updated {} files of the album total {}'.format(UPDATE_COUNT, len(ALBUM_SONGS)))
print('remaining album songs:', ALBUM_SONGS)
