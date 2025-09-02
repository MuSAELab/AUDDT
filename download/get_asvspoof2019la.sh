#!/bin/bash
# Download ASVspoof 2019 dataset from datashare.ed.ac.uk

source ./download/config.sh

DEST="$ROOT/asvspoof2019"
mkdir -p "$DEST"

wget -c -O $DEST/asvspoof2019.zip https://datashare.ed.ac.uk/download/DS_10283_3336.zip
unzip -o $DEST/asvspoof2019.zip -d "$DEST"

echo " --- ASVspoof 2019 download complete. File saved in $DEST ---"