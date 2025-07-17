#
# import os
# import re
# import sys
#
#
# def extract_artist_title(file_path):
#     """
#     Extract artist and title from a file path.
#     Expected format: .../Artist/Album/NN Title.ext
#     Special case: .../Compilations/Album/NN Title.ext -> Album - Title.ext
#
#     Args:
#         file_path (str): Full path to the music file
#
#     Returns:
#         str: Formatted string "Artist - Title.ext" or original filename if parsing fails
#     """
#     try:
#         # Get the filename and extension
#         filename = os.path.basename(file_path)
#         filename_no_ext = os.path.splitext(filename)[0]
#         extension = os.path.splitext(filename)[1]
#
#         # Split the path into parts
#         path_parts = file_path.split(os.sep)
#
#         # Find artist (second to last directory) and title (filename)
#         if len(path_parts) >= 3:
#             artist = path_parts[-3]  # Artist directory
#             album = path_parts[-2]   # Album directory
#
#             # Remove track number from filename (assumes format like "08 One Way Ticket")
#             title = filename_no_ext
#             # Remove leading numbers and spaces/dots/dashes
#             title = re.sub(r'^\d+[\s\.\-]*', '', title)
#
#             # Special case for Compilations
#             if artist.lower() == "compilations":
#                 return f"{album} - {title}{extension}"
#             else:
#                 return f"{artist} - {title}{extension}"
#         else:
#             # Fallback: just clean up the filename
#             title = re.sub(r'^\d+[\s\.\-]*', '', filename_no_ext)
#             return f"{title}{extension}"
#     except Exception:
#         # If anything goes wrong, return the original filename
#         return os.path.splitext(os.path.basename(file_path))[0]
#
# def list_music_files(directory_path):
#     """
#     List only music files (common audio formats).
#
#     Args:
#         directory_path (str): Path to the root directory to search
#     """
#     music_extensions = {'.mp3', '.wav', '.flac', '.m4a', '.aac', '.ogg', '.wma', '.mp4', '.m4v'}
#
#     if not os.path.exists(directory_path):
#         print(f"Error: Directory '{directory_path}' does not exist.")
#         return
#
#     if not os.path.isdir(directory_path):
#         print(f"Error: '{directory_path}' is not a directory.")
#         return
#
#     print(f"Listing music files in: {directory_path}")
#     print("-" * 60)
#
#     file_count = 0
#
#     for root, dirs, files in os.walk(directory_path):
#         for file in files:
#             file_ext = os.path.splitext(file)[1].lower()
#             if file_ext in music_extensions:
#                 file_path = os.path.join(root, file)
#                 prefix_to_remove = "F:/Personal backup docs\\iTunes\\iTunes Media\\Music\\"
#                 prefix_to_remove3 = "F:/Personal backup docs\\My Music\\iTunes\\iTunes Media\\Music\\"
#                 prefix_to_remove2 = "F:/Personal backup docs\\My Music\\Breezy Music Library\\iTunes Media\\Music\\"
#                 new_path = file_path.replace(prefix_to_remove, "")
#                 new_path = new_path.replace(prefix_to_remove2, "")
#                 new_path = new_path.replace(prefix_to_remove3, "")
#                 # print(file_path)
#                 # print(new_path)
#
#                 newTitle = extract_artist_title(new_path)
#                 print(newTitle)
#
#
#                 file_count += 1
#
#     print("-" * 60)
#     print(f"Total music files found: {file_count}")
#
#
# def main():
#     directory_path = 'F:/Personal backup docs'
#     list_music_files(directory_path)
#
#
# if __name__ == "__main__":
#     main()


import os
import re
import sys
import shutil


