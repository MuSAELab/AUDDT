#!/bin/bash

# Download and extract ASVspoof 2021 DF dataset from Zenodo (record 4835108)

source ./download/config.sh

DEST="$ROOT/asvspoof2021_df"
mkdir -p "$DEST/raw"
mkdir -p "$DEST/processed"

for i in {00..03}; do
    wget -c -O $DEST/raw/ASVspoof2021_DF_eval_part$i.tar.gz \
        "https://zenodo.org/record/4835108/files/ASVspoof2021_DF_eval_part$i.tar.gz"
done

# Verify checksums (optional but recommended by the organizers)
declare -A checksums=(
    [00]="4f2cbae07cf3ede2a1dde3b8d2ee55ea"
    [01]="1578c89ab433c2b60b1dce93bdf8fbec"
    [02]="5497a35f0126e94a1d7a7d26db57b4f7"
    [03]="42b7512ba2943e98a32a53c9608cf83c"
)

for i in {00..03}; do
    echo "${checksums[$i]}  $DEST/raw/ASVspoof2021_DF_eval_part$i.tar.gz" | md5sum -c -
done


for i in {00..03}; do
    tar -xzf $DEST/raw/ASVspoof2021_DF_eval_part$i.tar.gz -C "$DEST/processed"
done

echo " --- ASVspoof 2021 DF download and extraction complete. Files saved in $DEST ---"
