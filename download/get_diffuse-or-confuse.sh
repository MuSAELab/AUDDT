#!/bin/bash

# Download and extract the Diffuse or Confuse dataset

source ./download/config.sh

DEST="$ROOT/diffuse_or_confuse"
mkdir -p "$DEST/raw"
mkdir -p "$DEST/processed"

# Download each zip part
echo "Downloading dataset_01.zip..."
wget --no-check-certificate "https://zenodo.org/record/15260248/files/dataset_01.zip" -O "$DEST/raw/dataset_01.zip"

echo "Downloading dataset_02.zip..."
wget --no-check-certificate "https://zenodo.org/record/15260248/files/dataset_02.zip" -O "$DEST/raw/dataset_02.zip"

echo "Downloading dataset_03.zip..."
wget --no-check-certificate "https://zenodo.org/record/15260248/files/dataset_03.zip" -O "$DEST/raw/dataset_03.zip"

echo "Downloading dataset_04.zip..."
wget --no-check-certificate "https://zenodo.org/record/15260248/files/dataset_04.zip" -O "$DEST/raw/dataset_04.zip"

echo "Downloading metadata.zip..."
wget --no-check-certificate "https://zenodo.org/record/15260248/files/metadata.zip" -O "$DEST/raw/metadata.zip"

# Extract all zip files into the processed folder
echo "Extracting dataset_01.zip..."
unzip -o "$DEST/raw/dataset_01.zip" -d "$DEST/processed/dataset_01"

echo "Extracting dataset_02.zip..."
unzip -o "$DEST/raw/dataset_02.zip" -d "$DEST/processed/dataset_02"

echo "Extracting dataset_03.zip..."
unzip -o "$DEST/raw/dataset_03.zip" -d "$DEST/processed/dataset_03"

echo "Extracting dataset_04.zip..."
unzip -o "$DEST/raw/dataset_04.zip" -d "$DEST/processed/dataset_04"

echo "Extracting metadata.zip..."
unzip -o "$DEST/raw/metadata.zip" -d "$DEST/processed/metadata"

echo " --- Diffuse or Confuse dataset download and extraction complete. Files saved in $DEST ---"
