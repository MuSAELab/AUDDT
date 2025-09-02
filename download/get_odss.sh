#!/bin/bash

# Download and extract the ODSS dataset

source ./download/config.sh

DEST="$ROOT/odss"
mkdir -p "$DEST"

echo "Downloading ODSS dataset..."
wget -O $DEST/odss.zip "https://zenodo.org/records/8370669/files/ODSS.zip?download=1"

echo "Extracting odss.zip..."
unzip -o "$DEST/odss.zip" -d "$DEST"

echo " --- ODSS dataset download and extraction complete. Files saved in $DEST ---"
