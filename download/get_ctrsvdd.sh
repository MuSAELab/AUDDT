#!/bin/bash
# Download CTR-SVDD dataset from Zenodo (record 12703261)
# Note: Download speed for this dataset, via wget, is very slow.

source ./download/config.sh

SRC="$ROOT/ctrsvdd/raw"
DEST="$ROOT/ctrsvdd/processed"

mkdir -p "$SRC"
mkdir -p "$DEST"

# Download the dataset only if it doesn't exist
if [ ! -f $SRC/test_set.zip ]; then
    echo "Downloading CTR-SVDD dataset..."
    if ! wget -c -O $SRC/test_set.zip https://zenodo.org/records/12703261/files/test_set.zip; then
        echo "Error: Failed to download CTR-SVDD dataset"
        exit 1
    fi
    wget -c -O $DEST/test.txt https://zenodo.org/records/12703261/files/test.txt
    echo "Label file downloaded successfully"
fi

# Extract the dataset
echo "Extracting dataset..."
if ! unzip $SRC/test_set.zip -d $DEST; then
    echo "Error: Failed to extract CTR-SVDD dataset"
    exit 1
fi

# Verify extraction was successful (check if any files were extracted)
if [ ! "$(ls -A $DEST)" ]; then
    echo "Error: No files were extracted"
    exit 1
fi

echo " --- CTR-SVDD download complete. Files saved in $DEST ---"
