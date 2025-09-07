import io
import os
import sys
import shutil
import pandas as pd
from glob import glob
from tqdm import tqdm

import torchaudio
import speechbrain as sb
from hyperpyyaml import load_hyperpyyaml


def main(data_folder: str, dest_folder: str, manifest_file: str):
    test_files = glob(os.path.join(data_folder, "**/*.wav"), recursive=True)
    test_set = pd.DataFrame(test_files, columns=["original_wav_path"])
    test_set["target"] = "bonafide"

    # Create the destination folder if it doesn't exist
    os.makedirs(dest_folder, exist_ok=True)

    dest_wav_path_list = []
    duration_list = []
    for _, row in tqdm(test_set.iterrows(), total=len(test_set), desc="Preprocessing SRC4VC"):
        # Save the audio file to dest_folder
        dest_wav_path = row["original_wav_path"].replace(data_folder, dest_folder)
        os.makedirs(os.path.dirname(dest_wav_path), exist_ok=True)

        shutil.copy2(row["original_wav_path"], dest_wav_path)

        info = torchaudio.info(dest_wav_path)
        duration = info.num_frames / info.sample_rate
        duration_list.append(duration)
        dest_wav_path_list.append(dest_wav_path)

    # Save the manifest file
    test_set["duration"] = duration_list
    test_set["wav_path"] = dest_wav_path_list
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
        data_folder=os.path.join(hparams["data_root"], "src4vc", "raw"),
        dest_folder=os.path.join(hparams["dest_folder"], "src4vc", "processed"),
        manifest_file=hparams["manifest_file"]
    )
