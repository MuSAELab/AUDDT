#!/bin/bash

# Download and extract the for-rerec version of the FoR dataset

source ./download/config.sh

DEST="$ROOT/for-rerec"
mkdir -p "$DEST/raw"
mkdir -p "$DEST/processed"

echo "Downloading for-rerec.tar.gz..."
wget --no-check-certificate "https://bil.eecs.yorku.ca/share/for-rerec.tar.gz" -O "$DEST/raw/for-rerec.tar.gz"

echo "Extracting for-rerec.tar.gz..."
tar -xzvf "$DEST/raw/for-rerec.tar.gz" -C "$DEST/processed"

echo " --- for-rerec dataset download and extraction complete. Files saved in $DEST ---"
