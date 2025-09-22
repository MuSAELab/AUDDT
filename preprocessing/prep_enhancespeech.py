# First, download the dataset (only the test folder) from the Google Drive repository
# by following: http://hguimaraes.me/DiTSE
# Insert the zip file in a folder called "enhancespeech/raw" inside your data root
# Unzip the compressed file and insert in a folder called "enhancespeech/processed" inside your data root.
# In the end, your folder structure should be like this:
#
# data_root/
#  ├── enhancespeech/
#  │   ├── raw/
#  │   │   └── DiTSE_Results-download_datetime.zip
#  │   ├── processed/
#  │   │   └── DiTSE_Results/
#  │   │       └── **/*.wav
#  │   └── manifest_enhancespeech.csv
#  └── ...
# Note: the manifest_enhancespeech.csv file will be created with this script

import io
import os
import argparse
import pandas as pd
from glob import glob
from tqdm import tqdm

import torchaudio


def prepare_dataset(source_dir: str, output_path: str):
    test_files_demo = glob(os.path.join(source_dir, "DiTSE_Results/DEMO_SE_results_MOS", "**/*.wav"), recursive=True)
    test_files_demo = pd.DataFrame(test_files_demo, columns=["wav_path"])
    test_files_demo = test_files_demo[test_files_demo["wav_path"].str.contains(
        "ditse-base-dac-16k|genhancer-16k|hifigan2-16k|miipher-16k|sgmseplus-16k|input-16k"
    )]

    test_files_aqecc = glob(os.path.join(source_dir, "DiTSE_Results/AQECC_SE_results_MOS", "**/*.wav"), recursive=True)
    test_files_aqecc = pd.DataFrame(test_files_aqecc, columns=["wav_path"])
    test_files_aqecc = test_files_aqecc[test_files_aqecc["wav_path"].str.contains(
        "ditse-base-dac-16k|genhancer-16k|hifigan2-16k|miipher-16k|sgmseplus-16k|input-16k"
    )]

    test_files_daps = glob(os.path.join(source_dir, "DiTSE_Results/DAPS_SE_results_MOS", "**/*.wav"), recursive=True)
    test_files_daps = pd.DataFrame(test_files_daps, columns=["wav_path"])
    test_files_daps = test_files_daps[test_files_daps["wav_path"].str.contains(
        "clean-44k|ditse-base-dac-44k|genhancer-44k|hifigan2-44k|miipher-22k|sgmseplus-48k|input-44k"
    )]

    # Filter files that not contain ["AQECC", "DEMO", "DAPS"] in their filename
    test_set = pd.concat([test_files_demo, test_files_aqecc, test_files_daps])
    test_set["target"] = "bonafide"

    duration_list = []
    for _, row in tqdm(test_set.iterrows(), total=len(test_set), desc="Preprocessing EnhanceSpeech"):
        info = torchaudio.info(row["wav_path"])
        duration = info.num_frames / info.sample_rate
        duration_list.append(duration)

    # Save the manifest file
    test_set["duration"] = duration_list
    test_set[["wav_path", "duration", "target"]].to_csv(output_path, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Prepare a dataset manifest for the EnhanceSpeech dataset."
    )
    parser.add_argument(
        '--source_dir',
        type=str,
        required=True,
        help="The root directory of the EnhanceSpeech dataset."
    )
    parser.add_argument(
        '--output_path',
        type=str,
        required=True,
        help="The path to save the final manifest CSV file."
    )
    
    args = parser.parse_args()
    prepare_dataset(args.source_dir, args.output_path)
