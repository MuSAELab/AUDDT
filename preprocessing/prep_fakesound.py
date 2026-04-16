# First, download the dataset from Hugging Face:
# https://huggingface.co/datasets/ZeyuXie/FakeSound/resolve/main/FakeSound.zip
# Insert the zip file in a folder called "fakesound/raw" inside your data root
# Unzip the compressed file and insert in a folder called "fakesound/processed" inside your data root.
# In the end, your folder structure should be like this:
#
# data_root/
#  ├── fakesound/
#  │   ├── raw/
#  │   │   └── FakeSound.zip
#  │   ├── processed/
#  │   │   └── FakeSound/
#  │   │       ├── audio_data/
#  │   │       │   ├── easy/*.wav
#  │   │       │   ├── hard/*.wav
#  │   │       │   └── zeroshot/*.wav
#  │   │       └── meta_data/
#  │   └── manifest_fakesound.csv
#  └── ...
# Note: the manifest_fakesound.csv file will be created with this script
# Note: This dataset contains only fake (spoof) audio samples.
#       Only test splits (easy, hard, zeroshot) are used; train is excluded.

import io
import os
import argparse
import pandas as pd
from glob import glob
from tqdm import tqdm

import torchaudio


def prepare_dataset(source_dir: str, output_path: str):
    # Only include test splits (easy, hard, zeroshot), exclude train
    test_splits = ["easy", "hard", "zeroshot"]
    test_files = []
    for split in test_splits:
        split_dir = os.path.join(source_dir, "FakeSound", "audio_data", split)
        test_files.extend(glob(os.path.join(split_dir, "*.wav")))

    test_set = pd.DataFrame(test_files, columns=["audio_path"])
    test_set["label"] = "spoof"

    duration_list = []
    for _, row in tqdm(test_set.iterrows(), total=len(test_set), desc="Preprocessing FakeSound"):
        info = torchaudio.info(row["audio_path"])
        duration = info.num_frames / info.sample_rate
        duration_list.append(duration)

    # Save the manifest file
    test_set["duration"] = duration_list
    test_set[["audio_path", "duration", "label"]].to_csv(output_path, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Prepare a dataset manifest for the FakeSound dataset."
    )
    parser.add_argument(
        '--source_dir',
        type=str,
        required=True,
        help="The root directory of the FakeSound dataset."
    )
    parser.add_argument(
        '--output_path',
        type=str,
        required=True,
        help="The path to save the final manifest CSV file."
    )

    args = parser.parse_args()
    prepare_dataset(args.source_dir, args.output_path)
