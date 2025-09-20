#!/bin/bash

# Download and extract the SpoofCeleb dataset

source ./download/config.sh

DEST="$ROOT/spoofceleb"
mkdir -p "$DEST/raw"
mkdir -p "$DEST/processed"

echo "Downloading SpoofCeleb dataset parts..."

# Use HF CLI to download
# You must be logged in via huggingface-cli and have access
# huggingface-cli download jungjee/spoofceleb --repo-type dataset --local-dir $DEST/raw/spoofceleb


# Alternatively, if you know exact part filenames, you could loop them:
# parts=(spoofceleb.tar.gzaa spoofceleb.tar.gzab spoofceleb.tar.gzac ... spoofceleb.tar.gzaj)
# for p in "${parts[@]}"; do
#   echo "Downloading part $p..."
#   wget -c "https://huggingface.co/datasets/jungjee/spoofceleb/resolve/main/$p" -O "$DEST/raw/$p"
# done

echo "Combining parts..."
cat $DEST/raw/spoofceleb/spoofceleb.tar.gz* > $DEST/raw/spoofceleb_full.tar.gz

echo "Extracting SpoofCeleb..."
tar -xvzf "$DEST/raw/spoofceleb_full.tar.gz" -C "$DEST/processed"

echo " --- SpoofCeleb dataset download and extraction complete. Files saved in $DEST ---"
