import os
import sys
from pathlib import Path
from xml.sax.saxutils import escape

def get_recent_mp3s(directory, limit=50):
    mp3_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.mp3', '.wma', '.m4a')):
                full_path = Path(root) / file
                try:
                    # mtime = os.path.getmtime(full_path)  # Use ctime on Windows if desired
                    mtime = full_path.stat().st_mtime
                    mp3_files.append((mtime, full_path))
                except Exception as e:
                    print(f"Error accessing {full_path}: {e}")
    print(mp3_files[:limit])
    # Sort files by modified time (newest first)
    mp3_files.sort(key=lambda x: x[0], reverse=True)
    # Convert paths to uniform forward-slash format
    return [str(path.as_posix()) for _, path in mp3_files[:limit]]

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
        # Escape XML special characters
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

    parser = argparse.ArgumentParser(description="Create a playlist of the 50 most recently modified mp3 files.")
    parser.add_argument(
        "--directory",
        help="Directory to search for MP3 files",
        default="D:/Music/Int/Country"
    )
    parser.add_argument(
        "--output",
        help="Output playlist file (e.g., recent_playlist.wpl)",
        default="D:/Music/Playlists/country-recent50-2025-05.wpl"
    )
    args = parser.parse_args()

    if os.path.exists(args.output):
        print(f"Playlist file '{args.output}' already exists. Exiting without changes.")
        sys.exit(0)

    recent_mp3s = get_recent_mp3s(args.directory, limit=50)
    print('\n'.join(recent_mp3s))
    save_to_wpl(recent_mp3s, args.output)
    print(f"Saved playlist with {len(recent_mp3s)} files to {args.output}")
