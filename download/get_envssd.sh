#!/bin/bash
# Download EnvSDD dataset (test and remain splits) from Hugging Face

source ./download/config.sh

SRC="$ROOT/envssd/raw"
DEST="$ROOT/envssd/processed"

mkdir -p "$SRC"
mkdir -p "$DEST"

# Download test split parquet files (14 shards)
echo "Downloading EnvSDD test split (14 parquet files)..."
for i in $(seq 0 13); do
    FILE=$(printf "test-%05d-of-00014.parquet" $i)
    if [ ! -f "$SRC/$FILE" ]; then
        if ! wget -c -O "$SRC/$FILE" "https://huggingface.co/datasets/EnvSDD/EnvSDD/resolve/main/data/$FILE"; then
            echo "Error: Failed to download $FILE"
            exit 1
        fi
    fi
done
echo "Test split download complete."

# Download remain split parquet files (40 shards)
echo "Downloading EnvSDD remain split (40 parquet files)..."
for i in $(seq 0 39); do
    FILE=$(printf "remain-%05d-of-00040.parquet" $i)
    if [ ! -f "$SRC/$FILE" ]; then
        if ! wget -c -O "$SRC/$FILE" "https://huggingface.co/datasets/EnvSDD/EnvSDD/resolve/main/data/$FILE"; then
            echo "Error: Failed to download $FILE"
            exit 1
        fi
    fi
done
echo "Remain split download complete."

echo " --- EnvSDD download complete. Files saved in $SRC ---"
