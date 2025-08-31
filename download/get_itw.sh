#!/bin/bash

# Download and extract the in-the-wild dataset


source ./config.sh

DEST="$ROOT/in-the-wild"
mkdir -p "$DEST"
cd "$DEST" || exit


echo "Downloading in-the-wild dataset..."
wget --no-check-certificate "https://owncloud.fraunhofer.de/index.php/s/JZgXh0JEAF0elxa/download" -O "in-the-wild.zip"


echo "Extracting in-the-wild.zip..."
unzip -o "in-the-wild.zip" -d "$DEST"

echo " --- in-the-wild dataset download and extraction complete. Files saved in $DEST --- "
