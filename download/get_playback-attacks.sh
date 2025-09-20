#!/bin/bash

# Extracts the playback attacks dataset from Mendeley

source ./download/config.sh

DEST="$ROOT/playback_attacks"
mkdir -p "$DEST/raw"
mkdir -p "$DEST/processed"

# Assume you have already downloaded the combined ZIP as playback_attacks.zip
if [ -f "$DEST/raw/playback_attacks.zip" ]; then
  echo "Extracting playback_attacks.zip..."
  unzip -o "$DEST/raw/playback_attacks.zip" -d "$DEST/processed"
  echo "Dataset extraction complete. Files are in $DEST/processed"
else
  echo "  playback_attacks.zip not found in $PWD."
  echo "  Please download the dataset manually from:"
  echo "  https://data.mendeley.com/datasets/5t56sjbgf6/2"
  echo "  and place the ZIP file here before running this script."
  exit 1
fi
