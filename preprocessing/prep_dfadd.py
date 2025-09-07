import io
import os
import sys
import pandas as pd
from glob import glob
from tqdm import tqdm

import torchaudio
import speechbrain as sb
from hyperpyyaml import load_hyperpyyaml


def main(data_folder: str, dest_folder: str, manifest_file: str):
    test_files = glob(os.path.join(data_folder, "*.parquet"))

    test_set = []
    for file in test_files:
        df = pd.read_parquet(file)
        test_set.append(df)

    test_set = pd.concat(test_set)

    # Create the destination folder if it doesn't exist
    os.makedirs(dest_folder, exist_ok=True)

    wav_path_list = []
    duration_list = []
    for _, row in tqdm(test_set.iterrows(), total=len(test_set), desc="Preprocessing DFADD"):
        # Save the audio file to dest_folder
        rel_dir = os.path.join(row["label"], row["audio_name"])
        os.makedirs(os.path.dirname(os.path.join(dest_folder, rel_dir)), exist_ok=True)

        # Load bytes with torchaudio
        audio, sr = torchaudio.load(io.BytesIO(row["audio"]["bytes"]))
        torchaudio.save(os.path.join(dest_folder, rel_dir), audio, sr)

        duration = audio.shape[1] / sr
        duration_list.append(duration)
        wav_path_list.append(os.path.join(dest_folder, rel_dir))

    # Save the manifest file
    test_set["duration"] = duration_list
    test_set["wav_path"] = wav_path_list
    test_set["target"] = test_set["label"]
    test_set[["wav_path", "duration", "target"]].to_csv(os.path.join(dest_folder, manifest_file), index=False)

if __name__ == "__main__":
    # Reading command line arguments
    hparams_file, run_opts, overrides = sb.parse_arguments(sys.argv[1:])

    # Load hyperparameters file with command-line overrides
    with open(hparams_file) as f:
        hparams = load_hyperpyyaml(f, overrides)
    
    if hparams.get("dest_folder") is None:
        hparams["dest_folder"] = hparams["data_root"]

    main(
        data_folder=os.path.join(hparams["data_root"], "dfadd", "raw"),
        dest_folder=os.path.join(hparams["dest_folder"], "dfadd", "processed"),
        manifest_file=hparams["manifest_file"]
    )
