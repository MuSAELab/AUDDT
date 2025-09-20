# First, download the dataset from the Google Drive repository
# Insert in a folder called "enhancespeech/raw" inside your data root
# Unzip the compressed file and delete the zip file

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
    test_files_demo = glob(os.path.join(data_folder, "DiTSE_Results/DEMO_SE_results_MOS", "**/*.wav"), recursive=True)
    test_files_demo = pd.DataFrame(test_files_demo, columns=["original_wav_path"])
    test_files_demo = test_files_demo[test_files_demo["original_wav_path"].str.contains(
        "ditse-base-dac-16k|genhancer-16k|hifigan2-16k|miipher-16k|sgmseplus-16k|input-16k"
    )]

    test_files_aqecc = glob(os.path.join(data_folder, "DiTSE_Results/AQECC_SE_results_MOS", "**/*.wav"), recursive=True)
    test_files_aqecc = pd.DataFrame(test_files_aqecc, columns=["original_wav_path"])
    test_files_aqecc = test_files_aqecc[test_files_aqecc["original_wav_path"].str.contains(
        "ditse-base-dac-16k|genhancer-16k|hifigan2-16k|miipher-16k|sgmseplus-16k|input-16k"
    )]

    test_files_daps = glob(os.path.join(data_folder, "DiTSE_Results/DAPS_SE_results_MOS", "**/*.wav"), recursive=True)
    test_files_daps = pd.DataFrame(test_files_daps, columns=["original_wav_path"])
    test_files_daps = test_files_daps[test_files_daps["original_wav_path"].str.contains(
        "clean-44k|ditse-base-dac-44k|genhancer-44k|hifigan2-44k|miipher-22k|sgmseplus-48k|input-44k"
    )]

    # Filter files that not contain ["AQECC", "DEMO", "DAPS"] in their filename
    test_set = pd.concat([test_files_demo, test_files_aqecc, test_files_daps])
    test_set["target"] = "bonafide"

    # Create the destination folder if it doesn't exist
    os.makedirs(dest_folder, exist_ok=True)

    dest_wav_path_list = []
    duration_list = []
    for _, row in tqdm(test_set.iterrows(), total=len(test_set), desc="Preprocessing EnhanceSpeech"):
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
        data_folder=os.path.join(hparams["data_root"], "enhancespeech", "raw"),
        dest_folder=os.path.join(hparams["dest_folder"], "enhancespeech", "processed"),
        manifest_file=hparams["manifest_file"]
    )
