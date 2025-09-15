import pandas as pd
import argparse
from pathlib import Path
from tqdm import tqdm

def prepare_dataset(source_dir, output_path):
    """
    Prepares the manifest file for the Codecfake dataset.

    It works by finding all label files (.txt) in the 'label' subdirectory,
    and for each label file, it finds the corresponding audio files in the
    matching subdirectory.

    Args:
        source_dir (str): The root directory of the Codecfake dataset.
        output_path (str): The path to save the final manifest CSV file.
    """
    source_path = Path(source_dir).resolve()
    label_dir = source_path / 'label'

    if not source_path.is_dir() or not label_dir.is_dir():
        print(f"Error: Source directory '{source_path}' or label directory '{label_dir}' not found.")
        return

    print(f"Scanning for label files in: {label_dir}")
    label_files = list(label_dir.glob('*.txt'))

    if not label_files:
        print(f"Error: No label .txt files found in {label_dir}.")
        return

    print(f"Found {len(label_files)} label files to process.")
    
    all_records = []

    for label_file in tqdm(label_files, desc="Processing label files"):
        # The audio subfolder name matches the label file name (without extension)
        audio_subdir_name = label_file.stem
        audio_dir = source_path / audio_subdir_name

        if not audio_dir.is_dir():
            print(f"Warning: Corresponding audio directory '{audio_dir}' not found for label file '{label_file.name}'. Skipping.")
            continue

        try:
            # Read the label file. It has no header and is space-separated.
            df = pd.read_csv(label_file, sep='\s+', header=None)
            # Assign generic column names as requested
            df.columns = [f'column_{i+1}' for i in range(df.shape[1])]

            for _, row in df.iterrows():
                record = row.to_dict()
                audio_filename = row['column_1']
                audio_path = audio_dir / audio_filename
                
                if audio_path.exists():
                    record['audio_path'] = str(audio_path)
                    
                    # Custom logic: Flip labels for C1-C7 folders to 'real' as they are recoded
                    if audio_subdir_name.startswith('C'):
                        record['label'] = 'bonafide'
                    else:
                        # Original logic for A folders, as these are LMs generated
                        record['label'] = 'spoof' if row['column_2'] == 'fake' else 'bonafide'
                        
                    all_records.append(record)
                else:
                    print(f"Warning: Audio file not found at '{audio_path}'. Skipping entry.")
        
        except Exception as e:
            print(f"Warning: Could not process file {label_file}. Error: {e}")

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


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Prepare a dataset manifest for the Codecfake dataset."
    )
    parser.add_argument(
        '--source_dir',
        type=str,
        required=True,
        help="The root directory of the Codecfake dataset."
    )
    parser.add_argument(
        '--output_path',
        type=str,
        required=True,
        help="The path to save the final manifest CSV file."
    )
    
    args = parser.parse_args()
    prepare_dataset(args.source_dir, args.output_path)

