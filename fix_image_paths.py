#!/usr/bin/env python3
import re
from pathlib import Path

def fix_image_paths(file_path):
    """Fix image paths from /static/images/wp-content to /static/wp-content"""
    print(f"Processing: {file_path}")

    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    original_content = content

    # Replace /static/images/wp-content/uploads/ with /static/wp-content/uploads/
    content = content.replace('/static/images/wp-content/uploads/', '/static/wp-content/uploads/')

    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✓ Updated image paths")
        return True
    else:
        print(f"  No changes needed")
        return False

def main():
    base_dir = Path('/root/k1ltr0/committed.cl')

    html_files = []
    for pattern in ['index.html', '*/index.html']:
        html_files.extend(base_dir.glob(pattern))

    updated = 0
    for html_file in html_files:
        if '.bak' in str(html_file) or 'web.archive.org' in str(html_file):
            continue

        if fix_image_paths(html_file):
            updated += 1

    print(f"\nTotal files updated: {updated}")

if __name__ == '__main__':
    main()
