#!/bin/bash

MAPPING_FILE="/root/k1ltr0/committed.cl/url_mapping.txt"
DOWNLOAD_LOG="/root/k1ltr0/committed.cl/download_log.txt"
BASE_DIR="/root/k1ltr0/committed.cl"

> "$DOWNLOAD_LOG"

downloaded=0
skipped=0
failed=0

while IFS='|' read -r archive_url local_path; do
    # Convert local path to filesystem path
    full_path="${BASE_DIR}${local_path}"

    # Skip if file already exists
    if [ -f "$full_path" ]; then
        echo "SKIP: $full_path (already exists)" >> "$DOWNLOAD_LOG"
        ((skipped++))
        continue
    fi

    # Create parent directory
    mkdir -p "$(dirname "$full_path")"

    # Download file with timeout and retries
    echo "Downloading: $archive_url -> $full_path"
    if wget -T 10 -t 2 -q "$archive_url" -O "$full_path" 2>/dev/null; then
        # Verify file was downloaded and has content
        if [ -s "$full_path" ]; then
            echo "SUCCESS: $archive_url -> $full_path" >> "$DOWNLOAD_LOG"
            ((downloaded++))
        else
            echo "FAILED: $archive_url (empty file)" >> "$DOWNLOAD_LOG"
            rm -f "$full_path"
            ((failed++))
        fi
    else
        echo "FAILED: $archive_url" >> "$DOWNLOAD_LOG"
        rm -f "$full_path"
        ((failed++))
    fi

    # Small delay to avoid hammering the server
    sleep 0.2
done < "$MAPPING_FILE"

echo ""
echo "Download Summary:"
echo "  Downloaded: $downloaded"
echo "  Skipped (already exist): $skipped"
echo "  Failed: $failed"
echo ""
echo "See $DOWNLOAD_LOG for details"
