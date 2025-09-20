import pandas as pd
import argparse
from pathlib import Path
from tqdm import tqdm

def prepare_dataset(source_dir, output_path):
    """
    Prepares a manifest file for CVoiceFake.

    The script expects a structure like:
    - SOURCE_DIR/
      - LANGUAGE_CODE/
        - Bonafide/
          - audio1.mp3
        - model_name_generated/
          - audio2.mp3

    All audio files will be labeled as bona-fide since they are vocoded.
    An extra 'model_name' column will identify the source subfolder.
    A 'language' column will identify the language.

    Args:
        source_dir (str): The root directory of the dataset.
        output_path (str): The path to save the final manifest CSV file.
    """
    source_path = Path(source_dir).resolve()

    if not source_path.is_dir():
        print(f"Error: Source directory '{source_path}' not found.")
        return

    print(f"Scanning for language subdirectories in: {source_path}")
    language_dirs = [d for d in source_path.iterdir() if d.is_dir()]

    if not language_dirs:
        print(f"Error: No language subdirectories (e.g., 'IT', 'EN') found in {source_path}.")
        return

    print(f"Found {len(language_dirs)} language directories to process.")
    
    all_records = []
    
    for lang_dir in tqdm(language_dirs, desc="Processing languages"):
        language_code = lang_dir.name
        
        model_subdirs = [d for d in lang_dir.iterdir() if d.is_dir()]
        
        for model_dir in model_subdirs:
            model_name = model_dir.name
            
            # Find all audio files (.mp3) recursively within the model subdirectory
            audio_files = list(model_dir.glob('**/*.mp3'))
            
            for audio_path in audio_files:
                record = {
                    'audio_path': str(audio_path),
                    'label': 'bonafide',  # All are considered bona-fide
                    'language': language_code,
                    # For Bonafide folder, the model is 'bonafide', otherwise it's the folder name
                    'model_name': 'bonafide' if model_name == 'Bonafide' else model_name
                }
                all_records.append(record)

    if not all_records:
        print("Error: No .mp3 audio files were found and processed.")
        return

    # Create the final DataFrame
    final_df = pd.DataFrame(all_records)
    
    # Ensure a consistent column order
    final_df = final_df[['audio_path', 'label', 'language', 'model_name']]

    print(f"Final manifest size: {len(final_df)} entries.")
    
    # Save the manifest file
    output_path_obj = Path(output_path)
    output_path_obj.parent.mkdir(parents=True, exist_ok=True)
    final_df.to_csv(output_path_obj, index=False)
    
    print(f"Manifest file successfully created at: {output_path_obj}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Prepare a manifest for a multilingual bona-fide dataset."
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
