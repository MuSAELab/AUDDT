import io
import os
import argparse
import pandas as pd
from glob import glob
from tqdm import tqdm

import torchaudio


def prepare_dataset(source_dir: str, label_file: str, output_path: str):
    test_set = pd.read_csv(label_file, sep=" ", header=None, usecols=[2, 5])
    test_set.columns = ["wav_path", "target"]
    test_set["wav_path"] = test_set["wav_path"].apply(
        lambda x: os.path.join(
            source_dir, "test_set", f"{x}.flac"
        )
    )

    duration_list = []
    for _, row in tqdm(test_set.iterrows(), total=len(test_set), desc="Preprocessing CTR-SVDD"):
        info = torchaudio.info(row["wav_path"])
        duration = info.num_frames / info.sample_rate
        duration_list.append(duration)

    # Save the manifest file
    test_set["duration"] = duration_list
    test_set["target"] = test_set["target"].apply(lambda x: x if x == "bonafide" else "spoof")
    test_set[["wav_path", "duration", "target"]].to_csv(output_path, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Prepare a dataset manifest for the CTR-SVDD dataset."
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
