import pandas as pd
import argparse
from pathlib import Path
from tqdm import tqdm

def prepare_dataset(source_dir, output_path):
    """
    Scans a nested directory structure for 'meta.csv' files, processes them to find
    both fake and original audio paths, and compiles a single manifest file.
    This version preserves all original columns and creates a separate entry for
    each original audio file paired with a fake one.

    The expected structure is:
    source_dir/fake/language/model/meta.csv

    Args:
        source_dir (str): The root directory of the dataset (e.g., the directory
                          containing the 'fake' and original audio folders).
        output_path (str): The path where the final manifest CSV will be saved.
    """
    source_path = Path(source_dir).resolve()
    if not source_path.is_dir():
        print(f"Error: Source directory not found at: {source_path}")
        return

    print(f"Scanning for 'meta.csv' files in: {source_path}")
    
    # Use rglob to recursively find all meta.csv files in the directory
    meta_files = list(source_path.rglob('meta.csv'))
    
    if not meta_files:
        print("Error: No 'meta.csv' files found. Please check the directory structure.")
        return

    print(f"Found {len(meta_files)} meta.csv files to process.")
    
    all_records = []

    # Use tqdm for a progress bar as this might take a while
    for meta_file in tqdm(meta_files, desc="Processing metadata files"):
        try:
            # The 'path' column in meta.csv is relative to the source_dir
            # We must also handle the '|' separator.
            df = pd.read_csv(meta_file, sep='|')
            
            for _, row in df.iterrows():
                # --- 1. Create the FAKE audio record ---
                fake_record = row.to_dict()
                fake_audio_relative_path = row['path']
                fake_audio_abs_path = source_path / fake_audio_relative_path
                
                if fake_audio_abs_path.exists():
                    fake_record['audio_path'] = str(fake_audio_abs_path)
                    fake_record['label'] = 'spoof'
                    # Clean up the original 'path' column to avoid redundancy
                    del fake_record['path']
                    all_records.append(fake_record)

                # --- 2. Create the corresponding REAL audio record ---
                real_record = row.to_dict()
                real_audio_relative_path = row['original_file']
                real_audio_abs_path = source_path / 'real' / real_audio_relative_path

                if real_audio_abs_path.exists():
                    real_record['audio_path'] = str(real_audio_abs_path)
                    real_record['label'] = 'bonafide'
                    # Also clean up the 'path' column here
                    del real_record['path']
                    all_records.append(real_record)

        except Exception as e:
            print(f"Warning: Could not process file {meta_file}. Error: {e}")

    if not all_records:
        print("Error: No audio records were successfully processed.")
        return

    print(f"Total audio paths collected: {len(all_records)}")

    # Create the final DataFrame and remove any duplicates based on the absolute audio path
    final_df = pd.DataFrame(all_records)
    final_df.drop_duplicates(subset=['audio_path'], inplace=True)
    
    print(f"Final manifest size (after removing duplicates): {len(final_df)} entries.")
    
    # Save the manifest file
    output_path_obj = Path(output_path)
    output_path_obj.parent.mkdir(parents=True, exist_ok=True)
    final_df.to_csv(output_path_obj, index=False)
    
    print(f"Manifest file successfully created at: {output_path_obj}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Prepare a dataset manifest from a complex nested structure containing 'meta.csv' files."
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

