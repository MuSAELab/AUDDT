#!/bin/bash
# Download WaveFake dataset from Zenodo (record 5642694)
# Note: Download speed for this dataset, via wget, is very slow.

source ./download/config.sh

SRC="$ROOT/wavefake/raw"
DEST="$ROOT/wavefake/processed"

mkdir -p "$SRC"
mkdir -p "$DEST"

# Download the dataset only if it doesn't exist
if [ ! -f $SRC/generated_audio.zip ]; then
    echo "Downloading WaveFake dataset..."
    if ! wget -c -O $SRC/generated_audio.zip https://zenodo.org/records/5642694/files/generated_audio.zip; then
        echo "Error: Failed to download WaveFake dataset"
        exit 1
    fi
    echo "Download completed successfully"
fi

# Extract the dataset
echo "Extracting dataset..."
if ! unzip $SRC/generated_audio.zip -d $DEST; then
    echo "Error: Failed to extract TIMIT-TTS dataset"
    exit 1
fi

# Verify extraction was successful (check if any files were extracted)
if [ ! "$(ls -A $DEST)" ]; then
    echo "Error: No files were extracted"
    exit 1
fi

echo " --- WaveFake download complete. Files saved in $DEST ---"
