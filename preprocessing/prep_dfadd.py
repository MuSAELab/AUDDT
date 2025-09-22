import io
import os
import argparse
import pandas as pd
from glob import glob
from tqdm import tqdm

import torchaudio


def prepare_dataset(source_dir: str, dest_dir: str, output_path: str):
    test_files = glob(os.path.join(source_dir, "*.parquet"))

    test_set = []
    for file in test_files:
        df = pd.read_parquet(file)
        test_set.append(df)

    test_set = pd.concat(test_set)

    # Create the destination folder if it doesn't exist
    os.makedirs(dest_dir, exist_ok=True)

    wav_path_list = []
    duration_list = []
    for _, row in tqdm(test_set.iterrows(), total=len(test_set), desc="Preprocessing DFADD"):
        # Save the audio file to dest_folder
        rel_dir = os.path.join(row["label"], row["audio_name"])
        os.makedirs(os.path.dirname(os.path.join(dest_dir, rel_dir)), exist_ok=True)

        # Load bytes with torchaudio
        audio, sr = torchaudio.load(io.BytesIO(row["audio"]["bytes"]))
        torchaudio.save(os.path.join(dest_dir, rel_dir), audio, sr)

        duration = audio.shape[1] / sr
        duration_list.append(duration)
        wav_path_list.append(os.path.join(dest_dir, rel_dir))

    # Save the manifest file
    test_set["duration"] = duration_list
    test_set["wav_path"] = wav_path_list
    test_set["target"] = test_set["label"]
    test_set[["wav_path", "duration", "target"]].to_csv(output_path, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Prepare a dataset manifest for the DFADD dataset."
    )
    parser.add_argument(
        '--source_dir',
        type=str,
        required=True,
        help="The root directory of the DFADD dataset."
    )
    parser.add_argument(
        '--dest_dir',
        type=str,
        required=True,
        help="The destination directory of the DFADD dataset (Where the audio files will be saved)."
    )
    parser.add_argument(
        '--output_path',
        type=str,
        required=True,
        help="The path to save the final manifest CSV file."
    )
    
    args = parser.parse_args()
    prepare_dataset(args.source_dir, args.dest_dir, args.output_path)
