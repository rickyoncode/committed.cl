#!/bin/bash

# Script to extract and download all web.archive.org resources
# and create a mapping file for replacement

OUTPUT_FILE="/root/k1ltr0/committed.cl/archive_urls.txt"
MAPPING_FILE="/root/k1ltr0/committed.cl/url_mapping.txt"

# Clear previous outputs
> "$OUTPUT_FILE"
> "$MAPPING_FILE"

# Find all HTML files
find /root/k1ltr0/committed.cl -name "*.html" -type f | while read -r htmlfile; do
    echo "Processing: $htmlfile"

    # Extract all web.archive.org URLs
    grep -oE '(https?:)?//web\.archive\.org/web/[0-9]+[a-z_]*/https?://[^"'\''> ]+' "$htmlfile" | sort -u >> "$OUTPUT_FILE"
done

# Sort and deduplicate
sort -u "$OUTPUT_FILE" -o "$OUTPUT_FILE"

echo "Extracted $(wc -l < "$OUTPUT_FILE") unique archive.org URLs"

# Parse URLs and create mapping
while IFS= read -r archiveurl; do
    # Remove leading // if present
    archiveurl="${archiveurl#//}"

    # Ensure https://
    if [[ ! "$archiveurl" =~ ^https?:// ]]; then
        archiveurl="https://$archiveurl"
    fi

    # Extract original URL from archive.org URL
    # Pattern: https://web.archive.org/web/TIMESTAMPmodifier/ORIGINAL_URL
    if [[ "$archiveurl" =~ web\.archive\.org/web/[0-9]+([a-z_]+)?/(https?://.+)$ ]]; then
        modifier="${BASH_REMATCH[1]}"
        original="${BASH_REMATCH[2]}"

        # Determine if it's a committed.cl resource
        if [[ "$original" =~ committed\.cl/ ]]; then
            # Extract path after committed.cl
            path_part="${original#*committed.cl/}"

            # Determine file type and target directory
            if [[ "$path_part" =~ \.css ]]; then
                target="/static/css/$(basename "$path_part")"
            elif [[ "$path_part" =~ \.js ]]; then
                target="/static/js/$(basename "$path_part")"
            elif [[ "$path_part" =~ \.(woff|woff2|ttf|eot) ]]; then
                target="/static/fonts/$(basename "$path_part")"
            elif [[ "$path_part" =~ \.(jpg|jpeg|png|gif|svg|webp|ico) ]]; then
                # Keep directory structure for images
                target="/static/images/$path_part"
            else
                # Other files
                target="/static/$path_part"
            fi

            echo "$archiveurl|$target" >> "$MAPPING_FILE"
        fi
    fi
done < "$OUTPUT_FILE"

echo "Created mapping for $(wc -l < "$MAPPING_FILE") committed.cl resources"
