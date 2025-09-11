#!/bin/bash

# Download and extract the for-rerec version of the FoR dataset


source ./config.sh

DEST="$ROOT/for-rerec"
mkdir -p "$DEST/raw"
mkdir -p "$DEST/processed"

echo "Downloading for-rerec.tar.gz..."
wget --no-check-certificate "https://bil.eecs.yorku.ca/share/for-rerec.tar.gz" -O "$DEST/for-rerec.tar.gz"

echo "Extracting for-rerec.tar.gz..."
tar -xzvf "$DEST/for-rerec.tar.gz"

echo " --- for-rerec dataset download and extraction complete. Files saved in $DEST ---"
