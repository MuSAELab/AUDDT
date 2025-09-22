#!/bin/bash
# Download DFADD dataset from Hugging Face

source ./download/config.sh

DEST="$ROOT/dfadd/raw"
mkdir -p "$DEST"

# label and readme files
wget -c -O $DEST/test-00000-of-00002.parquet https://huggingface.co/datasets/isjwdu/DFADD/resolve/main/data/test-00000-of-00002.parquet
wget -c -O $DEST/test-00001-of-00002.parquet https://huggingface.co/datasets/isjwdu/DFADD/resolve/main/data/test-00001-of-00002.parquet

echo " --- DFADD download complete. Files saved in $DEST ---"
