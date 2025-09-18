#!/bin/bash
# Download CTR-SVDD dataset from Zenodo (record 12703261)
# Note: Download speed for this dataset, via wget, is very slow.

source ./download/config.sh

DEST="$ROOT/ctrsvdd/raw"
mkdir -p "$DEST"

# Download the dataset only if it doesn't exist
if [ ! -f $DEST/test_set.zip ]; then
    echo "Downloading CTR-SVDD dataset..."
    if ! wget -c -O $DEST/test_set.zip https://zenodo.org/records/12703261/files/test_set.zip; then
        echo "Error: Failed to download CTR-SVDD dataset"
        exit 1
    fi
    wget -c -O $DEST/test.txt https://zenodo.org/records/12703261/files/test.txt
    echo "Download completed successfully"
fi

# Extract the dataset
echo "Extracting dataset..."
if ! unzip $DEST/test_set.zip -d $DEST; then
    echo "Error: Failed to extract CTR-SVDD dataset"
    exit 1
fi

# Verify extraction was successful (check if any files were extracted)
if [ ! "$(ls -A $DEST)" ]; then
    echo "Error: No files were extracted"
    exit 1
fi

# Remove the zip file only after successful extraction
rm $DEST/test_set.zip

echo " --- CTR-SVDD download complete. Files saved in $DEST ---"
