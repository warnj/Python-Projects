import os
import shutil
import re

def deletedir(dir):
    try:
        os.rmdir(dir)
    except Exception as e:
        print('Exception while deleting empty directory {}, err: {}'.format(dir, e))

def sanitize_filename(filename):
    # Remove leading numbers and underscores (e.g., "04 Faithfully.m4a" -> "Faithfully.m4a")
    filename = filename.strip()
    return re.sub(r'^\d+[\s._-]*', '', filename)

def move_files_to_root(root_dir, dryrun=True):
    for subdir, dirs, files in os.walk(root_dir):

        if subdir == root_dir:
            print('skipping root dir')
            continue

        # Extract artist name from the immediate subdirectory of root_dir (i.e., first directory under root_dir)
        artist = os.path.basename(os.path.dirname(subdir))  # Go up one level to get the artist name

        for file in files:
            file_path = os.path.join(subdir, file)

            # Extract file title and extension, sanitize title to remove leading numbers
            title, extension = os.path.splitext(file)
            title = sanitize_filename(title)

            # Create the new file name in the desired format
            new_filename = f"{artist} - {title}{extension}"
            new_path = os.path.join(root_dir, new_filename)

            # Ensure no file name conflict by adding a suffix if a file already exists
            if os.path.exists(new_path):
                base, extension = os.path.splitext(new_filename)
                counter = 1
                while os.path.exists(new_path):
                    new_name = f"{base}_duplicate_{counter}{extension}"
                    new_path = os.path.join(root_dir, new_name)
                    counter += 1

            print('moving file from {} to {}'.format(file_path, new_path))
            if not dryrun:
                try:
                    shutil.move(file_path, new_path)
                except Exception as e:
                    print('Exception while moving file from {} to {}, err: {}'.format(file_path, new_path, e))

    for subdir, dirs, files in os.walk(root_dir, topdown=False):
        if subdir != root_dir:
            if not os.listdir(subdir):
                print('removing empty dir', subdir)
                if not dryrun:
                    deletedir(subdir)

# Example usage:
root_directory = 'F:/Mom/Music'
move_files_to_root(root_directory, False)
