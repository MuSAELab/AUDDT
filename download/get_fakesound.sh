#!/bin/bash
# Download FakeSound dataset from Hugging Face

source ./download/config.sh

SRC="$ROOT/fakesound/raw"
DEST="$ROOT/fakesound/processed"

mkdir -p "$SRC"
mkdir -p "$DEST"

# Download the dataset only if it doesn't exist
if [ ! -f $SRC/FakeSound.zip ]; then
    echo "Downloading FakeSound dataset..."
    if ! wget -c -O $SRC/FakeSound.zip https://huggingface.co/datasets/ZeyuXie/FakeSound/resolve/main/FakeSound.zip; then
        echo "Error: Failed to download FakeSound dataset"
        exit 1
    fi
    echo "Download completed successfully"
fi

# Extract the dataset
echo "Extracting dataset..."
if ! unzip $SRC/FakeSound.zip -d $DEST; then
    echo "Error: Failed to extract FakeSound dataset"
    exit 1
fi

# Verify extraction was successful (check if any files were extracted)
if [ ! "$(ls -A $DEST)" ]; then
    echo "Error: No files were extracted"
    exit 1
fi

echo " --- FakeSound download complete. Files saved in $DEST ---"
