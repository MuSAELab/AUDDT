# Download the dataset parquet files first using download/get_envssd.sh.
# The script downloads parquet files (with embedded audio) for the test and remain splits.
#
# After downloading, your folder structure should look like:
#
# data_root/
#  ├── envssd/
#  │   ├── raw/
#  │   │   ├── test-00000-of-00014.parquet
#  │   │   ├── ...
#  │   │   ├── remain-00000-of-00040.parquet
#  │   │   └── ...
#  │   └── processed/
#  │       ├── test/
#  │       │   └── *.wav
#  │       ├── remain/
#  │       │   └── *.wav
#  │       └── manifest_envssd.csv
#
# This script reads the parquet files, extracts the embedded WAV audio to disk,
# and produces the manifest CSV.
# Labels: "real" -> "bonafide", "fake" -> "spoof"

import io
import os
import argparse
import pandas as pd
from pathlib import Path
from tqdm import tqdm

import torchaudio


def prepare_dataset(source_dir: str, audio_dir: str, output_path: str):
    records = []

    for split in ["test", "remain"]:
        split_audio_dir = os.path.join(audio_dir, split)
        os.makedirs(split_audio_dir, exist_ok=True)

        parquet_files = sorted(Path(source_dir).glob(f"{split}-*.parquet"))
        if not parquet_files:
            print(f"Warning: no parquet files found for split '{split}' in {source_dir}")
            continue

        for parquet_file in tqdm(parquet_files, desc=f"Processing {split} shards"):
            shard_num = int(parquet_file.stem.split("-")[1])
            df = pd.read_parquet(parquet_file)

            for local_idx, (_, row) in enumerate(df.iterrows()):
                out_filename = f"{shard_num:05d}_{local_idx:05d}.wav"
                out_path = os.path.join(split_audio_dir, out_filename)

                if not os.path.exists(out_path):
                    audio_bytes = row["audio"]["bytes"]
                    waveform, sample_rate = torchaudio.load(io.BytesIO(audio_bytes))
                    torchaudio.save(out_path, waveform, sample_rate)

                info = torchaudio.info(out_path)
                duration = info.num_frames / info.sample_rate
                label = "bonafide" if row["label"] == "real" else "spoof"

                records.append({
                    "audio_path": out_path,
                    "duration": duration,
                    "label": label,
                })

    df_out = pd.DataFrame(records)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df_out[["audio_path", "duration", "label"]].to_csv(output_path, index=False)
    print(f"Manifest saved to {output_path} ({len(df_out)} entries).")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Prepare a dataset manifest for the EnvSDD dataset."
    )
    parser.add_argument(
        "--source_dir",
        type=str,
        required=True,
        help="Directory containing the downloaded parquet files (envssd/raw/).",
    )
    parser.add_argument(
        "--audio_dir",
        type=str,
        required=True,
        help="Directory where extracted WAV files will be written (envssd/processed/).",
    )
    parser.add_argument(
        "--output_path",
        type=str,
        required=True,
        help="Path for the output manifest CSV file.",
    )

    args = parser.parse_args()
    prepare_dataset(args.source_dir, args.audio_dir, args.output_path)
