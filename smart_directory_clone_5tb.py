import os, shutil

# Settings
SOURCE = 'D:/Pictures'
DESTINATION = 'F:/Justin/Pictures'
# DESTINATION = 'H:/JKW_BKUP/Pictures'
VACATION_YEARS_TO_PRESERVE = {str(year) for year in range(2006, 2025)}  # IMPORTANT TO ADD TO THIS AS NEEDED
TEST = True  # ALWAYS RUN FIRST IN TEST MODE
PRINT = True
PRESERVED_PATH_PREFIX = os.path.normpath(os.path.join(DESTINATION, 'Vacation'))

def copyfile(src, dest):
    try:
        shutil.copy2(src, dest)
    except Exception as e:
        print(f'Exception while copying {src} to {dest}, err: {e}')

def deletefile(file):
    try:
        os.unlink(file)
    except Exception as e:
        print(f'Exception while deleting {file}, err: {e}')

def deletedir(dir):
    try:
        os.rmdir(dir)
    except Exception as e:
        print(f'Exception while deleting empty directory {dir}, err: {e}')

def is_preserved_vacation_path(p):
    norm_path = os.path.normpath(p)
    if norm_path.startswith(PRESERVED_PATH_PREFIX):
        relative_path = os.path.relpath(norm_path, PRESERVED_PATH_PREFIX)
        parts = relative_path.split(os.sep)
        if parts and parts[0] in VACATION_YEARS_TO_PRESERVE:
            return True
    return False

if not os.path.isdir(DESTINATION):
    print(f'ERROR: Destination directory "{DESTINATION}" does not exist')
    exit(1)

tag = 'Test: ' if TEST else ''
files = {}   # dest abs path -> source path
dirs = {}   # dest abs path -> source path

# Walk source directory
print('Beginning directory walk to create source to dest mapping')
for root, directories, filenames in os.walk(SOURCE):
    relativeroot = root[len(SOURCE)+1:]  # relative path to root directory from SOURCE
    destroot = os.path.join(DESTINATION, relativeroot)  # future absolute path to root directory from DESTINATION

    for directory in directories:
        s = os.path.normpath(os.path.join(root, directory))
        d = os.path.normpath(os.path.join(destroot, directory))
        dirs[d] = s

    for filename in filenames:
        s = os.path.normpath(os.path.join(root, filename))
        d = os.path.normpath(os.path.join(destroot, filename))
        files[d] = s

# Remove orphaned files in destination
print('Removing destination files that are not present in source')
for root, directories, filenames in os.walk(DESTINATION):
    if is_preserved_vacation_path(root):
        # print(f'skipping path {root} since it is in vacation')
        continue

    for filename in filenames:
        d = os.path.normpath(os.path.join(root, filename))
        if d not in files:
            if PRINT:
                print(f'{tag}deleting file from dest that is no longer in src: {d}')
            if not TEST:
                deletefile(d)

# Remove empty directories
print('Removing empty destination directories')
for root, directories, filenames in os.walk(DESTINATION, topdown=False):
    for directory in directories:
        d = os.path.normpath(os.path.join(root, directory))
        if os.path.isdir(d) and not os.listdir(d):
            if PRINT:
                print(f'{tag}removing empty directory {d}')
            if not TEST:
                deletedir(d)

# Make needed directories
print('Making dest directories')
for d in dirs:
    if not os.path.isdir(d):
        if PRINT:
            print(f'{tag}creating directory {d}')
        if not TEST:
            os.makedirs(d, exist_ok=True)

# Copy missing or changed files
print('Comparing files and copying if needed')
for dest, src in files.items():
    try:
        stats = os.stat(dest)
    except OSError:
        if PRINT:
            print(f'{tag}file {dest} does not exist, copying')
        if not TEST:
            copyfile(src, dest)
    else:
        try:
            srcstats = os.stat(src)
            if stats.st_size != srcstats.st_size:
                if PRINT:
                    print(f'{tag}File exists {dest}, overwriting dest')
                if not TEST:
                    copyfile(src, dest)
        except OSError:
            print(f'{tag}Exception getting source stats {src}')

print('Done cloning')
