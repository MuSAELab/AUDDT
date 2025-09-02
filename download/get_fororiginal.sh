#!/bin/bash

# Download and extract the for-original version of the FoR dataset

source ./download/config.sh

DEST="$ROOT/for-original"
mkdir -p "$DEST"

echo "Downloading for-original.tar.gz..."
wget --no-check-certificate "https://bil.eecs.yorku.ca/share/for-original.tar.gz" -O "$DEST/for-original.tar.gz"

echo "Extracting for-original.tar.gz..."
tar -xzvf "$DEST/for-original.tar.gz"

echo "--- for-original dataset download and extraction complete. Files saved in $DEST ---"
