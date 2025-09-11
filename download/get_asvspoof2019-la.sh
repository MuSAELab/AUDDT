#!/bin/bash
# Download ASVspoof 2019 dataset from datashare.ed.ac.uk

source ./download/config.sh

DEST="$ROOT/asvspoof2019"
mkdir -p "$DEST/raw"
mkdir -p "$DEST/processed"

wget -c -O $DEST/raw/asvspoof2019.zip https://datashare.ed.ac.uk/download/DS_10283_3336.zip
unzip -o $DEST/raw/asvspoof2019.zip -d "$DEST/processed"

echo " --- ASVspoof 2019 download complete. File saved in $DEST ---"