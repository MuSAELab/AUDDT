import pandas as pd
import argparse
from pathlib import Path
from tqdm import tqdm

def prepare_dataset(source_dir, output_path):
    """
    Prepares a manifest file for the processed CodecFake dataset.

    This script iterates through subfolders in the source directory.
    - Audios in 'genuine' are labeled 'bonafide'.
    - Audios in 'valle' and 'valle-x' are labeled 'spoof'.
    - Audios in all other folders are considered recoded and labeled 'bonafide'.
    An extra 'model_name' column is added to identify the source folder.

    Args:
        source_dir (str): The root directory of the dataset.
        output_path (str): The path to save the final manifest CSV file.
    """
    source_path = Path(source_dir).resolve()

    if not source_path.is_dir():
        print(f"Error: Source directory '{source_path}' not found.")
        return

    print(f"Scanning for subdirectories in: {source_path}")
    subdirectories = [d for d in source_path.iterdir() if d.is_dir()]

    if not subdirectories:
        print(f"Error: No subdirectories found in {source_path}.")
        return

    print(f"Found {len(subdirectories)} subdirectories to process.")
    
    all_records = []
    
    for subdir in tqdm(subdirectories, desc="Processing subdirectories"):
        model_name = subdir.name
        
        # Determine the label based on the folder name
        if model_name in ['valle', 'valle-x', 'speechx']:
            label = 'spoof'
        else:
            # 'genuine' and all other recoded folders are 'bonafide'
            label = 'bonafide'
            
        # Find all audio files in the subdirectory, searching recursively
        audio_files = list(subdir.glob('**/*.wav'))
        
        for audio_path in audio_files:
            record = {
                'audio_path': str(audio_path),
                'label': label,
                'model_name': model_name,
            }
            all_records.append(record)

    if not all_records:
        print("Error: No audio files were found and processed.")
        return

    # Create the final DataFrame
    final_df = pd.DataFrame(all_records)
    
    # Ensure a consistent column order
    final_df = final_df[['audio_path', 'label', 'model_name']]

    print(f"Final manifest size: {len(final_df)} entries.")
    
    # Save the manifest file
    output_path_obj = Path(output_path)
    output_path_obj.parent.mkdir(parents=True, exist_ok=True)
    final_df.to_csv(output_path_obj, index=False)
    
    print(f"Manifest file successfully created at: {output_path_obj}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Prepare a manifest for the processed CodecFake dataset."
    )
    parser.add_argument(
        '--source_dir',
        type=str,
        required=True,
        help="The root directory of the processed CodecFake dataset."
    )
    parser.add_argument(
        '--output_path',
        type=str,
        required=True,
        help="The path to save the final manifest CSV file."
    )
    
    args = parser.parse_args()
    prepare_dataset(args.source_dir, args.output_path)

