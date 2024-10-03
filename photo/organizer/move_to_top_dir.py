import os
import shutil

# this is step 1

def deletedir(dir):
    try:
        os.rmdir(dir)
    except Exception as e:
        print('Exception while deleting empty directory {}, err: {}'.format(dir, e))

def move_files_to_root(root_dir, dryrun=True):
    for subdir, dirs, files in os.walk(root_dir):
        # print('subdir', subdir, 'dirs', dirs, 'files', files)

        if subdir == root_dir:
            print('skipping root dir')
            continue

        # if root_directory + '\\2010' in str(subdir):
        #     print('DEALING WITH 2010: ' + str(subdir))

        for file in files:
            file_path = os.path.join(subdir, file)
            new_path = os.path.join(root_dir, file)
            if os.path.exists(new_path):
                base, extension = os.path.splitext(file)
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
        # else:
        #     continue

    for subdir, dirs, files in os.walk(root_dir, topdown=False):
        if subdir != root_dir:
            if not os.listdir(subdir):
                print('removing emtpy dir', subdir)
                if not dryrun:
                    deletedir(subdir)

root_directory = 'F:/Mom/Pictures'
move_files_to_root(root_directory)
