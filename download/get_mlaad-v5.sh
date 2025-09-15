#!/bin/bash

# part of this is the download script copied from https://owncloud.fraunhofer.de/index.php/s/tL2Y1FKrWiX4ZtP#editor

source ./download/config.sh

DEST="$ROOT/mlaad-v5"
mkdir -p "$DEST/raw"
mkdir -p "$DEST/processed"

# echo "Commencing download of MLAAD V5 data"

# # Download files with proper handling for redirection and filenames
# wget --content-disposition -O $DEST/raw/mlaad_v5.zip.md5 "https://owncloud.fraunhofer.de/index.php/s/tL2Y1FKrWiX4ZtP/download?path=%2Fv5&files=mlaad_v5.zip.md5"
# wget --content-disposition -O $DEST/raw/mlaad_v5.zip "https://owncloud.fraunhofer.de/index.php/s/tL2Y1FKrWiX4ZtP/download?path=%2Fv5&files=mlaad_v5.zip"
# wget --content-disposition -O $DEST/raw/mlaad_v5.z01 "https://owncloud.fraunhofer.de/index.php/s/tL2Y1FKrWiX4ZtP/download?path=%2Fv5&files=mlaad_v5.z01"
# wget --content-disposition -O $DEST/raw/mlaad_v5.z02 "https://owncloud.fraunhofer.de/index.php/s/tL2Y1FKrWiX4ZtP/download?path=%2Fv5&files=mlaad_v5.z02"
# wget --content-disposition -O $DEST/raw/mlaad_v5.z03 "https://owncloud.fraunhofer.de/index.php/s/tL2Y1FKrWiX4ZtP/download?path=%2Fv5&files=mlaad_v5.z03"
# wget --content-disposition -O $DEST/raw/mlaad_v5.z04 "https://owncloud.fraunhofer.de/index.php/s/tL2Y1FKrWiX4ZtP/download?path=%2Fv5&files=mlaad_v5.z04"
# wget --content-disposition -O $DEST/raw/mlaad_v5.z05 "https://owncloud.fraunhofer.de/index.php/s/tL2Y1FKrWiX4ZtP/download?path=%2Fv5&files=mlaad_v5.z05"
# wget --content-disposition -O $DEST/raw/mlaad_v5.z06 "https://owncloud.fraunhofer.de/index.php/s/tL2Y1FKrWiX4ZtP/download?path=%2Fv5&files=mlaad_v5.z06"
# wget --content-disposition -O $DEST/raw/mlaad_v5.z07 "https://owncloud.fraunhofer.de/index.php/s/tL2Y1FKrWiX4ZtP/download?path=%2Fv5&files=mlaad_v5.z07"
# wget --content-disposition -O $DEST/raw/mlaad_v5.z08 "https://owncloud.fraunhofer.de/index.php/s/tL2Y1FKrWiX4ZtP/download?path=%2Fv5&files=mlaad_v5.z08"
# wget --content-disposition -O $DEST/raw/mlaad_v5.z09 "https://owncloud.fraunhofer.de/index.php/s/tL2Y1FKrWiX4ZtP/download?path=%2Fv5&files=mlaad_v5.z09"
# wget --content-disposition -O $DEST/raw/mlaad_v5.z10 "https://owncloud.fraunhofer.de/index.php/s/tL2Y1FKrWiX4ZtP/download?path=%2Fv5&files=mlaad_v5.z10"

# echo "Checking integrity of downloaded files"

# # Ensure the MD5 file references the correct filenames
# md5sum -c $DEST/raw/mlaad_v5.zip.md5

# # Unzip
# 7z x $DEST/raw/mlaad_v5.zip meta.csv -o$DEST/processed

### Download real ones from M-AILABS; this takes 110GB space

# List of languages
# langs=(de_DE en_UK en_US es_ES it_IT uk_UK ru_RU fr_FR pl_PL)
langs=(en_US)

for lang in "${langs[@]}"; do
  echo "Downloading $lang..."
  wget -O "$DEST/raw/$lang.tgz" "https://ics.tau-ceti.space/data/Training/stt_tts/$lang.tgz"
done

# Extract loop
for lang in "${langs[@]}"; do
  archive="$DEST/raw/$lang.tgz"
  if [ -f "$archive" ]; then
    echo "Extracting $archive..."
    mkdir -P "$DEST/processed/real"
    tar -xvzf "$archive" -C "$DEST/processed/real"
  else
    echo "$archive not found, skipping extraction."
  fi
done

echo " --- MLAAD-v5 dataset download and extraction complete. Files saved in $DEST ---"
