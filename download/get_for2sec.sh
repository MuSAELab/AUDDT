#!/bin/bash

# Download and extract the for-2sec version of the FoR dataset


source ./config.sh

DEST="$ROOT/for-2sec"
mkdir -p "$DEST"
cd "$DEST" || exit


echo "Downloading for-2sec.tar.gz..."
wget --no-check-certificate "https://bil.eecs.yorku.ca/share/for-2sec.tar.gz" -O "for-2sec.tar.gz"


echo "Extracting for-2sec.tar.gz..."
tar -xzvf "for-2sec.tar.gz"

echo " --- for-2sec dataset download and extraction complete. Files saved in $DEST ---"
