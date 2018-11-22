import os, shutil


def copyfile(src, dest):
    try:
        shutil.copy2(src, dest)
    except Exception as e:
        print('Exception while copying {} to {}, err: {}'.format(src, dest, e))


def deletefile(file):
    try:
        os.unlink(file)
    except Exception as e:
        print('Exception while deleting {}, err: {}'.format(file, e))


SOURCE = '/Users/j.warner/scripts'
DESTINATION = '/Users/j.warner/scriptsbkup'

files = {}
dirs = {}
os.makedirs(DESTINATION, exist_ok=True)

# create source to destination file and directory mappings
for root, directories, filenames in os.walk(SOURCE):
    relativeroot = root[len(SOURCE) + 1:]  # relative path to root directory from SOURCE
    destroot = os.path.join(DESTINATION, relativeroot)  # future absolute path to root directory from DESTINATION

    for directory in directories:
        s = os.path.join(root, directory)
        d = os.path.join(destroot, directory)
        dirs[d] = s
    for filename in filenames:
        s = os.path.join(root, filename)
        d = os.path.join(destroot, filename)
        files[d] = s

# remove files in destination that do not have respective source file
for root, directories, filenames in os.walk(DESTINATION):
    for filename in filenames:
        d = os.path.join(root, filename)
        if d not in files:
            print('deleting file from dest that is no longer in src: {}'.format(d))
            deletefile(d)

# remove empty directories in destination
for root, directories, filenames in os.walk(DESTINATION):
    for directory in directories:
        d = os.path.join(root, directory)
        if len(os.listdir(d)) == 0:
            print('removing empty directory {}'.format(d))
            try:
                os.rmdir(d)
            except Exception as e:
                print('Exception while deleting empty directory {}, err: {}'.format(d, e))

# make directories in destination as needed
for d in dirs:
    if not os.path.isdir(d):
        os.makedirs(d, exist_ok=True)

# copy files to destination that are not already there
for dest, src in files.items():
    try:
        stats = os.stat(dest)
    except OSError:
        # file doesn't exist
        copyfile(src, dest)
    else:
        # file does exist, compare stats
        srcstats = os.stat(src)
        if stats.st_size == srcstats.st_size:
            # print('files the same size, skipping {}'.format(dest))
            continue
        elif stats.st_mtime == srcstats.st_mtime:
            # print('files modifies at same time, skipping {}'.format(dest))
            continue
        else:
            print('File exists, deleting dest, then copying to dest')
            # deletefile(dest)
            copyfile(src, dest)
