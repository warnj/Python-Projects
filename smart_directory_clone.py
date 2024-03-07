import os, shutil

#copies file from src to dest, deleting the dest file if it exists
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

def deletedir(dir):
    try:
        os.rmdir(dir)
    except Exception as e:
        print('Exception while deleting empty directory {}, err: {}'.format(dir, e))


# !!!!!!!!!!!!!!!!!!!!  WARNING: DOUBLE CHECK THIS  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
SOURCE = 'D:\Pictures'
DESTINATION = 'F:\Bkup 2019_6_23\Pictures'
TEST = False
PRINT = True

files = {}  # dest abs path -> source path
dirs = {}  # dest abs path -> source path
os.makedirs(DESTINATION, exist_ok=True)
if TEST:
    tag = 'Test: '
else:
    tag = ''

# create source to destination file and directory mappings
print('Beginning directory walk to create source to dest mapping')
for root, directories, filenames in os.walk(SOURCE):
    relativeroot = root[len(SOURCE)+1:]  # relative path to root directory from SOURCE
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
print('Removing destination files that are not present in source')
for root, directories, filenames in os.walk(DESTINATION):
    for filename in filenames:
        d = os.path.join(root, filename)
        if d not in files:
            if PRINT:
                print('{}deleting file from dest that is no longer in src: {}'.format(tag, d))
            if not TEST:
                deletefile(d)


# remove empty directories in destination
print('Removing empty dest directories')
for root, directories, filenames in os.walk(DESTINATION):
    for directory in directories:
        d = os.path.join(root, directory)
        if len(os.listdir(d)) == 0:
            if PRINT:
                print('{}removing empty directory {}'.format(tag, d))
            if not TEST:
                deletedir(d)


# make directories in destination as needed
print('Making dest directories')
for d in dirs:
    if not os.path.isdir(d):
        if PRINT:
            print('{}creating directory {}'.format(tag, d))
        if not TEST:
            os.makedirs(d, exist_ok=True)


# copy files to destination that are not already there
print('Comparing files and copying if needed')
for dest, src in files.items():
    try:
        stats = os.stat(dest)
    except OSError:
        # file doesn't exist
        if PRINT:
            print('{}file {} does not exist, copying'.format(tag, dest))
        if not TEST:
            copyfile(src, dest)
    else:
        # file does exist, compare stats
        srcstats = os.stat(src)
        if stats.st_size == srcstats.st_size:
            # print('files the same size, skipping {}'.format(dest))
            continue
        else:  # this happens if previously backed up photo is rotated or otherwise changed
            if PRINT:
                print('{}File exists {}, overwriting dest'.format(tag, dest))
            if not TEST:
                copyfile(src, dest)

print('Done cloning')
