#!/usr/bin/env python3
import re
from pathlib import Path

def cleanup_js_objects(file_path):
    """Clean up archive.org URLs in JavaScript objects"""
    print(f"Processing: {file_path}")

    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    original_content = content
    count = 0

    # Fix wpemojiSettings baseUrl and svgUrl
    content = re.sub(
        r'"baseUrl":"https:\\/\\/web\.archive\.org\\/web\\/\d+\\/https:\\/\\/s\.w\.org\\/([^"]+)"',
        r'"baseUrl":"https://s.w.org/\1"',
        content
    )
    content = re.sub(
        r'"svgUrl":"https:\\/\\/web\.archive\.org\\/web\\/\d+\\/https:\\/\\/s\.w\.org\\/([^"]+)"',
        r'"svgUrl":"https://s.w.org/\1"',
        content
    )
    content = re.sub(
        r'"concatemoji":"https:\\/\\/web\.archive\.org\\/web\\/\d+\\/https:\\/\\/committed\.cl\\/([^"]+)"',
        r'"concatemoji":"/static/\1"',
        content
    )

    # Fix wpcf7 apiSettings
    content = re.sub(
        r'"root":"https:\\/\\/web\.archive\.org\\/web\\/\d+\\/https:\\/\\/committed\.cl\\/([^"]+)"',
        r'"root":"https://committed.cl/\1"',
        content
    )

    # Fix tel: and mailto: links
    content = re.sub(
        r'https://web\.archive\.org/web/\d+/tel:',
        'tel:',
        content
    )
    content = re.sub(
        r'https://web\.archive\.org/web/\d+/mailto:',
        'mailto:',
        content
    )

    # Fix $us.templateDirectoryUri
    content = re.sub(
        r"\$us\.templateDirectoryUri = '//web\.archive\.org/web/\d+/http://committed\.cl/wp-content/themes/Impreza'",
        r"$us.templateDirectoryUri = '/static/wp-content/themes/Impreza'",
        content
    )

    # Fix jsFileLocation in RevSlider
    content = re.sub(
        r'jsFileLocation:"//web\.archive\.org/web/\d+/http://committed\.cl/([^"]+)"',
        r'jsFileLocation:"/static/\1"',
        content
    )

    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  Updated JavaScript objects")
        return 1
    else:
        print(f"  No JavaScript objects to update")
        return 0

def main():
    base_dir = Path('/root/k1ltr0/committed.cl')

    html_files = []
    for pattern in ['index.html', '*/index.html']:
        html_files.extend(base_dir.glob(pattern))

    total = 0
    for html_file in html_files:
        if '.bak' in str(html_file) or 'web.archive.org' in str(html_file):
            continue

        count = cleanup_js_objects(html_file)
        total += count

    print(f"\nTotal files updated: {total}")

if __name__ == '__main__':
    main()
