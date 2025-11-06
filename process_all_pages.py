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
    """Convert committed.cl URL to local static path"""
    path = re.sub(r'https?://committed\.cl/', '', original_url)
    path = strip_query_params(path)

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
        return f'/static/wp-content/uploads/{path}' if 'wp-content/uploads' in path else f'/static/images/{path}'
    elif 'wp-content/uploads' in path:
        return f'/static/wp-content/uploads/{path}'
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

        if is_committed_resource(original_url):
            local_path = get_local_path(original_url)
            replacements.append((archive_url, local_path))
        elif is_external_cdn(original_url):
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

    # Fix JavaScript objects
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
    content = re.sub(
        r'"root":"https:\\/\\/web\.archive\.org\\/web\\/\d+\\/https:\\/\\/committed\.cl\\/([^"]+)"',
        r'"root":"https://committed.cl/\1"',
        content
    )
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
    content = re.sub(
        r"\$us\.templateDirectoryUri = '//web\.archive\.org/web/\d+/http://committed\.cl/wp-content/themes/Impreza'",
        r"$us.templateDirectoryUri = '/static/wp-content/themes/Impreza'",
        content
    )
    content = re.sub(
        r'jsFileLocation:"//web\.archive\.org/web/\d+/http://committed\.cl/([^"]+)"',
        r'jsFileLocation:"/static/\1"',
        content
    )

    # Fix image paths
    content = content.replace('/static/images/wp-content/uploads/', '/static/wp-content/uploads/')

    if content != original_content:
        # Backup original
        backup_path = f"{file_path}.bak"
        if not Path(backup_path).exists():
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(original_content)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✓ Updated: {len(replacements)} URL replacements + JS objects")
        return len(replacements)
    else:
        print(f"  No changes needed")
        return 0

def main():
    base_dir = Path('/root/k1ltr0/committed.cl')

    # Process specific pages
    pages = ['servicios', 'galeria', 'contacto', 'clientes']

    total_replacements = 0
    for page in pages:
        html_file = base_dir / page / 'index.html'
        if html_file.exists():
            count = cleanup_html(html_file)
            total_replacements += count
        else:
            print(f"Skip: {page}/index.html (not found)")

    print(f"\n=== Summary ===")
    print(f"Total replacements: {total_replacements}")

if __name__ == '__main__':
    main()
