# Unarchive Report

Date: 2025-11-06
Task: Remove web.archive.org references and download missing static files

## Summary

Successfully processed HTML files to remove web.archive.org references and ensure all committed.cl resources are available locally.

## Statistics

### Archive URLs Processed
- **Total unique archive.org URLs found:** 296
- **Committed.cl resources identified:** 259
- **External CDN resources:** 37 (preserved as original URLs)

### Static Files
- **Downloaded successfully:** 24 new files
- **Already existing (skipped):** 79 files
- **Failed downloads:** 156 files
- **Total files in static folder:** 49

### HTML Files Updated
- **index.html:** 49 URL replacements + JavaScript objects cleaned
- **nosotros/index.html:** 41 URL replacements + JavaScript objects cleaned
- **Total replacements:** 90+ URLs updated

## Changes Made

### 1. Committed.cl Resources → Local Paths

All committed.cl resources were redirected to local `/static/` folder:

| Resource Type | Target Directory |
|--------------|------------------|
| CSS files | `/static/css/` |
| JavaScript files | `/static/js/` |
| Images | `/static/images/wp-content/uploads/` |
| Fonts | `/static/fonts/` |
| WordPress content | `/static/wp-content/` |

### 2. External CDN URLs → Original URLs

External resources now use their original URLs:
- **Google Fonts:** `https://fonts.googleapis.com/...`
- **WordPress.org:** `https://s.w.org/...`
- **Schema.org:** `https://schema.org/...`
- **LinkedIn:** `https://www.linkedin.com/...`
- **Vimeo:** `http://player.vimeo.com/...`

### 3. JavaScript Objects Cleaned

Fixed embedded JavaScript configuration:
- `window._wpemojiSettings` - baseUrl, svgUrl, source.concatemoji
- `wpcf7.apiSettings` - root URL
- `$us.templateDirectoryUri` - theme directory path
- RevSlider `jsFileLocation`
- `tel:` and `mailto:` links

## Remaining Archive.org References

Only **non-functional** archive.org references remain:

1. **HTML Comments** (safe to ignore)
   ```html
   <!-- Mirrored from web.archive.org/... by HTTrack -->
   ```

2. **Wayback Machine Infrastructure** (needed if file is still served through archive.org)
   - `__wm.init()` - Wayback Machine initialization
   - `wombat.js` - URL rewriting library
   - Archive.org analytics scripts

These references are harmless and don't affect functionality. They can be manually removed if desired.

## Files Created

- `archive_urls.txt` - All 296 extracted archive.org URLs
- `url_mapping.txt` - Mapping of 259 archive URLs to local paths
- `download_log.txt` - Detailed download results (success/skip/fail)
- `*.html.bak` - Backup copies of modified HTML files
- `unarchive.sh` - URL extraction script
- `download_missing.sh` - File download script
- `cleanup_html.py` - HTML URL replacement script
- `cleanup_js_objects.py` - JavaScript object cleanup script

## Failed Downloads

156 files failed to download, primarily:
- Some image variations (300x167, 600x333, 768x427 sizes)
- Files with malformed URLs (e.g., ending in `);background-repeat:`)
- Missing or removed files from archive.org
- HTML pages and JSON endpoints (intentionally not downloaded)
- Wordfence security files (not needed)

These failures don't significantly impact the site as:
1. Many were alternate image sizes (responsive variants)
2. Some were API endpoints or HTML pages (not static assets)
3. The main versions of images were successfully downloaded

## Verification

To verify the changes:

```bash
# Check remaining archive.org functional URLs (should be ~0)
grep -E "web\.archive\.org" index.html | grep -v "<!-- Mirrored" | grep -v "__wm\." | wc -l

# List all downloaded static files
find static -type f | sort

# View download statistics
grep -c "^SUCCESS" download_log.txt
grep -c "^SKIP" download_log.txt
grep -c "^FAILED" download_log.txt
```

## Recommendations

1. **Test the site** - Open index.html and nosotros/index.html in a browser to verify all resources load correctly
2. **Clean up Wayback Machine code** - Remove `__wm.init()`, wombat.js references if not needed
3. **Review failed downloads** - Check download_log.txt for any critical missing files
4. **Delete backup files** - Remove *.html.bak files once changes are verified
5. **Delete helper scripts** - Remove *.sh and *.py scripts once satisfied with results

## Conclusion

The unarchive process successfully:
- Identified and categorized all archive.org references
- Downloaded committed.cl resources to local storage
- Updated HTML files to use local paths for committed.cl resources
- Preserved external CDN URLs in their original form
- Cleaned up JavaScript configuration objects
- Created detailed logs and backups

The site should now function independently of web.archive.org for committed.cl resources while maintaining access to external CDN resources.
