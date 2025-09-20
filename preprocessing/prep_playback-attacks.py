import os
import argparse
import pandas as pd
from tqdm import tqdm

def create_manifest_from_labels(source_dir, label_file, output_path):
    """
    Creates an enhanced manifest file from a directory of audios and an existing label file.

    Args:
        source_dir (str): Path to the directory containing all the audio files.
        label_file (str): Path to the existing CSV/TXT label file.
        output_path (str): Path to save the new, enhanced manifest CSV file.
    """
    # --- 1. Input Validation ---
    if not os.path.isdir(source_dir):
        raise FileNotFoundError(f"Audio source directory not found at: {source_dir}")
    if not os.path.isfile(label_file):
        raise FileNotFoundError(f"Label file not found at: {label_file}")

    print(f"Reading label file from: {label_file}")
    df = pd.read_csv(label_file)

    # Check if the key column ('rec_id' in your example) exists
    # You can change 'rec_id' if other datasets use a different column name for the filename
    key_column = 'rec_id'
    if key_column not in df.columns:
        raise ValueError(f"Key column '{key_column}' not found in the label file.")

    # Convert the key column to string to ensure proper joining, just in case
    df[key_column] = df[key_column].astype(str)

    # --- 2. Generate 'audio_path' Column ---
    print("Generating absolute audio paths...")
    # This creates the full path for each audio file. Assumes a .wav extension.
    # Change '.wav' if your audio files have a different format (e.g., '.flac').
    df['audio_path'] = df[key_column].apply(
        lambda rec_id: os.path.abspath(os.path.join(source_dir, f"{rec_id}.wav"))
    )

    # --- 3. Generate 'label' Column ---
    print("Generating labels...")
    # As you specified, for this particular dataset, all audios are real (label=1).
    df['label'] = 1
    
    # NOTE: For a different dataset that has both authentic and spoof types,
    # you could use logic like this instead:
    #
    # if 'rec_type' in df.columns:
    #     df['label'] = df['rec_type'].apply(lambda x: 1 if x == 'authentic' else 0)
    # else:
    #     # Default or error if the column doesn't exist
    #     raise ValueError("'rec_type' column not found for generating labels.")

    # --- 4. (Optional but Recommended) Verify Audio Files Exist ---
    print("Verifying that audio files exist...")
    missing_files = 0
    for path in tqdm(df['audio_path'], desc="Checking files"):
        if not os.path.exists(path):
            missing_files += 1
            # print(f"  - Warning: File not found: {path}") # Uncomment for verbose debugging
    
    if missing_files > 0:
        print(f"\nWarning: {missing_files} audio file(s) listed in the label file were not found on disk.")
        print("The manifest has been created, but these entries will cause errors during training/evaluation.")

    # --- 5. Reorder Columns for Clarity ---
    # Get all original columns and make sure our new columns are first.
    original_cols = [col for col in df.columns if col not in ['audio_path', 'label']]
    new_col_order = ['audio_path', 'label'] + original_cols
    df = df[new_col_order]

    # --- 6. Save the Final Manifest ---
    try:
        df.to_csv(output_path, index=False)
        print(f"\nSuccessfully created enhanced manifest with {len(df)} entries at:")
        print(output_path)
    except Exception as e:
        print(f"\nError saving manifest file: {e}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Prepare a dataset manifest from an audio directory and an existing label file."
    )
    # This argument is renamed for clarity to distinguish from the label file itself.
    parser.add_argument(
        '--source_dir',
        type=str,
        required=True,
        help="Path to the source directory containing the raw audio files."
    )
    parser.add_argument(
        '--label_file',
        type=str,
        required=True,
        help="Path to the existing label CSV file."
    )
    parser.add_argument(
        '--output_path',
        type=str,
        required=True,
        help="Path to save the new, enhanced manifest CSV file."
    )
    args = parser.parse_args()

    # Ensure the output directory exists
    output_dir = os.path.dirname(args.output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    create_manifest_from_labels(args.source_dir, args.label_file, args.output_path)
