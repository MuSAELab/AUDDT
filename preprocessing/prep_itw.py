import pandas as pd
import argparse
from pathlib import Path
from tqdm import tqdm

def prepare_dataset(source_dir, output_path):
    """
    Prepares a manifest file from a central meta.csv file where all audios
    are in the same directory.

    Args:
        source_dir (str): The directory containing all .wav files and the meta.csv.
        output_path (str): The path to save the final manifest CSV file.
    """
    source_path = Path(source_dir).resolve()
    meta_file_path = source_path / 'meta.csv'

    if not source_path.is_dir():
        print(f"Error: Source directory '{source_path}' not found.")
        return

    if not meta_file_path.is_file():
        print(f"Error: 'meta.csv' not found in '{source_path}'.")
        return

    print(f"Reading metadata from: {meta_file_path}")
    
    try:
        # Read the CSV file, which has no header
        df = pd.read_csv(meta_file_path, header=None)
        # Assign clear column names
        df.columns = ['filename', 'speaker', 'original_label']

        all_records = []
        
        # Use tqdm for progress bar
        for _, row in tqdm(df.iterrows(), total=df.shape[0], desc="Processing metadata"):
            record = row.to_dict()
            audio_path = source_path / row['filename']

            if audio_path.exists():
                record['audio_path'] = str(audio_path)
                record['label'] = 'bonafide' if row['original_label'] == 'bona-fide' else 'spoof'
                all_records.append(record)
            else:
                print(f"Warning: Audio file not found at '{audio_path}'. Skipping entry.")
        
        if not all_records:
            print("Error: No valid audio records were processed.")
            return

        # Create the final DataFrame
        final_df = pd.DataFrame(all_records)
        
        # Reorder columns to have audio_path and label first for consistency
        cols = ['audio_path', 'label'] + [col for col in final_df.columns if col not in ['audio_path', 'label']]
        final_df = final_df[cols]

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
        description="Prepare a dataset manifest from a central meta.csv file."
    )
    parser.add_argument(
        '--source_dir',
        type=str,
        required=True,
        help="The directory containing the audio files and meta.csv."
    )
    parser.add_argument(
        '--output_path',
        type=str,
        required=True,
        help="The path to save the final manifest CSV file."
    )
    
    args = parser.parse_args()
    prepare_dataset(args.source_dir, args.output_path)
