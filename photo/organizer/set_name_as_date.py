import os
from PIL import Image
import PIL.ExifTags as ExifTags
import re

# Regular expression to check if the filename starts with 4 digits and a hyphen
pattern = r'^\d{4}-'

def deletefile(file):
    try:
        os.remove(file)
    except Exception as e:
        print('Exception while deleting {}, err: {}'.format(file, e))

def get_photo_taken_date(image_path):
    try:
        image = Image.open(image_path)
        exif_data = image._getexif()

        # Find the tag for DateTimeOriginal, which contains the photo's timestamp
        if exif_data:
            for tag, value in exif_data.items():
                tag_name = ExifTags.TAGS.get(tag, tag)
                if tag_name == "DateTimeOriginal":
                    return value
    except Exception as e:
        print(f"Error reading EXIF data from {image_path}: {e}")
    return None

def rename_photos(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        # Check if it's a file with a photo extension
        if os.path.isfile(file_path) and filename.lower().endswith(('.jpg', '.jpeg', '.png')) and not re.match(pattern, filename):
            date_taken = get_photo_taken_date(file_path)

            if date_taken:
                # Format the date into 'YYYY-MM-DD HH.MM.SS'
                date_parts = date_taken.split(' ')
                date = date_parts[0].replace(':', '-')
                time = date_parts[1].replace(':', '.')

                # Create the new file name
                new_filename = f"{date} {time}.jpg"
                if filename.lower().endswith('.png'):
                    new_filename = f"{date} {time}.png"
                new_file_path = os.path.join(directory, new_filename)

                # Check if a file with the new name already exists to avoid overwriting
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
            else:
                print(f"No EXIF date data found for {filename}. Skipping.")


directory_path = 'F:/Mom/Pictures'
rename_photos(directory_path)
