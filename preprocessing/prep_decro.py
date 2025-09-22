import io
import os
import argparse
import pandas as pd
from glob import glob
from tqdm import tqdm

import torchaudio
import speechbrain as sb
from hyperpyyaml import load_hyperpyyaml


def prepare_dataset(source_dir: str, output_path: str):
    ch_eval_metadata = pd.read_csv(os.path.join(source_dir, "petrichorwq-DECRO-dataset-6fc9884", "ch_eval.txt"), sep=" ", header=None)
    ch_eval_metadata.columns = ["SPEAKER_ID", "AUDIO_FILE_NAME", "-", "SYSTEM_ID", "label"]
    ch_eval_metadata = ch_eval_metadata[["AUDIO_FILE_NAME", "label"]]
    ch_eval_metadata["AUDIO_FILE_NAME"] = ch_eval_metadata["AUDIO_FILE_NAME"].apply(
        lambda x: os.path.join(
            source_dir, "petrichorwq-DECRO-dataset-6fc9884", "ch_eval", f"{x}.wav"
        )
    )

    en_eval_metadata = pd.read_csv(os.path.join(source_dir, "petrichorwq-DECRO-dataset-6fc9884", "en_eval.txt"), sep=" ", header=None)
    en_eval_metadata.columns = ["SPEAKER_ID", "AUDIO_FILE_NAME", "-", "SYSTEM_ID", "label"]
    en_eval_metadata = en_eval_metadata[["AUDIO_FILE_NAME", "label"]]
    en_eval_metadata["AUDIO_FILE_NAME"] = en_eval_metadata["AUDIO_FILE_NAME"].apply(
        lambda x: os.path.join(
            source_dir, "petrichorwq-DECRO-dataset-6fc9884", "en_eval", f"{x}.wav"
        )
    )

    test_set = pd.concat([ch_eval_metadata, en_eval_metadata])
    test_set["audio_path"] = test_set["AUDIO_FILE_NAME"]

    duration_list = []
    for _, row in tqdm(test_set.iterrows(), total=len(test_set), desc="Preprocessing DECRO"):
        info = torchaudio.info(row["audio_path"])
        duration = info.num_frames / info.sample_rate
        duration_list.append(duration)

    # Save the manifest file
    test_set["duration"] = duration_list
    test_set[["audio_path", "duration", "label"]].to_csv(output_path, index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Prepare a dataset manifest for the DECRO dataset."
    )
    parser.add_argument(
        '--source_dir',
        type=str,
        required=True,
        help="The root directory of the DECRO dataset."
    )
    parser.add_argument(
        '--output_path',
        type=str,
        required=True,
        help="The path to save the final manifest CSV file."
    )
    
    args = parser.parse_args()
    prepare_dataset(args.source_dir, args.output_path)
