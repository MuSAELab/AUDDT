#!/bin/bash

# Download and extract the CVoiceFake-Full dataset (Zenodo 14062964)

source ./download/config.sh

DEST="$ROOT/cvoicefake"
mkdir -p "$DEST/raw"
mkdir -p "$DEST/processed"

echo "Downloading CVoiceFake-Full dataset parts..."

# Download all parts of CVoiceFake_Large
for i in {0..9}; do
    wget -c "https://zenodo.org/records/14062964/files/CVoiceFake_Large.tar.gz.$i?download=1" \
        -O "$DEST/raw/CVoiceFake_Large.tar.gz.$i"
done

# Download all parts of diffwave update
for i in {0..1}; do
    wget -c "https://zenodo.org/records/14062964/files/CVoiceFake_Large_diffwave_update.tar.gz.0$i?download=1" \
        -O "$DEST/raw/CVoiceFake_Large_diffwave_update.tar.gz.0$i"
done

echo "Combining CVoiceFake_Large parts..."
cat $DEST/raw/CVoiceFake_Large.tar.gz.* > $DEST/raw/CVoiceFake_Large.tar.gz

echo "Extracting CVoiceFake_Large..."
tar -xzvf "$DEST/raw/CVoiceFake_Large.tar.gz" -C "$DEST/processed"

echo "Combining diffwave update parts..."
cat $DEST/raw/CVoiceFake_Large_diffwave_update.tar.gz.* > $DEST/raw/CVoiceFake_Large_diffwave_update.tar.gz

echo "Extracting diffwave update..."
tar -xzvf "$DEST/raw/CVoiceFake_Large_diffwave_update.tar.gz" -C "$DEST/processed"

echo " --- CVoiceFake-Full dataset download and extraction complete. Files saved in $DEST ---"
