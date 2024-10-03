import os
import re

def deletefile(file):
    try:
        os.remove(file)
    except Exception as e:
        print('Exception while deleting {}, err: {}'.format(file, e))

def remove_duplicate_files(directory, dryrun=True):
    # Dictionary to store files based on their base names
    file_groups = {}

    # Regex to identify base name and duplicate suffix pattern
    duplicate_pattern = re.compile(r'^(.*?)(_duplicate_\d+)?(\.[a-zA-Z0-9]+)$')

    # Loop over all files in the directory
    for filename in os.listdir(directory):
        match = duplicate_pattern.match(filename)
        if match:
            base_name = match.group(1)
            extension = match.group(3)

            # Full base name (without duplicate suffix)
            full_base_name = base_name + extension

            # Group files by their full base name
            if full_base_name not in file_groups:
                file_groups[full_base_name] = []
            file_groups[full_base_name].append(filename)

    # Compare the files in each group to check for duplicates
    for base_name, files in file_groups.items():
        if len(files) > 1:
            # Sort files to compare them more effectively
            files.sort()

            for i in range(len(files) - 1):
                file1 = files[i]
                file2 = files[i + 1]

                file1_path = os.path.join(directory, file1)
                file2_path = os.path.join(directory, file2)

                # Compare file sizes
                if os.path.exists(file1_path) and os.path.exists(file2_path):
                    size1 = os.path.getsize(file1_path)
                    size2 = os.path.getsize(file2_path)

                    if size1 == size2:
                        # If the sizes are the same, remove the duplicate file
                        if not dryrun:
                            deletefile(file2_path)
                        print(f"Removed duplicate file with size {size1}: {file2_path}")
                    # else:
                    #     print(f"Different sizes, kept both: {file1_path} and {file2_path}")

directory_path = 'F:/Mom/Pictures'
remove_duplicate_files(directory_path)
