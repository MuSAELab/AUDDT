#!/bin/bash
# TODO: have not figured out a clean way to download this one..

source ./download/config.sh

DEST="$ROOT/habla"
mkdir -p "$DEST"


REMOTE_NAME="gdrive"
FOLDER_ID="1hEYYt1LHuCxsT8fgNyVfbegDl1zSkIUJ"


echo "Starting HABLA download via rclone..."
rclone copy "$REMOTE_NAME":"$FOLDER_ID" "$DEST" --progress --transfers 16 --checkers 16

for zipfile in "$DEST"/*.zip; do
    [ -f "$zipfile" ] || continue
    echo "Extracting $zipfile..."
    unzip -o "$zipfile" -d "$DEST"
done

echo " --- HABLA download and extraction complete ---"
