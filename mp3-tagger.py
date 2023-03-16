from os import walk
import eyed3

# SOURCE_PATH = 'D:/Music/Int/Country/'
SOURCE_PATH = 'D:/Music/Int/'

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
    titlename = filename[i+3:-4]
    return titlename

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

        if updated: # actually do the update
            print('updating...')
            audiofile.tag.save()
            updateCount += 1

print('updated {} files'.format(updateCount))