def extract_artist_title(file_path):
    """
    Extract artist and title from a file path.
    Expected format: .../Artist/Album/NN Title.ext
    Special case: .../Compilations/Album/NN Title.ext -> Album - Title.ext

    Args:
        file_path (str): Full path to the music file

    Returns:
        str: Formatted string "Artist - Title.ext" or original filename if parsing fails
    """
    try:
        # Get the filename and extension
        filename = os.path.basename(file_path)
        filename_no_ext = os.path.splitext(filename)[0]
        extension = os.path.splitext(filename)[1]

        # Split the path into parts
        path_parts = file_path.split(os.sep)

        # Find artist (second to last directory) and title (filename)
        if len(path_parts) >= 3:
            artist = path_parts[-3]  # Artist directory
            album = path_parts[-2]  # Album directory

            # Remove track number from filename (assumes format like "08 One Way Ticket")
            title = filename_no_ext
            # Remove leading numbers and spaces/dots/dashes
            title = re.sub(r'^\d+[\s\.\-]*', '', title)

            # Special case for Compilations
            if artist.lower() == "compilations":
                return f"{album} - {title}{extension}"
            else:
                return f"{artist} - {title}{extension}"
        else:
            # Fallback: just clean up the filename
            title = re.sub(r'^\d+[\s\.\-]*', '', filename_no_ext)
            return f"{title}{extension}"
    except Exception:
        # If anything goes wrong, return the original filename
        return os.path.splitext(os.path.basename(file_path))[0]


def copy_music_files(source_directory, destination_directory):
    """
    Copy music files to a new destination with renamed filenames.

    Args:
        source_directory (str): Path to the root directory to search
        destination_directory (str): Path to the destination directory
    """
    music_extensions = {'.mp3', '.wav', '.flac', '.m4a', '.aac', '.ogg', '.wma', '.mp4', '.m4v'}

    if not os.path.exists(source_directory):
        print(f"Error: Source directory '{source_directory}' does not exist.")
        return

    if not os.path.isdir(source_directory):
        print(f"Error: '{source_directory}' is not a directory.")
        return

    if not os.path.exists(destination_directory):
        print(f"Error: destination_directory '{destination_directory}' does not exist.")
        return

    if not os.path.isdir(destination_directory):
        print(f"Error: '{destination_directory}' is not a directory.")
        return

    print(f"Copying music files from: {source_directory}")
    print(f"To: {destination_directory}")
    print("-" * 60)

    file_count = 0
    copied_count = 0
    error_count = 0

    for root, dirs, files in os.walk(source_directory):
        for file in files:
            file_ext = os.path.splitext(file)[1].lower()
            if file_ext in music_extensions:
                file_path = os.path.join(root, file)
                prefix_to_remove = "F:/Personal backup docs\\iTunes\\iTunes Media\\Music\\"
                prefix_to_remove3 = "F:/Personal backup docs\\My Music\\iTunes\\iTunes Media\\Music\\"
                prefix_to_remove2 = "F:/Personal backup docs\\My Music\\Breezy Music Library\\iTunes Media\\Music\\"
                new_path = file_path.replace(prefix_to_remove, "")
                new_path = new_path.replace(prefix_to_remove2, "")
                new_path = new_path.replace(prefix_to_remove3, "")

                newTitle = extract_artist_title(new_path)
                destination_file = os.path.join(destination_directory, newTitle)

                try:
                    # Check if destination file already exists
                    if os.path.exists(destination_file):
                        print(f"Skipping (already exists): {newTitle}")
                    else:
                        shutil.copy2(file_path, destination_file)
                        print(f"Copied: {file} -> {newTitle}")
                        copied_count += 1
                except Exception as e:
                    print(f"Error copying {file}: {e}")
                    error_count += 1

                file_count += 1

    print("-" * 60)
    print(f"Total music files found: {file_count}")
    print(f"Files copied: {copied_count}")
    print(f"Files skipped (already exist): {file_count - copied_count - error_count}")
    print(f"Errors: {error_count}")


def main():
    source_directory = 'F:/Personal backup docs'
    destination_directory = 'H:/Dad/Music2'
    copy_music_files(source_directory, destination_directory)


if __name__ == "__main__":
    main()