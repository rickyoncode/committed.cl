#!/usr/bin/env python3
import re
from pathlib import Path

def extract_original_url(archive_url):
    """Extract the original URL from an archive.org URL"""
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

def strip_query_params(path):
    """Remove query parameters from path"""
    return path.split('?')[0]

def get_local_path(original_url):
    """Convert committed.cl URL to local static path (without query params)"""
    # Remove protocol and domain
    path = re.sub(r'https?://committed\.cl/', '', original_url)

    # Strip query parameters
    path = strip_query_params(path)

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
        return f'/static/images/{path}'
    elif 'wp-content/uploads' in path:
        return f'/static/images/{path}'
    else:
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
            local_path = get_local_path(original_url)
            replacements.append((archive_url, local_path))
        elif is_external_cdn(original_url):
            # Strip query params from external URLs too
            clean_url = strip_query_params(original_url)
            replacements.append((archive_url, clean_url))

    # Apply replacements
    for old, new in replacements:
        content = content.replace(old, new)

    # Handle protocol-relative URLs
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
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  Updated: {len(replacements)} replacements made")
        return len(replacements)
    else:
        print(f"  No changes needed")
        return 0

def main():
    base_dir = Path('/root/k1ltr0/committed.cl')

    html_files = []
    for pattern in ['index.html', '*/index.html']:
        html_files.extend(base_dir.glob(pattern))

    total_replacements = 0
    for html_file in html_files:
        if '.bak' in str(html_file) or 'web.archive.org' in str(html_file):
            continue

        count = cleanup_html(html_file)
        total_replacements += count

    print(f"\n=== Summary ===")
    print(f"Total files processed: {len([f for f in html_files if '.bak' not in str(f)])}")
    print(f"Total replacements: {total_replacements}")

if __name__ == '__main__':
    main()
