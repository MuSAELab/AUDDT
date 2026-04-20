import os
import argparse
import pandas as pd
from tqdm import tqdm
import torchaudio
import random


# Define the dataset folders for spoof samples
SPOOF_FOLDERS = {
    "audiocraft_audio_cut",
    "audioLDM1_audio_cut",
    "audioLDM2_audio_cut",
    "V2A_mapper_audio_cut",
    "V2A_mlp_audio_cut",
}
# VGGsound_test_14923_audio_cut contains only bonafide samples
BONAFIDE_FOLDERS = {
    "VGGsound_test_14923_audio_cut",
}
# Define the manifest configuration for each split
MANIFEST_CONFIG = {
    "train": {
        "groups": ["audioLDM1_audio_cut", "audioLDM2_audio_cut", 
                    "V2A_mapper_audio_cut", "VGGsound_test_14923_audio_cut"],
        "num_samples": 11149,
        "slice": slice(0, 11149),
    },
    "dev1": {
        "groups": ["audioLDM1_audio_cut", "audioLDM2_audio_cut", 
                    "V2A_mapper_audio_cut", "VGGsound_test_14923_audio_cut"],
        "num_samples": 3774,
        "slice": slice(11149, 14923),
    },
    "dev2": {
        "groups": ["V2A_mlp_audio_cut", "audiocraft_audio_cut", 
                    "VGGsound_test_14923_audio_cut"],
        "num_samples": 3774,
        "slice": slice(0, 3774),
    },
    "dev3": {
        "groups": ["audioLDM1_audio_cut", "audioLDM2_audio_cut", 
                    "V2A_mapper_audio_cut", "V2A_mlp_audio_cut",
                    "audiocraft_audio_cut", "VGGsound_test_14923_audio_cut"],
        "num_samples": 3774,
        "slice": slice(0, 3774),
    },
}


def get_dataset_folder(audio_path):
    """
    Extract the dataset folder name from the audio path. This is used to 
    determine the label (spoof vs bonafide) and to group samples for manifest 
    generation.
    
    Parameters
    ----------
    audio_path : str
        Path to the audio file.
    
    Returns
    ----------
    part : str or None
        The dataset folder name if found, otherwise None.
    """
    parts = audio_path.split(os.sep)
    for part in parts:
        if part in SPOOF_FOLDERS or part in BONAFIDE_FOLDERS:
            return part
    return None


def get_duration(audio_path):
    """
    Get the duration of an audio file.
    
    Parameters
    ----------
    audio_path :str
        Path to the audio file.
    
    Returns
    ----------
    duration :float
        Duration of the audio file in seconds.
    """
    info = torchaudio.info(audio_path)
    return float(info.num_frames) / float(info.sample_rate)


def collect_audio_records(source_dir):
    """
    Walk through the source directory and collect metadata for all .wav files.

    Parameters
    ----------
    source_dir :str
        The root directory of the VcapAV dataset containing all audio files.
    
    Returns
    ----------
    records :list of dict
        A list of dictionaries, each containing metadata for an audio file 
        with keys: audio_path, label, duration, dataset_folder. 
    """
    records = []
    all_files = []
    # Walk through the source directory and collect all .wav files
    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.endswith(".wav"):
                all_files.append((root, file))
    
    # Process each audio file and extract metadata
    for root, file in tqdm(all_files, desc="Processing audio files"):
        audio_path = os.path.abspath(os.path.join(root, file))
        dataset_folder = get_dataset_folder(audio_path)
        if dataset_folder is None:
            print(f"Warning: Skipping unknown dataset folder for {audio_path}")
            continue

        # Determine the label based on the dataset folder
        if dataset_folder in SPOOF_FOLDERS:
            label = "spoof"
        elif dataset_folder in BONAFIDE_FOLDERS:
            label = "bonafide"
        else:
            print(f"Warning: Unrecognized folder " \
                f"{dataset_folder} for {audio_path}")
            continue
        
        # Get the duration of the audio file
        try:
            duration = get_duration(audio_path)
        except Exception as exc:
            print(f"Warning: Failed to read duration for {audio_path}: {exc}")
            continue

        # Append the record to the list
        records.append(
            {
                "audio_path": audio_path,
                "label": label,
                "duration": duration,
                "dataset_folder": dataset_folder,
            }
        )

    return records


def save_manifest(records, output_path):
    """
    Save a list of audio records to a CSV manifest file with columns: 
    audio_path, label, duration.
    
    Parameters
    ----------  
    records : list of dict 
        List of audio records to save. 
        Each record should have keys: audio_path, label, duration.
    output_path :str
            Path to save the CSV manifest file.

    Returns
    ----------
    None
    """

    df = pd.DataFrame(records)[["audio_path", "label", "duration"]]
    df.to_csv(output_path, index=False)
    print(f"Saved manifest: {output_path} ({len(df)} rows)")


def prepare_dataset(source_dir, output_dir):
    """
    Prepare the VcapAV dataset by generating CSV manifest files for 
    train/dev1/dev2/dev3 splits.
    
    Parameters
    ----------
    source_dir :str
        The root directory of the VcapAV dataset containing all audio files.
    output_dir :str
        Directory where train/dev1/dev2/dev3 CSV manifests will be written.     
    Returns 
    ----------
    None
    """
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Collect metadata for all audio files in the source directory
    records = collect_audio_records(source_dir)
    if len(records) == 0:
        raise ValueError(f"No audio records were found under {source_dir}.")

    # Group records by dataset folder to facilitate manifest generation based 
    # on the defined splits
    grouped = {}
    for record in records:
        grouped.setdefault(record["dataset_folder"], []).append(record)
    
    # Randomly shuffle records within each group 
    for group_records in grouped.values():
        random.shuffle(group_records)

    # Generate manifests for each split based on the defined configuration
    for manifest_name, config in tqdm(MANIFEST_CONFIG.items(), 
                                    desc="Generating manifests"):
        selected = []
        for folder in config["groups"]:
            group_records = grouped.get(folder, [])
            selected.extend(group_records[config["slice"]])

        output_path = os.path.join(output_dir, f"{manifest_name}.csv")
        save_manifest(selected, output_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Prepare metadata manifests for the VcapAV dataset."
    )
    parser.add_argument(
        "--source_dir",
        type=str,
        required=True,
        help="The root directory of the VcapAV dataset."
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        required=True,
        help="Directory where train/dev1,2,3 CSV manifests will be written."
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for shuffling records (default: 42)."
    )
    args = parser.parse_args()
    random.seed(args.seed) # Set the random seed for reproducibility
    prepare_dataset(args.source_dir, args.output_dir)
