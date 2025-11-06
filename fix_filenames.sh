#!/bin/bash

# Script to rename files with query parameters in their names

echo "Renaming files with query parameters..."

# Find all files with ? in their name and rename them
find /root/k1ltr0/committed.cl/static -type f -name "*\?*" | while read -r filepath; do
    # Get directory and filename
    dir=$(dirname "$filepath")
    filename=$(basename "$filepath")

    # Remove query parameters (everything after ?)
    newfilename=$(echo "$filename" | cut -d'?' -f1)

    # Skip if it's not a valid file (like the wordfence or oembed stuff)
    if [[ "$newfilename" == "" ]] || [[ "$filename" == "?"* ]] || [[ ! "$newfilename" =~ \. ]]; then
        echo "Skipping: $filepath (not a valid file)"
        continue
    fi

    newpath="$dir/$newfilename"

    # Only rename if target doesn't exist or is smaller than source
    if [[ ! -f "$newpath" ]] || [[ $(stat -f%z "$filepath" 2>/dev/null || stat -c%s "$filepath") -gt $(stat -f%z "$newpath" 2>/dev/null || stat -c%s "$newpath") ]]; then
        echo "Renaming: $filename -> $newfilename"
        mv "$filepath" "$newpath"
    else
        echo "Removing duplicate: $filename (target exists and is larger/same)"
        rm "$filepath"
    fi
done

echo ""
echo "Cleanup complete!"
echo "Remaining files with query params: $(find /root/k1ltr0/committed.cl/static -type f -name "*\?*" | wc -l)"
