#!/bin/bash
# Download SRC4VC dataset from Zenodo (record 14498691)
# Note: Download speed for this dataset, via wget, is very slow.

source ./download/config.sh

SRC="$ROOT/src4vc/raw"
DEST="$ROOT/src4vc/processed"

mkdir -p "$SRC"
mkdir -p "$DEST"

# Download the dataset only if it doesn't exist
if [ ! -f $SRC/SRC4VC_ver1.zip ]; then
    echo "Downloading SRC4VC dataset..."
    if ! wget -c -O $SRC/SRC4VC_ver1.zip http://sython.org/Corpus/SRC4VC/SRC4VC_ver1.zip; then
        echo "Error: Failed to download SRC4VC dataset"
        exit 1
    fi
    echo "Download completed successfully"
fi

# Extract the dataset
echo "Extracting dataset..."
if ! unzip $SRC/SRC4VC_ver1.zip -d $DEST; then
    echo "Error: Failed to extract SRC4VC dataset"
    exit 1
fi

# Verify extraction was successful (check if any files were extracted)
if [ ! "$(ls -A $DEST)" ]; then
    echo "Error: No files were extracted"
    exit 1
fi

echo " --- SRC4VC download complete. Files saved in $DEST ---"