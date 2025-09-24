#!/bin/bash

# Download and extract the ODSS dataset

source ./download/config.sh

DEST="$ROOT/odss"
mkdir -p "$DEST/raw"
mkdir -p "$DEST/processed"

echo "Downloading ODSS dataset..."
wget --no-check-certificate "https://zenodo.org/records/8370669/files/odss.zip?download=1" -O $DEST/raw/odss.zip

echo "Extracting odss.zip..."
unzip -o "$DEST/raw/odss.zip" -d "$DEST/processed"

echo " --- ODSS dataset download and extraction complete. Files saved in $DEST ---"
