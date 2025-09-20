import pandas as pd
import argparse
from pathlib import Path
from tqdm import tqdm

def prepare_dataset(source_dir, output_path):
    """
    Prepares the manifest file for the SpoofCeleb dataset's evaluation set.

    This script specifically targets the data within the 'flac/evaluation/' subdirectory.
    - Audios in the 'a00' subfolder are labeled as 'bona-fide'.
    - Audios in all other 'aXX' subfolders are labeled as 'spoof'.
    An 'attack_type' column is added to identify the source subfolder.

    Args:
        source_dir (str): The root directory of the SpoofCeleb dataset.
        output_path (str): The path to save the final manifest CSV file.
    """
    source_path = Path(source_dir).resolve()
    eval_path = source_path / 'flac' / 'evaluation'

    if not eval_path.is_dir():
        print(f"Error: Evaluation directory not found at '{eval_path}'.")
        print("Please ensure the source directory is the root of the SpoofCeleb dataset.")
        return

    print(f"Scanning for attack type subdirectories in: {eval_path}")
    attack_subdirs = [d for d in eval_path.iterdir() if d.is_dir()]

    if not attack_subdirs:
        print(f"Error: No subdirectories (a00, a15, etc.) found in {eval_path}.")
        return

    print(f"Found {len(attack_subdirs)} subdirectories to process.")
    
    all_records = []
    
    for subdir in tqdm(attack_subdirs, desc="Processing attack types"):
        attack_type = subdir.name
        
        # Determine the label based on the folder name
        label = 'bonafide' if attack_type == 'a00' else 'spoof'
            
        # Find all audio files (.flac) recursively within the attack subdirectory
        audio_files = list(subdir.glob('**/*.flac'))
        
        for audio_path in audio_files:
            record = {
                'audio_path': str(audio_path),
                'label': label,
                'attack_type': attack_type,
            }
            all_records.append(record)

    if not all_records:
        print("Error: No .flac audio files were found and processed.")
        return

    # Create the final DataFrame
    final_df = pd.DataFrame(all_records)
    
    # Ensure a consistent column order
    final_df = final_df[['audio_path', 'label', 'attack_type']]

    print(f"Final manifest size: {len(final_df)} entries.")
    
    # Save the manifest file
    output_path_obj = Path(output_path)
    output_path_obj.parent.mkdir(parents=True, exist_ok=True)
    final_df.to_csv(output_path_obj, index=False)
    
    print(f"Manifest file successfully created at: {output_path_obj}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Prepare a manifest for the SpoofCeleb evaluation dataset."
    )
    parser.add_argument(
        '--source_dir',
        type=str,
        required=True,
        help="The root directory of the SpoofCeleb dataset."
    )
    parser.add_argument(
        '--output_path',
        type=str,
        required=True,
        help="The path to save the final manifest CSV file."
    )
    
    args = parser.parse_args()
    prepare_dataset(args.source_dir, args.output_path)
