#!/bin/bash
# Download VCapAV dataset from Hugging Face

source ./download/config.sh

DEST="$ROOT/vcapav"
mkdir -p "$DEST"

mkdir -p "$DEST/audioLDM1_audio_cut"
mkdir -p "$DEST/audioLDM2_audio_cut"
mkdir -p "$DEST/audiocraft_audio_cut"
mkdir -p "$DEST/V2A_mlp_audio_cut"
mkdir -p "$DEST/V2A_mapper_audio_cut"
mkdir -p "$DEST/VGGsound_test_14923_audio_cut"

wget -c https://huggingface.co/datasets/WailyWang/VCapAV/resolve/main/T2A/audioLDM1_audio_cut.zip
unzip audioLDM1_audio_cut.zip -d audioLDM1_audio_cut/
rm audioLDM1_audio_cut.zip

wget -c https://huggingface.co/datasets/WailyWang/VCapAV/resolve/main/T2A/audioLDM2_audio_cut.zip
unzip audioLDM2_audio_cut.zip -d audioLDM2_audio_cut/
rm audioLDM2_audio_cut.zip

wget -c https://huggingface.co/datasets/WailyWang/VCapAV/resolve/main/T2A/audiocraft_audio_cut.zip
unzip audiocraft_audio_cut.zip -d audiocraft_audio_cut/
rm audiocraft_audio_cut.zip

wget -c https://huggingface.co/datasets/WailyWang/VCapAV/resolve/main/V2A/V2A_mlp_audio_cut.zip
unzip V2A_mlp_audio_cut.zip -d V2A_mlp_audio_cut/
rm V2A_mlp_audio_cut.zip

wget -c https://huggingface.co/datasets/WailyWang/VCapAV/resolve/main/V2A/V2A_mapper_audio_cut.zip
unzip V2A_mapper_audio_cut.zip -d V2A_mapper_audio_cut/
rm V2A_mapper_audio_cut.zip

wget -c https://huggingface.co/datasets/WailyWang/VCapAV/resolve/main/VGGsound_test_14923_audio_cut.zip
unzip VGGsound_test_14923_audio_cut.zip -d VGGsound_test_14923_audio_cut/
rm VGGsound_test_14923_audio_cut.zip


echo " --- VCapAV download complete. Files saved in $DEST ---"
