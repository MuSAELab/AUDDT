import os
import shutil
import argparse
import pandas as pd
from tqdm import tqdm

import torchaudio


def prepare_dataset(source_dir: str, label_file: str, output_path: str):
    train_val_test_splits = pd.read_csv(label_file)
    test_set = train_val_test_splits[train_val_test_splits["set"] == "test"]

    # Replace "librispeech" with "LibriSpeech" in the filename column
    test_set["filename"] = test_set["filename"]\
        .str.replace("librispeech", "LibriSpeech")\
        .str.replace("ljspeech", "LJSpeech-1.1/wavs")

    duration_list = []
    for _, row in tqdm(test_set.iterrows(), total=len(test_set), desc="Preprocessing DIFFSSD"):
        info = torchaudio.info(os.path.join(source_dir, row["filename"]))
        duration = info.num_frames / info.sample_rate
        duration_list.append(duration)

    # Save the manifest file
    test_set["duration"] = duration_list
    test_set["audio_path"] = test_set["filename"].apply(lambda x: os.path.join(source_dir, x))
    test_set["label"] = test_set["label"].apply(lambda x: "bonafide" if x == 0 else "spoof")
    test_set[["audio_path", "duration", "label"]].to_csv(output_path, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Prepare a dataset manifest for the DIFFSSD dataset."
    )
    parser.add_argument(
        '--source_dir',
        type=str,
        required=True,
        help="The root directory of the DIFFSSD dataset."
    )
    parser.add_argument(
        '--label_file',
        type=str,
        required=True,
        help="The path to the label file."
    )
    parser.add_argument(
        '--output_path',
        type=str,
        required=True,
        help="The path to save the final manifest CSV file."
    )
    
    args = parser.parse_args()
    prepare_dataset(args.source_dir, args.label_file, args.output_path)
