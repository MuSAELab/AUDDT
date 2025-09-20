#!/bin/bash
# TODO: have not figured out a clean way to download this one..

source ./download/config.sh

DEST="$ROOT/habla"
mkdir -p "$DEST/raw"
mkdir -p "$DEST/processed"

# Download the dataset using gdown
echo "Downloading HABLA dataset..."
# gdown --folder "https://drive.google.com/drive/folders/1hEYYt1LHuCxsT8fgNyVfbegDl1zSkIUJ" \
#       -O "$DEST/processed" --remaining-ok

gdown 10HeHTCCMJAYVoUAlZyV6B4oJP7JISPQz -O $DEST/raw/protocol.txt

echo " --- Download and extraction of HABLA complete. Files are in $DEST ---"

