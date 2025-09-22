import io
import os
import argparse
import pandas as pd
from glob import glob
from tqdm import tqdm

import torchaudio


def prepare_dataset(source_dir: str, output_path: str):
    test_files = glob(os.path.join(source_dir, "**/*.wav"), recursive=True)
    test_set = pd.DataFrame(test_files, columns=["wav_path"])
    test_set["target"] = "bonafide"

    duration_list = []
    for _, row in tqdm(test_set.iterrows(), total=len(test_set), desc="Preprocessing SRC4VC"):
        info = torchaudio.info(row["wav_path"])
        duration = info.num_frames / info.sample_rate
        duration_list.append(duration)

    # Save the manifest file
    test_set["duration"] = duration_list
    test_set[["wav_path", "duration", "target"]].to_csv(output_path, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Prepare a dataset manifest for the SRC4VC dataset."
    )
    parser.add_argument(
        '--source_dir',
        type=str,
        required=True,
        help="The root directory of the SRC4VC dataset."
    )
    parser.add_argument(
        '--output_path',
        type=str,
        required=True,
        help="The path to save the final manifest CSV file."
    )
    
    args = parser.parse_args()
    prepare_dataset(args.source_dir, args.output_path)
