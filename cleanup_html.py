#!/usr/bin/env python3
import re
import sys
from pathlib import Path

def extract_original_url(archive_url):
    """Extract the original URL from an archive.org URL"""
    # Pattern: https://web.archive.org/web/TIMESTAMPmodifier/ORIGINAL_URL
    pattern = r'(?:https?:)?//web\.archive\.org/web/\d+(?:[a-z_]+)?/(https?://[^"\'>]+)'
    match = re.search(pattern, archive_url)
    if match:
        return match.group(1)
    return None

def is_committed_resource(url):
    """Check if URL is a committed.cl resource"""
    return 'committed.cl' in url

def is_external_cdn(url):
    """Check if URL is an external CDN"""
    external_domains = [
        'fonts.googleapis.com',
        's.w.org',
        'schema.org',
        'api.w.org',
        'linkedin.com',
        'player.vimeo.com'
    ]
    return any(domain in url for domain in external_domains)

def get_local_path(original_url):
    """Convert committed.cl URL to local static path"""
    # Remove protocol and domain
    path = re.sub(r'https?://committed\.cl/', '', original_url)

    # Handle specific file types
    if '.css' in path:
        filename = Path(path).name
        return f'/static/css/{filename}'
    elif '.js' in path:
        filename = Path(path).name
        return f'/static/js/{filename}'
    elif re.search(r'\.(woff|woff2|ttf|eot)', path):
        filename = Path(path).name
        return f'/static/fonts/{filename}'
    elif re.search(r'\.(jpg|jpeg|png|gif|svg|webp|ico)', path):
        # Keep directory structure for images
        return f'/static/images/{path}'
    elif 'wp-content/uploads' in path:
        return f'/static/images/{path}'
    else:
        # For other resources, try to preserve some structure
        return f'/static/{path}'

def cleanup_html(file_path):
    """Clean up archive.org URLs in an HTML file"""
    print(f"Processing: {file_path}")

    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    original_content = content
    replacements = []

    # Find all archive.org URLs
    pattern = r'((?:https?:)?//web\.archive\.org/web/\d+(?:[a-z_]+)?/https?://[^"\' >]+)'
    matches = re.findall(pattern, content)

    for archive_url in set(matches):
        original_url = extract_original_url(archive_url)
        if not original_url:
            continue

        # Determine replacement
        if is_committed_resource(original_url):
            # Replace with local path
            local_path = get_local_path(original_url)
            replacements.append((archive_url, local_path))
        elif is_external_cdn(original_url):
            # Replace with original URL
            replacements.append((archive_url, original_url))
        # else: keep archive.org URL as fallback

    # Apply replacements
    for old, new in replacements:
        content = content.replace(old, new)

    # Also handle protocol-relative URLs (//web.archive.org/...)
    content = re.sub(
        r'//web\.archive\.org/web/\d+[a-z_]*/http://fonts\.googleapis\.com/',
        'https://fonts.googleapis.com/',
        content
    )
    content = re.sub(
        r'//web\.archive\.org/web/\d+[a-z_]*/http://s\.w\.org/',
        'https://s.w.org/',
        content
    )

    if content != original_content:
        # Backup original
        backup_path = f"{file_path}.bak"
        if not Path(backup_path).exists():
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(original_content)

        # Write cleaned content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"  Updated: {len(replacements)} replacements made")
        return len(replacements)
    else:
        print(f"  No changes needed")
        return 0

def main():
    base_dir = Path('/root/k1ltr0/committed.cl')

    # Find all HTML files
    html_files = []
    for pattern in ['index.html', '*/index.html']:
        html_files.extend(base_dir.glob(pattern))

    total_replacements = 0
    for html_file in html_files:
        # Skip backup files and files in web.archive.org directories
        if '.bak' in str(html_file) or 'web.archive.org' in str(html_file):
            continue

        count = cleanup_html(html_file)
        total_replacements += count

    print(f"\n=== Summary ===")
    print(f"Total files processed: {len(html_files)}")
    print(f"Total replacements: {total_replacements}")

if __name__ == '__main__':
    main()
