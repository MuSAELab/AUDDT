#!/bin/bash

# Download and extract the for-norm version of the FoR dataset


source ./config.sh

DEST="$ROOT/for-norm"
mkdir -p "$DEST/raw"
mkdir -p "$DEST/processed"

echo "Downloading for-norm.tar.gz..."
wget --no-check-certificate "https://bil.eecs.yorku.ca/share/for-norm.tar.gz" -O "$DEST/for-norm.tar.gz"


echo "Extracting for-norm.tar.gz..."
tar -xzvf "$DEST/raw/for-norm.tar.gz" -C "$DEST/processed"

echo "--- for-norm dataset download and extraction complete. Files saved in $DEST ---"
