#!/bin/bash
# Download ASVspoof5 dataset from Zenodo (record 14498691)

source ./download/config.sh

DEST="$ROOT/asvspoof5"
mkdir -p "$DEST/raw"
mkdir -p "$DEST/processed"

# label and readme files
wget -c -O $DEST/raw/LICENSE.txt https://zenodo.org/record/14498691/files/LICENSE.txt
wget -c -O $DEST/raw/README.txt https://zenodo.org/record/14498691/files/README.txt
wget -c -O $DEST/raw/ASVspoof5_protocols.tar.gz https://zenodo.org/record/14498691/files/ASVspoof5_protocols.tar.gz

tar -xzf $DEST/raw/ASVspoof5_protocols.tar.gz -C "$DEST/processed"

# Evaluation split
for file in flac_E_aa.tar flac_E_ab.tar flac_E_ac.tar flac_E_ad.tar flac_E_ae.tar \
            flac_E_af.tar flac_E_ag.tar flac_E_ah.tar; do
    wget -c -O $DEST/raw/$file https://zenodo.org/record/14498691/files/$file
    tar -xf $DEST/raw/$file -C "$DEST/processed"
done

################################
# We do not include training and development sets for evaluation, as they are typically used for training.
################################

echo " --- ASVspoof5 download complete. Files saved in $DEST ---"
