#!/bin/bash

# Use earlier timestamp that works: 20180814171407
TIMESTAMP="20180814171407"
BASE_DIR="/root/k1ltr0/committed.cl/static"

# Create directories
mkdir -p "$BASE_DIR/wp-content/uploads/2017/05"
mkdir -p "$BASE_DIR/wp-content/uploads/2017/06"

echo "Downloading missing images with timestamp $TIMESTAMP..."

# Download key images
declare -A images=(
    # 2017/05 images
    ["concrete_seamless.png"]="wp-content/uploads/2017/05"
    ["SHADOW-1.png"]="wp-content/uploads/2017/05"
    ["LOGO_COMMITTED_NOSOTROS.png"]="wp-content/uploads/2017/05"
    ["LOGO_COMMITTED_NOSOTROS-300x209.png"]="wp-content/uploads/2017/05"
    ["HOME-01.jpg"]="wp-content/uploads/2017/05"
    ["HOME-01-300x167.jpg"]="wp-content/uploads/2017/05"
    ["HOME-01-600x333.jpg"]="wp-content/uploads/2017/05"
    ["HOME-01-768x427.jpg"]="wp-content/uploads/2017/05"
    ["HOME-02.jpg"]="wp-content/uploads/2017/05"
    ["HOME-02-300x167.jpg"]="wp-content/uploads/2017/05"
    ["HOME-02-600x333.jpg"]="wp-content/uploads/2017/05"
    ["HOME-02-768x427.jpg"]="wp-content/uploads/2017/05"
    ["HOME-03.jpg"]="wp-content/uploads/2017/05"
    ["HOME-03-300x167.jpg"]="wp-content/uploads/2017/05"
    ["HOME-03-600x333.jpg"]="wp-content/uploads/2017/05"
    ["HOME-03-768x427.jpg"]="wp-content/uploads/2017/05"
    # 2017/06 images
    ["SLIDER-HOME-04.jpg"]="wp-content/uploads/2017/06"
    ["SLIDER-HOME-05.jpg"]="wp-content/uploads/2017/06"
    ["SLIDER-HOME-06.jpg"]="wp-content/uploads/2017/06"
)

downloaded=0
failed=0

for filename in "${!images[@]}"; do
    dir="${images[$filename]}"
    target="$BASE_DIR/$dir/$filename"

    # Skip if already exists
    if [[ -f "$target" ]]; then
        echo "SKIP: $filename (already exists)"
        continue
    fi

    # Try to download
    url="https://web.archive.org/web/${TIMESTAMP}im_/http://committed.cl/$dir/$filename"
    echo "Downloading: $filename"

    if wget -q -T 10 -t 2 "$url" -O "$target" 2>/dev/null; then
        if [[ -s "$target" ]]; then
            echo "  ✓ SUCCESS"
            ((downloaded++))
        else
            echo "  ✗ FAILED (empty)"
            rm -f "$target"
            ((failed++))
        fi
    else
        echo "  ✗ FAILED (wget error)"
        rm -f "$target"
        ((failed++))
    fi
done

echo ""
echo "Summary:"
echo "  Downloaded: $downloaded"
echo "  Failed: $failed"
