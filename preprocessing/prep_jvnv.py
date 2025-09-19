import pandas as pd
import argparse
from pathlib import Path
from tqdm import tqdm

def prepare_dataset(source_dir, output_path):
    """
    Prepares a manifest file for the JVNV dataset.

    This script walks through a directory structure like:
    - F1/
    - F2/
    - M1/
      - anger/
        - free/
          - M1_anger_free_01.wav
    and extracts speaker_id, emotion, and label for each audio file.

    Args:
        source_dir (str): The root directory of the dataset.
        output_path (str): The path to save the final manifest CSV file.
    """
    source_path = Path(source_dir).resolve()

    if not source_path.is_dir():
        print(f"Error: Source directory '{source_path}' not found.")
        return

    print(f"Scanning for audio files in: {source_path}")
    # Using glob to find all .wav files in the expected nested structure.
    # The pattern * / * / * / *.wav corresponds to speaker/emotion/subfolder/audio.wav
    audio_files = list(source_path.glob('*/*/*/*.wav'))

    if not audio_files:
        print(f"Error: No .wav files found with the expected directory structure in {source_path}.")
        return

    print(f"Found {len(audio_files)} audio files to process.")
    
    all_records = []
    for audio_path in tqdm(audio_files, desc="Processing audio files"):
        try:
            # Get the path relative to the source directory to extract parts
            relative_path = audio_path.relative_to(source_path)
            
            # The parts of the path will be ['M2', 'anger', 'free', 'audio.wav']
            parts = relative_path.parts
            
            if len(parts) >= 3:
                speaker_id = parts[0]
                emotion = parts[1]
                
                record = {
                    'audio_path': str(audio_path),
                    'label': 'bonafide', # all audios in JVNV are real human voice
                    'speaker_id': speaker_id,
                    'emotion': emotion,
                }
                all_records.append(record)
            else:
                 print(f"Warning: Skipping file with unexpected path structure: {audio_path}")

        except Exception as e:
            print(f"Warning: Could not process file {audio_path}. Error: {e}")

    if not all_records:
        print("Error: No valid records were created.")
        return

    # Create the final DataFrame
    final_df = pd.DataFrame(all_records)
    
    # Ensure a consistent column order
    final_df = final_df[['audio_path', 'label', 'speaker_id', 'emotion']]

    print(f"Final manifest size: {len(final_df)} entries.")
    
    # Save the manifest file
    output_path_obj = Path(output_path)
    output_path_obj.parent.mkdir(parents=True, exist_ok=True)
    final_df.to_csv(output_path_obj, index=False)
    
    print(f"Manifest file successfully created at: {output_path_obj}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Prepare a dataset manifest for the emotion dataset."
    )
    parser.add_argument(
        '--source_dir',
        type=str,
        required=True,
        help="The root directory of the emotion dataset."
    )
    parser.add_argument(
        '--output_path',
        type=str,
        required=True,
        help="The path to save the final manifest CSV file."
    )
    
    args = parser.parse_args()
    prepare_dataset(args.source_dir, args.output_path)
