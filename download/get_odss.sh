#!/bin/bash

# Download and extract the ODSS dataset

source ./download/config.sh

DEST="$ROOT/odss"
mkdir -p "$DEST/raw"
mkdir -p "$DEST/processed"

echo "Downloading ODSS dataset..."
wget -O $DEST/raw/odss.zip "https://zenodo.org/records/8370669/files/ODSS.zip?download=1"

echo "Extracting odss.zip..."
unzip -o "$DEST/raw/odss.zip" -d "$DEST/processed"

echo " --- ODSS dataset download and extraction complete. Files saved in $DEST ---"
