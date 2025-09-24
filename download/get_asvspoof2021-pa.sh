#!/bin/bash

# Download and extract the ASVspoof 2021 PA (Physical Access) evaluation set

source ./download/config.sh

DEST="$ROOT/asvspoof2021_pa"
mkdir -p "$DEST/raw"
mkdir -p "$DEST/processed"

echo "Downloading ASVspoof2021 PA evaluation parts..."

# There are multiple tar.gz parts
parts=(eval_part00 eval_part01 eval_part02 eval_part03 eval_part04 eval_part05 eval_part06)

for p in "${parts[@]}"; do
    wget --no-check-certificate \
        "https://zenodo.org/record/4834716/files/ASVspoof2021_PA_${p}.tar.gz?download=1" \
        -O "$DEST/raw/ASVspoof2021_PA_${p}.tar.gz"
done

echo "Extracting ASVspoof2021 PA parts..."

for p in "${parts[@]}"; do
    archive="$DEST/raw/ASVspoof2021_PA_${p}.tar.gz"
    if [ -f "$archive" ]; then
        echo "Extracting $archive ..."
        tar -xvzf "$archive" -C "$DEST/processed"
    else
        echo " Archive $archive not found, skipping."
    fi
done

echo " --- ASVspoof2021 PA dataset download & extraction complete. Files saved in $DEST ---"
