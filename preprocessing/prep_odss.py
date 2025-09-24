import pandas as pd
import argparse
from pathlib import Path
from tqdm import tqdm

def prepare_dataset(source_dir, output_path):
    """
    Prep manifest file for ODSS.

    Args:
        source_dir (str): The root directory of the dataset containing subfolders.
        output_path (str): The path to save the final manifest CSV file.
    """
    source_path = Path(source_dir).resolve()
    
    if not source_path.is_dir():
        raise FileNotFoundError(f"Source directory '{source_path}' not found.")

    print(f"Scanning for audio files in: {source_path}")
    
    # Define labels based on top-level folders
    label_map = {
        'natural': 'bonafide',
        'fastpitch-hifigan': 'spoof',
        'vits': 'spoof'
    }
    
    all_records = []
    
    # Use glob to find all .wav files in the directory tree
    audio_files = list(source_path.glob('**/*.wav'))

    if not audio_files:
        print(f"Error: No .wav files found in {source_path}.")
        return

    print(f"Found {len(audio_files)} audio files to process.")

    for audio_file in tqdm(audio_files, desc="Processing audio files"):
        # Determine the label based on the parent folder name
        # We check each parent in the path until we find one of the defined labels
        label = None
        for part in audio_file.parts:
            if part in label_map:
                label = label_map[part]
                break
        
        if label is None:
            print(f"Warning: Could not determine label for {audio_file}. Skipping.")
            continue
            
        record = {
            'audio_path': str(audio_file),
            'label': label
        }
        all_records.append(record)

    if not all_records:
        print("Error: No valid audio records were processed.")
        return

    # Create the final DataFrame
    final_df = pd.DataFrame(all_records)
    
    print(f"Final manifest size: {len(final_df)} entries.")
    
    # Save the manifest file
    output_path_obj = Path(output_path)
    output_path_obj.parent.mkdir(parents=True, exist_ok=True)
    final_df.to_csv(output_path_obj, index=False)
    
    print(f"Manifest file successfully created at: {output_path_obj}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Prepare a dataset manifest from a nested folder structure."
    )
    parser.add_argument(
        '--source_dir',
        type=str,
        required=True,
        help="The root directory of the dataset."
    )
    parser.add_argument(
        '--output_path',
        type=str,
        required=True,
        help="The path to save the final manifest CSV file."
    )
    
    args = parser.parse_args()
    prepare_dataset(args.source_dir, args.output_path)
