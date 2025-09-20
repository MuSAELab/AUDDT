import pandas as pd
import argparse
from pathlib import Path
from tqdm import tqdm

def prepare_dataset(source_dir, label_file, output_path):
    """
    Prepares a manifest file for HABLA.

    The label file format is expected to be:
    col1 filename - attack_type label

    Args:
        source_dir (str): The directory containing all the .wav audio files.
        label_file (str): The path to the 5-column label .txt file.
        output_path (str): The path to save the final manifest CSV file.
    """
    source_path = Path(source_dir).resolve()
    label_file_path = Path(label_file).resolve()

    if not source_path.is_dir():
        print(f"Error: Source directory '{source_path}' not found.")
        return

    if not label_file_path.is_file():
        print(f"Error: Label file not found at '{label_file_path}'.")
        return

    print(f"Reading labels from: {label_file_path}")
    
    try:
        # Read the space-separated file with 5 columns and no header
        df = pd.read_csv(label_file_path, sep='\s+', header=None, engine='python')
        if df.shape[1] != 5:
            print(f"Error: Expected 5 columns in label file, but found {df.shape[1]}.")
            return
            
        df.columns = ['id', 'filename_base', 'col3', 'attack_type', 'original_label']

        all_records = []
        
        for _, row in tqdm(df.iterrows(), total=df.shape[0], desc="Processing labels"):
            record = row.to_dict()
            # Append the .wav suffix to the base filename
            filename = f"{row['filename_base']}.wav"
            audio_path = source_path / filename

            if audio_path.exists():
                record['audio_path'] = str(audio_path)
                # Convert string label to integer: 1 for bona-fide/bonafide, 0 for spoof
                # Using .lower() to make it case-insensitive
                label_str = str(row['original_label']).lower()
                record['label'] = 'spoof' if 'spoof' in label_str else 'bonafide'
                all_records.append(record)
            else:
                print(f"Warning: Audio file not found at '{audio_path}'. Skipping entry.")
        
        if not all_records:
            print("Error: No valid audio records were processed.")
            return

        # Create the final DataFrame
        final_df = pd.DataFrame(all_records)
        
        # Reorder columns for consistency
        cols_to_keep = ['id', 'filename_base', 'col3', 'attack_type', 'original_label']
        final_cols = ['audio_path', 'label'] + cols_to_keep
        final_df = final_df[final_cols]

        print(f"Final manifest size: {len(final_df)} entries.")
        
        # Save the manifest file
        output_path_obj = Path(output_path)
        output_path_obj.parent.mkdir(parents=True, exist_ok=True)
        final_df.to_csv(output_path_obj, index=False)
        
        print(f"Manifest file successfully created at: {output_path_obj}")

    except Exception as e:
        print(f"An error occurred while processing the file: {e}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Prepare a dataset manifest from a 5-column label file."
    )
    parser.add_argument(
        '--source_dir',
        type=str,
        required=True,
        help="The directory containing the audio files."
    )
    parser.add_argument(
        '--label_file',
        type=str,
        required=True,
        help="Path to the 5-column space-separated label file."
    )
    parser.add_argument(
        '--output_path',
        type=str,
        required=True,
        help="The path to save the final manifest CSV file."
    )
    
    args = parser.parse_args()
    prepare_dataset(args.source_dir, args.label_file, args.output_path)
