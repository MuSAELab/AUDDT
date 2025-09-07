#!/bin/bash
# Download DECRO dataset from Zenodo (record 7603208)
# Note: Download speed for this dataset, via wget, is very slow.

source ./download/config.sh

DEST="$ROOT/decro/raw"
mkdir -p "$DEST"

# Download the dataset only if it doesn't exist
if [ ! -f $DEST/DECRO-dataset-v1.2.zip ]; then
    echo "Downloading DECRO dataset..."
    if ! wget -c -O $DEST/DECRO-dataset-v1.2.zip https://zenodo.org/records/7603208/files/petrichorwq/DECRO-dataset-v1.2.zip; then
        echo "Error: Failed to download DECRO dataset"
        exit 1
    fi
    echo "Download completed successfully"
fi

# Extract the dataset
echo "Extracting dataset..."
if ! unzip $DEST/DECRO-dataset-v1.2.zip -d $DEST; then
    echo "Error: Failed to extract DECRO dataset"
    exit 1
fi

# Verify extraction was successful (check if any files were extracted)
if [ ! "$(ls -A $DEST)" ]; then
    echo "Error: No files were extracted"
    exit 1
fi

# Remove the zip file only after successful extraction
rm $DEST/DECRO-dataset-v1.2.zip

echo " --- DECRO download complete. Files saved in $DEST ---"
