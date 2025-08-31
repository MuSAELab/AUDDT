#!/bin/bash

# Download and extract the for-norm version of the FoR dataset


source ./config.sh

DEST="$ROOT/for-norm"
mkdir -p "$DEST"
cd "$DEST" || exit


echo "Downloading for-norm.tar.gz..."
wget --no-check-certificate "https://bil.eecs.yorku.ca/share/for-norm.tar.gz" -O "for-norm.tar.gz"


echo "Extracting for-norm.tar.gz..."
tar -xzvf "for-norm.tar.gz"

echo "--- for-norm dataset download and extraction complete. Files saved in $DEST ---"
