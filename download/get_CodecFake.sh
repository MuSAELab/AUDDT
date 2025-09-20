#!/bin/bash

# Download CodecFake_wavs dataset from Hugging Face

source ./download/config.sh

DEST="$ROOT/CodecFake"
mkdir -p "$DEST/raw"
mkdir -p "$DEST/processed"

# echo "Cloning CodecFake dataset from Hugging Face..."
# git lfs install
# git clone https://huggingface.co/datasets/rogertseng/CodecFake_wavs $DEST/raw

# Find all .zip archives and extract them into their own subfolder
find "$DEST/raw" -type f -name "*.zip" | while read archive; do
    base=$(basename "$archive" .zip)           # e.g. train_part1.zip → train_part1
    outdir="$DEST/processed/$base"
    mkdir -p "$outdir"
    echo "Extracting $archive into $outdir ..."
    unzip -o "$archive" -d "$outdir"
    # Optional: remove archive after extraction
    # rm "$archive"
done

echo " --- Download and extraction of CodecFake complete. Files are in $DEST ---"
