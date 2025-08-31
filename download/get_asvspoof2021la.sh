#!/bin/bash

# Download and extract ASVspoof 2021 LA dataset from Zenodo (record 4837263)

source ./download/config.sh

DEST="$ROOT/asvspoof2021_la"
mkdir -p "$DEST"
cd "$DEST" || exit

wget -c -O ASVspoof2021_LA_eval.tar.gz https://zenodo.org/record/4837263/files/ASVspoof2021_LA_eval.tar.gz

# Verify checksum (optional but recommended by the organizer)
echo "2abee34d8b0b91159555fc4f016e4562  ASVspoof2021_LA_eval.tar.gz" | md5sum -c -

tar -xzf ASVspoof2021_LA_eval.tar.gz -C "$DEST"

echo " --- ASVspoof 2021 LA download and extraction complete. Files saved in $DEST ---"
