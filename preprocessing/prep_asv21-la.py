import pandas as pd
import argparse
import os
from pathlib import Path
from tqdm import tqdm

def prepare_dataset(data_root, input_label_path, output_csv):
    """
    Prepares a manifest file from the new dataset's label file format.

    Args:
        data_root (str): The root directory of the dataset.
        input_label_path (str): Path to the original label .txt file.
        output_csv (str): The path to save the final manifest CSV file.
    """
    data_root_path = Path(data_root).resolve()
    input_label_path_obj = Path(input_label_path).resolve()

    if not data_root_path.is_dir() or not input_label_path_obj.is_file():
        print(f"Error: Data root directory '{data_root_path}' or label file '{input_label_path_obj}' not found.")
        return

    print(f"Scanning for label file: {input_label_path_obj}")
    
    all_records = []
    
    with open(input_label_path_obj, 'r') as f:
        lines = f.readlines()
        
    for line in tqdm(lines, desc="Processing label file"):
        line = line.strip()
        if not line: # Skip empty lines
            continue

        try:
            parts = line.split()
            if len(parts) < 5:
                print(f"Warning: Skipping line with an unexpected number of columns: {line}")
                continue
                
            audio_filename = parts[1]
            audio_label = parts[5]
            
            audio_path = data_root_path / f"{audio_filename}.flac"

            if audio_path.exists():
                record = {
                    'audio_path': str(audio_path),
                    'label': audio_label
                }
                all_records.append(record)
            else:
                print(f"Warning: Audio file not found at '{audio_path}'. Skipping entry.")
        
        except IndexError as e:
            print(f"Warning: Could not parse line due to missing columns: {line}. Error: {e}")
        except Exception as e:
            print(f"Warning: Could not process line {line}. Error: {e}")

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
    parser = argparse.ArgumentParser(description="Create a manifest CSV from a dataset's label file.")
    parser.add_argument(
        '--data_root',
        type=str,
        required=True,
        help="Root directory of the dataset with the audio files."
    )
    parser.add_argument(
        '--input_label_path', 
        type=str, 
        required=True, 
        help="Path to the original label file."
    )
    parser.add_argument(
        '--output_csv', 
        type=str, 
        required=True, 
        help="Path to save the output manifest CSV file."
    )
    args = parser.parse_args()

    prepare_dataset(args.data_root, args.input_label_path, args.output_csv)
