#!/bin/bash

# Download and extract the JVNV dataset

source ./download/config.sh

DEST="$ROOT/jvnv"
mkdir -p "$DEST/raw"
mkdir -p "$DEST/processed"

echo "Downloading JVNV dataset..."
wget --no-check-certificate "https://ss-takashi.sakura.ne.jp/corpus/jvnv/jvnv_ver1.zip" -O "$DEST/raw/jvnv.zip"

echo "Extracting JVNV..."
unzip -o "$DEST/raw/jvnv.zip" -d "$DEST/processed"

echo " --- JVNV dataset download and extraction complete. Files saved in $DEST ---"
