import os
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
import datetime
import re

# Regular expression to check if the filename starts with 4 digits and a hyphen
pattern = r'^\d{4}-'

video_extensions = ['.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv']

def deletefile(file):
    try:
        os.remove(file)
    except Exception as e:
        print('Exception while deleting {}, err: {}'.format(file, e))

def get_recording_date(file_path):
    parser = createParser(file_path)
    if not parser:
        print(f"Unable to parse {file_path}")
        return None

    with parser:
        metadata = extractMetadata(parser)
        if metadata and metadata.has("creation_date"):
            return metadata.get("creation_date")
        else:
            return None

# Function to rename files in the specified format
def rename_videos(directory):
    for filename in os.listdir(directory):
        file_extension = os.path.splitext(filename)[1].lower()
        if file_extension.lower() in video_extensions and not re.match(pattern, filename):
            file_path = os.path.join(directory, filename)

            # creation_time = os.path.getmtime(file_path)
            # formatted_time = datetime.datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d %H.%M.%S')

            recording_date = get_recording_date(file_path)
            if not recording_date:
                print('could not get creation time, skipping')
                continue
            formatted_time = recording_date.strftime('%Y-%m-%d %H.%M.%S')

            new_filename = f"{formatted_time}{file_extension}"
            new_file_path = os.path.join(directory, new_filename)

            if not os.path.exists(new_file_path):
                try:
                    os.rename(file_path, new_file_path)
                    print(f"Renamed {filename} to {new_filename}")
                except Exception as e:
                    print('Exception while renaming {} to {}, err: {}'.format(file_path, new_file_path, e))
            else:
                print(f"File {new_file_path} already exists.")
                size1 = os.path.getsize(file_path)
                size2 = os.path.getsize(new_file_path)
                if size1 == size2:
                    print(f"Size of {file_path} and {new_file_path} match, deleting duplicate")
                    deletefile(file_path)
                else:
                    print(f"Size of {file_path} and {new_file_path} do not match, skipping")

directory_path = 'F:/Mom/Pictures'
rename_videos(directory_path)
