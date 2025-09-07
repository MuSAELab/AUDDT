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
    ch_eval_metadata = pd.read_csv(os.path.join(data_folder, "petrichorwq-DECRO-dataset-6fc9884", "ch_eval.txt"), sep=" ", header=None)
    ch_eval_metadata.columns = ["SPEAKER_ID", "AUDIO_FILE_NAME", "-", "SYSTEM_ID", "target"]
    ch_eval_metadata = ch_eval_metadata[["AUDIO_FILE_NAME", "target"]]
    ch_eval_metadata["AUDIO_FILE_NAME"] = ch_eval_metadata["AUDIO_FILE_NAME"].apply(
        lambda x: os.path.join(
            data_folder, "petrichorwq-DECRO-dataset-6fc9884", "ch_eval", f"{x}.wav"
        )
    )

    en_eval_metadata = pd.read_csv(os.path.join(data_folder, "petrichorwq-DECRO-dataset-6fc9884", "en_eval.txt"), sep=" ", header=None)
    en_eval_metadata.columns = ["SPEAKER_ID", "AUDIO_FILE_NAME", "-", "SYSTEM_ID", "target"]
    en_eval_metadata = en_eval_metadata[["AUDIO_FILE_NAME", "target"]]
    en_eval_metadata["AUDIO_FILE_NAME"] = en_eval_metadata["AUDIO_FILE_NAME"].apply(
        lambda x: os.path.join(
            data_folder, "petrichorwq-DECRO-dataset-6fc9884", "en_eval", f"{x}.wav"
        )
    )

    test_set = pd.concat([ch_eval_metadata, en_eval_metadata])
    test_set["wav_path"] = test_set["AUDIO_FILE_NAME"].str.replace(data_folder, dest_folder)

    # Create the destination folder if it doesn't exist
    os.makedirs(dest_folder, exist_ok=True)

    duration_list = []
    for _, row in tqdm(test_set.iterrows(), total=len(test_set), desc="Preprocessing DECRO"):
        # Copy the file to the destination folder. Create the folder if it doesn't exist.
        os.makedirs(os.path.dirname(row["wav_path"]), exist_ok=True)
        shutil.copy2(row["AUDIO_FILE_NAME"], row["wav_path"])

        info = torchaudio.info(row["wav_path"])
        duration = info.num_frames / info.sample_rate
        duration_list.append(duration)

    # Save the manifest file
    test_set["duration"] = duration_list
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
        data_folder=os.path.join(hparams["data_root"], "decro", "raw"),
        dest_folder=os.path.join(hparams["dest_folder"], "decro", "processed"),
        manifest_file=hparams["manifest_file"]
    )
