#!/bin/bash

# Download and extract the in-the-wild dataset

source ./download/config.sh

DEST="$ROOT/in-the-wild"
mkdir -p "$DEST/raw"
mkdir -p "$DEST/processed"

echo "Downloading in-the-wild dataset..."
wget --no-check-certificate "https://owncloud.fraunhofer.de/index.php/s/JZgXh0JEAF0elxa/download" -O "$DEST/raw/in-the-wild.zip"

echo "Extracting in-the-wild.zip..."
unzip -o "$DEST/raw/in-the-wild.zip" -d "$DEST/processed"

echo " --- in-the-wild dataset download and extraction complete. Files saved in $DEST --- "
