#!/bin/bash
# Download TIMIT-TTS dataset from Zenodo (record 6560159)
# Note: Download speed for this dataset, via wget, is very slow.

source ./download/config.sh

DEST="$ROOT/timittts/raw"
mkdir -p "$DEST"

# Download the dataset only if it doesn't exist
if [ ! -f $DEST/TIMIT-TTS.zip ]; then
    echo "Downloading TIMIT-TTS dataset..."
    if ! wget -c -O $DEST/TIMIT-TTS.zip https://zenodo.org/records/6560159/files/TIMIT-TTS.zip; then
        echo "Error: Failed to download TIMIT-TTS dataset"
        exit 1
    fi
    echo "Download completed successfully"
fi

# Extract the dataset
echo "Extracting dataset..."
if ! unzip $DEST/TIMIT-TTS.zip -d $DEST; then
    echo "Error: Failed to extract TIMIT-TTS dataset"
    exit 1
fi

# Verify extraction was successful (check if any files were extracted)
if [ ! "$(ls -A $DEST)" ]; then
    echo "Error: No files were extracted"
    exit 1
fi

# Remove the zip file only after successful extraction
rm $DEST/TIMIT-TTS.zip

echo " --- TIMIT-TTS download complete. Files saved in $DEST ---"