# prints all files by relative path

import os
from pathlib import Path

# Root directory to scan
SOURCE_PATH = 'D:/Pictures/'
SOURCE_PATH = 'H:/JKW_BKUP/Pictures/'

OUTPUT_FILE = 'file_list.txt'

def save_relative_file_paths(root_dir, output_file):
    root_path = Path(root_dir).resolve()
    file_count = 0
    lines = []

    for current_path, _, files in os.walk(root_path):
        for file in sorted(files):
            full_path = Path(current_path) / file
            relative_path = full_path.relative_to(root_path)
            lines.append(relative_path.as_posix())
            file_count += 1

    with open(output_file, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line + '\n')
        f.write(f'{file_count} files\n')

    print(f'File list saved to {output_file}')

save_relative_file_paths(SOURCE_PATH, OUTPUT_FILE)
