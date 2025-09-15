#!/bin/bash

# Download and extract the Codecfake dataset (ONLY test sets) from Zenodo

source ./download/config.sh

DEST="$ROOT/Codecfake"
mkdir -p "$DEST/raw"
mkdir -p "$DEST/processed"

# echo "Downloading label file..."
# wget -c -O "$DEST/raw/label.zip" "https://zenodo.org/records/13838106/files/label.zip?download=1"
# unzip -o "$DEST/raw/label.zip" -d "$DEST/processed"

# echo "Starting download of Codecfake Test sets..."
# # -------------------------------
# # Test set (part 1 of 2)
# # -------------------------------
# echo "Downloading Codecfake test set part 1 (Codec + ALM test: C1-C6 & A1-A3)..."

# wget -c -O "$DEST/raw/codecfake_test_part1.zip" "https://zenodo.org/records/13838823/files/C1.zip?download=1"
# wget -c -O "$DEST/raw/C2.zip" "https://zenodo.org/records/13838823/files/C2.zip?download=1"
# wget -c -O "$DEST/raw/C3.zip" "https://zenodo.org/records/13838823/files/C3.zip?download=1"
# wget -c -O "$DEST/raw/C4.zip" "https://zenodo.org/records/13838823/files/C4.zip?download=1"
# wget -c -O "$DEST/raw/C5.zip" "https://zenodo.org/records/13838823/files/C5.zip?download=1"
# wget -c -O "$DEST/raw/C6.zip" "https://zenodo.org/records/13838823/files/C6.zip?download=1"
# wget -c -O "$DEST/raw/A1.zip" "https://zenodo.org/records/13838823/files/A1.zip?download=1"
# wget -c -O "$DEST/raw/A2.zip" "https://zenodo.org/records/13838823/files/A2.zip?download=1"
# wget -c -O "$DEST/raw/A3.zip" "https://zenodo.org/records/13838823/files/A3.zip?download=1"

# # -------------------------------
# # Test set (part 2 of 2)
# # -------------------------------
# echo "Downloading Codecfake test set part 2 (Codec unseen test: C7.zip)..."
# wget -c -O "$DEST/raw/C7.zip" "https://zenodo.org/records/11125029/files/C7.zip?download=1"


# echo "Extracting Codecfake datasets..."

# test_parts=(C1 C2 C3 C4 C5 C6 C7 A1 A2 A3)

# for part in "${test_parts[@]}"; do
#   if [ -f "$DEST/raw/$part.zip" ]; then
#     echo "Extracting $part.zip..."
#     unzip -o "$DEST/raw/$part.zip" -d "$DEST/processed"
#   else
#     echo "$part.zip not found in $DEST/raw, skipping."
#   fi
# done

mv $DEST/processed/A3_fake $DEST/processed/A3

echo "--- Codecfake (test sets) download and extraction complete. Files saved in $DEST ---"

