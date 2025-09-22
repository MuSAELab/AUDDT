#!/bin/bash
# Download DIFFSSD dataset from Hugging Face

source ./download/config.sh

SRC="$ROOT/diffssd/raw"
DEST="$ROOT/diffssd/processed"

mkdir -p "$SRC"
mkdir -p "$DEST"

# Download the generated data
if [ ! -f $SRC/generated_speech.tar ]; then
    wget -c -O $SRC/generated_speech.tar https://huggingface.co/datasets/purdueviperlab/diffssd/resolve/main/generated_speech.tar
fi
tar -xzvf $SRC/generated_speech.tar -C $DEST

# Download the real data
mkdir -p $SRC/real_speech
mkdir -p $DEST/real_speech

if [ ! -f $SRC/real_speech/LJSpeech-1.1.tar.bz2 ]; then
    wget -c -O $SRC/real_speech/LJSpeech-1.1.tar.bz2 https://data.keithito.com/data/speech/LJSpeech-1.1.tar.bz2
fi
tar -xvjf $SRC/real_speech/LJSpeech-1.1.tar.bz2 -C $DEST/real_speech

if [ ! -f $SRC/real_speech/dev-clean.tar.gz ]; then
    wget -c -O $SRC/real_speech/dev-clean.tar.gz https://openslr.trmal.net/resources/12/dev-clean.tar.gz
fi
tar -xzvf $SRC/real_speech/dev-clean.tar.gz -C $DEST/real_speech

if [ ! -f $SRC/real_speech/dev-other.tar.gz ]; then
    wget -c -O $SRC/real_speech/dev-other.tar.gz https://openslr.trmal.net/resources/12/dev-other.tar.gz
fi
tar -xzvf $SRC/real_speech/dev-other.tar.gz -C $DEST/real_speech

if [ ! -f $SRC/real_speech/test-clean.tar.gz ]; then
    wget -c -O $SRC/real_speech/test-clean.tar.gz https://openslr.trmal.net/resources/12/test-clean.tar.gz
fi
tar -xzvf $SRC/real_speech/test-clean.tar.gz -C $DEST/real_speech

if [ ! -f $SRC/real_speech/test-other.tar.gz ]; then
    wget -c -O $SRC/real_speech/test-other.tar.gz https://openslr.trmal.net/resources/12/test-other.tar.gz
fi
tar -xzvf $SRC/real_speech/test-other.tar.gz -C $DEST/real_speech

# Download the train_val_test_splits.csv file
if [ ! -f $DEST/train_val_test_splits.csv ]; then
    wget -c -O $DEST/train_val_test_splits.csv https://huggingface.co/datasets/purdueviperlab/diffssd/resolve/main/train_val_test_splits.csv
fi

chmod -R 755 $DEST

echo " --- DIFFSSD download complete. Files saved in $DEST ---"
