#!/bin/bash

# Download CodecFake_wavs dataset from Hugging Face

source ./download/config.sh

DEST="$ROOT/CodecFake"
mkdir -p "$DEST/raw"
mkdir -p "$DEST/processed"

# echo "Cloning CodecFake dataset from Hugging Face..."
# git lfs install
# git clone https://huggingface.co/datasets/rogertseng/CodecFake_wavs $DEST/raw


# Find all .zip archives and extract them in place
find "$DEST/raw" -type f -name "*.zip" | while read archive; do
    echo "Extracting $archive..."
    unzip -o "$archive" -d $DEST/processed
    # Optional: remove archive after extraction
    # rm "$archive"
done

echo " --- Download and extraction of CodecFake complete. Files are in $DEST. ---"