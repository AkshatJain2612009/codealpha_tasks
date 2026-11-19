'''\
Automation Script for Multiple Small Tasks

Features:
- Move all .jpg files from a source directory to a destination directory.
- Extract all email addresses from a .txt file and write them to an output file.
- Scrape the title of a given webpage URL and save it to a text file.

Usage examples:
    python automation.py move --src ./images --dst ./photos
    python automation.py extract-emails --input emails.txt --output extracted.txt
    python automation.py scrape-title --url https://example.com --output title.txt

The script uses only the standard library for file operations and the
'requests' package for the web‑scraping part.
'''\

import argparse
import os
import re
import shutil
import sys
from pathlib import Path

# Optional import: requests is not in the stdlib but is allowed per the task description.
try:
    import requests
except ImportError:
    print("The 'requests' library is required for the scrape-title command.")
    print("Install it with: pip install requests")
    sys.exit(1)


def move_jpg_files(src: Path, dst: Path) -> None:
    """Move all *.jpg files from *src* to *dst*.

    The function creates *dst* if it does not exist.
    """
    if not src.is_dir():
        raise ValueError(f"Source directory does not exist: {src}")
    dst.mkdir(parents=True, exist_ok=True)
    for jpg_path in src.glob('*.jpg'):
        target = dst / jpg_path.name
        shutil.move(str(jpg_path), str(target))
        print(f"Moved: {jpg_path} → {target}")


def extract_emails(input_file: Path, output_file: Path) -> None:
    """Extract email addresses from *input_file* and write them to *output_file*.

    One email per line, duplicates removed while preserving order.
    """
    email_pattern = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
    seen = set()
    with input_file.open('r', encoding='utf-8') as f_in, output_file.open('w', encoding='utf-8') as f_out:
        for line in f_in:
            for match in email_pattern.findall(line):
                if match not in seen:
                    seen.add(match)
                    f_out.write(match + "\n")
                    print(f"Found email: {match}")
    print(f"Extracted {len(seen)} unique email(s) to {output_file}")


def scrape_title(url: str, output_file: Path) -> None:
    """Fetch *url* and save the HTML <title> contents to *output_file*.
    """
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    # Simple regex to capture the title tag. Not robust for edge‑cases but fine for a fixed page.
    title_match = re.search(r"<title>(.*?)</title>", response.text, re.IGNORECASE | re.DOTALL)
    if title_match:
        title = title_match.group(1).strip()
        output_file.write_text(title, encoding='utf-8')
        print(f"Title saved to {output_file}: {title}")
    else:
        print("No <title> tag found on the page.")
        sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(description="Small automation utilities.")
    subparsers = parser.add_subparsers(dest='command', required=True)

    # move command
    move_parser = subparsers.add_parser('move', help='Move .jpg files from src to dst')
    move_parser.add_argument('--src', required=True, type=Path, help='Source directory')
    move_parser.add_argument('--dst', required=True, type=Path, help='Destination directory')

    # extract-emails command
    email_parser = subparsers.add_parser('extract-emails', help='Extract emails from a text file')
    email_parser.add_argument('--input', required=True, type=Path, help='Input .txt file')
    email_parser.add_argument('--output', required=True, type=Path, help='Output file for extracted emails')

    # scrape-title command
    scrape_parser = subparsers.add_parser('scrape-title', help='Scrape the <title> of a webpage')
    scrape_parser.add_argument('--url', required=True, help='Web page URL')
    scrape_parser.add_argument('--output', required=True, type=Path, help='File to store the title')

    args = parser.parse_args()

    if args.command == 'move':
        move_jpg_files(args.src, args.dst)
    elif args.command == 'extract-emails':
        extract_emails(args.input, args.output)
    elif args.command == 'scrape-title':
        scrape_title(args.url, args.output)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()

