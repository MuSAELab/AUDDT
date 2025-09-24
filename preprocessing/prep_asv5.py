import pandas as pd
import argparse
import os
from pathlib import Path
from tqdm import tqdm

def prepare_dataset(data_root, input_tsv_path, output_csv):
    """
    Prepare label file for asvspoof5.

    Args:
        data_root (str): The root directory of the dataset.
        output_csv (str): The path to save the final manifest CSV file.
    """
    data_root_path = Path(data_root).resolve()
    input_tsv_path_obj = Path(input_tsv_path).resolve() # Convert string to Path object

    if not data_root_path.is_dir() or not input_tsv_path_obj.is_file():
        print(f"Error: Data root directory '{data_root_path}' or label file '{input_tsv_path_obj}' not found.")
        return

    print(f"Scanning for label files in: {input_tsv_path_obj}")
    
    all_records = []

    # Read the TSV file, specifying no header and using a space as the delimiter
    df = pd.read_csv(input_tsv_path_obj, sep=r'\s+', header=None, comment=None)

    # Iterate through the DataFrame with a progress bar
    for _, row in tqdm(df.iterrows(), total=len(df), desc="Processing TSV entries"):
        # Extract the filename (column 1) and label (column 9)
        audio_filename = row[1]
        audio_label = row[8]
        
        # The filename is assumed to be the base name without a suffix
        audio_path = data_root_path / f"{audio_filename}.flac"

        if audio_path.exists():
            record = {
                'audio_path': str(audio_path),
                'label': audio_label
            }
            all_records.append(record)
        else:
            print(f"Warning: Audio file not found at '{audio_path}'. Skipping entry.")

    if not all_records:
        print("Error: No valid audio records were processed.")
        return

    # Create the final DataFrame
    final_df = pd.DataFrame(all_records)
    
    # Save the manifest file
    output_path_obj = Path(output_csv)
    output_path_obj.parent.mkdir(parents=True, exist_ok=True)
    final_df.to_csv(output_path_obj, index=False)
    
    print(f"Manifest file successfully created at: {output_path_obj}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Create a manifest CSV from a dataset's TSV file.")
    parser.add_argument(
        '--data_root',
        type=str,
        required=True,
        help="Root directory of the dataset with the TSV and audio files."
    )
    parser.add_argument(
        '--input_tsv_path', 
        type=str, 
        required=True, 
        help="Path to the original label tsv file."
    )
    parser.add_argument(
        '--output_csv', 
        type=str, 
        required=True, 
        help="Path to save the output manifest CSV file."
    )
    args = parser.parse_args()

    prepare_dataset(args.data_root, args.input_tsv_path, args.output_csv)
