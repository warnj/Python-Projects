import os
import sys
from pathlib import Path
import random
from xml.sax.saxutils import escape

def get_recent_mp3s(directory, limit=50, recursive=True):
    mp3_files = []
    if recursive:
        print('using recursive directory exploration')
        walker = os.walk(directory)
    else:
        print('using non-recursive directory exploration')
        walker = [(directory, [], os.listdir(directory))]

    for root, _, files in walker:
        for file in files:
            if file.lower().endswith(('.mp3', '.wma', '.m4a')):
                full_path = Path(root) / file
                try:
                    mtime = full_path.stat().st_mtime
                    mp3_files.append((mtime, full_path))
                except Exception as e:
                    print(f"Error accessing {full_path}: {e}")
    mp3_files.sort(key=lambda x: x[0], reverse=True)
    return [str(path.as_posix()) for _, path in mp3_files[:limit]]

def get_random_mp3s(directory, limit=50, recursive=True):
    mp3_files = []
    if recursive:
        print('Using recursive directory exploration')
        walker = os.walk(directory)
    else:
        print('Using non-recursive directory exploration')
        walker = [(directory, [], os.listdir(directory))]

    for root, _, files in walker:
        for file in files:
            if file.lower().endswith(('.mp3', '.wma', '.m4a')):
                full_path = Path(root) / file
                mp3_files.append(full_path)

    if len(mp3_files) <= limit:
        selected = mp3_files
    else:
        selected = random.sample(mp3_files, limit)

    return [str(path.as_posix()) for path in selected]

def save_to_wpl(file_paths, output_path):
    title = Path(output_path).stem  # Use file name without extension as title
    lines = [
        '<?wpl version="1.0"?>',
        '<smil>',
        '  <head>',
        f'    <title>{escape(title)}</title>',
        '  </head>',
        '  <body>',
        '    <seq>'
    ]
    for path in file_paths:
        windows_path = str(Path(path))
        lines.append(f'      <media src="{escape(windows_path)}" />')
    lines.extend([
        '    </seq>',
        '  </body>',
        '</smil>'
    ])
    with open(output_path, 'w', encoding='utf-8', newline='\r\n') as f:
        f.write('\n'.join(lines))

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Create a playlist of the most recently modified MP3 files.")
    parser.add_argument("--directory", help="Directory to search for MP3 files", default="D:/Music/Int/Country")
    parser.add_argument("--output", help="Output playlist file (e.g., recent_playlist.wpl)", default="D:/Music/Playlists/country-random50-2025-05.wpl")
    parser.add_argument("--limit", type=int, help="Maximum number of recent files to include", default=50)
    parser.add_argument("--recursive", action="store_true", help="Search subdirectories recursively", default=False)
    parser.add_argument("--random", action="store_true", help="Select random files instead of most recent", default=True)
    args = parser.parse_args()

    if os.path.exists(args.output):
        print(f"Playlist file '{args.output}' already exists. Exiting without changes.")
        sys.exit(0)

    if args.random:
        selected_mp3s = get_random_mp3s(args.directory, limit=args.limit, recursive=args.recursive)
    else:
        selected_mp3s = get_recent_mp3s(args.directory, limit=args.limit, recursive=args.recursive)

    print('\n'.join(selected_mp3s))
    save_to_wpl(selected_mp3s, args.output)
    print(f"Saved playlist with {len(selected_mp3s)} files to {args.output}")
