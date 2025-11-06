#!/usr/bin/env python3
import re
from pathlib import Path

def fix_duplicate_paths(file_path):
    """Fix duplicate wp-content/uploads in paths"""
    print(f"Processing: {file_path}")

    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    original_content = content

    # Fix duplicate wp-content/uploads paths
    content = content.replace(
        '/static/wp-content/uploads/wp-content/uploads/',
        '/static/wp-content/uploads/'
    )

    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✓ Fixed duplicate paths")
        return True
    else:
        print(f"  No duplicates found")
        return False

def main():
    base_dir = Path('/root/k1ltr0/committed.cl')
    pages = ['servicios', 'galeria', 'contacto', 'clientes']

    fixed = 0
    for page in pages:
        html_file = base_dir / page / 'index.html'
        if html_file.exists():
            if fix_duplicate_paths(html_file):
                fixed += 1

    print(f"\nTotal files fixed: {fixed}")

if __name__ == '__main__':
    main()
