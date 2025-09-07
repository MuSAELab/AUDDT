import os
import sys
import shutil
import pandas as pd
from tqdm import tqdm

import torchaudio
import speechbrain as sb
from hyperpyyaml import load_hyperpyyaml


def main(data_folder: str, dest_folder: str, manifest_file: str):
    train_val_test_splits = pd.read_csv(f"{data_folder}/train_val_test_splits.csv")
    test_set = train_val_test_splits[train_val_test_splits["set"] == "test"]

    # Replace "librispeech" with "LibriSpeech" in the filename column
    test_set["filename"] = test_set["filename"]\
        .str.replace("librispeech", "LibriSpeech")\
        .str.replace("ljspeech", "LJSpeech-1.1/wavs")

    # Create the destination folder if it doesn't exist
    os.makedirs(dest_folder, exist_ok=True)

    duration_list = []
    for _, row in tqdm(test_set.iterrows(), total=len(test_set), desc="Preprocessing DIFFSSD"):
        # Copy the file to the destination folder. Create the folder if it doesn't exist.
        rel_dir = row["filename"]
        os.makedirs(os.path.dirname(os.path.join(dest_folder, rel_dir)), exist_ok=True)
        shutil.copy2(os.path.join(data_folder, rel_dir), os.path.join(dest_folder, rel_dir))

        info = torchaudio.info(os.path.join(dest_folder, rel_dir))
        duration = info.num_frames / info.sample_rate
        duration_list.append(duration)

    # Save the manifest file
    test_set["duration"] = duration_list
    test_set["wav_path"] = test_set["filename"].apply(lambda x: os.path.join(dest_folder, x))
    test_set["target"] = test_set["target"].apply(lambda x: "bonafide" if x == 0 else "spoof")
    test_set[["wav_path", "duration", "target"]].to_csv(os.path.join(dest_folder, manifest_file), index=False)

if __name__ == "__main__":
    # Reading command line arguments
    hparams_file, run_opts, overrides = sb.parse_arguments(sys.argv[1:])

    # Load hyperparameters file with command-line overrides
    with open(hparams_file) as f:
        hparams = load_hyperpyyaml(f, overrides)

    main(
        data_folder=hparams["data_root"],
        dest_folder=hparams["dest_folder"],
        manifest_file=hparams["manifest_file"]
    )
