#!/bin/bash

# Script to normalize all UFO files recursively
# Usage: ./normalize_ufo.sh [directory]
# If no directory is specified, uses current directory

# Set the target directory (default to current directory if not specified)
TARGET_DIR="${1:-.}"

echo "Normalizing UFO files in: $TARGET_DIR"
echo "=================================="

# Counter for processed files
count=0

# Find all .ufo directories recursively and process them
while IFS= read -r -d '' ufo_dir; do
    echo "Processing: $ufo_dir"
    if ufonormalizer "$ufo_dir"; then
        echo "✓ Successfully normalized: $ufo_dir"
        ((count++))
    else
        echo "✗ Failed to normalize: $ufo_dir"
    fi
    echo "---"
done < <(find "$TARGET_DIR" -name "*.ufo" -type d -print0)

echo "=================================="
echo "Normalization complete!"
echo "Processed $count UFO files"
