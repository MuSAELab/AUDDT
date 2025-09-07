#!/bin/bash
# Download DIFFSSD dataset from Hugging Face

source ./download/config.sh

DEST="$ROOT/diffssd/raw"
mkdir -p "$DEST"

# Download the generated data
if [ ! -d $DEST/generated_speech ]; then
    wget -c -O $DEST/generated_speech.tar https://huggingface.co/datasets/purdueviperlab/diffssd/resolve/main/generated_speech.tar
    tar -xzvf $DEST/generated_speech.tar -C $DEST
    rm $DEST/generated_speech.tar
fi

# Download the real data
if [ ! -d $DEST/real_speech/LJSpeech-1.1 ]; then
    mkdir -p $DEST/real_speech
    wget -c -O $DEST/real_speech/LJSpeech-1.1.tar.bz2 https://data.keithito.com/data/speech/LJSpeech-1.1.tar.bz2
    tar -xvjf $DEST/real_speech/LJSpeech-1.1.tar.bz2 -C $DEST/real_speech
    rm $DEST/real_speech/LJSpeech-1.1.tar.bz2
fi

if [ ! -d $DEST/real_speech/LibriSpeech ]; then
    wget -c -O $DEST/real_speech/dev-clean.tar.gz https://openslr.trmal.net/resources/12/dev-clean.tar.gz
    wget -c -O $DEST/real_speech/dev-other.tar.gz https://openslr.trmal.net/resources/12/dev-other.tar.gz
    wget -c -O $DEST/real_speech/test-clean.tar.gz https://openslr.trmal.net/resources/12/test-clean.tar.gz
    wget -c -O $DEST/real_speech/test-other.tar.gz https://openslr.trmal.net/resources/12/test-other.tar.gz

    tar -xzvf $DEST/real_speech/dev-clean.tar.gz -C $DEST/real_speech
    tar -xzvf $DEST/real_speech/dev-other.tar.gz -C $DEST/real_speech
    tar -xzvf $DEST/real_speech/test-clean.tar.gz -C $DEST/real_speech
    tar -xzvf $DEST/real_speech/test-other.tar.gz -C $DEST/real_speech

    rm $DEST/real_speech/dev-clean.tar.gz
    rm $DEST/real_speech/dev-other.tar.gz
    rm $DEST/real_speech/test-clean.tar.gz
    rm $DEST/real_speech/test-other.tar.gz
fi

# Download the train_val_test_splits.csv file
if [ ! -f $DEST/train_val_test_splits.csv ]; then
    wget -c -O $DEST/train_val_test_splits.csv https://huggingface.co/datasets/purdueviperlab/diffssd/resolve/main/train_val_test_splits.csv
fi

chmod -R 755 $DEST

echo " --- DIFFSSD download complete. Files saved in $DEST ---"
