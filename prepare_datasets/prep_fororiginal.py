import os
import argparse
import pandas as pd
from tqdm import tqdm

def create_manifest(source_dir, output_path):
    """
    Scans a directory with 'real' and 'fake' subfolders and creates a manifest CSV file.

    Args:
        source_dir (str): The path to the root directory of the dataset.
        output_path (str): The path where the output manifest.csv file will be saved.
    """

    if not os.path.isdir(source_dir):
        raise FileNotFoundError(f"Source directory not found at: {source_dir}")

    real_path = os.path.join(source_dir, 'real')
    fake_path = os.path.join(source_dir, 'fake')

    if not os.path.isdir(real_path):
        print(f"Warning: 'real' subfolder not found in {source_dir}. Skipping.")
    if not os.path.isdir(fake_path):
        print(f"Warning: 'fake' subfolder not found in {source_dir}. Skipping.")

    manifest_data = []
    supported_extensions = ('.wav', '.flac', '.mp3', '.ogg')
    
    # Process the 'real' directory
    if os.path.isdir(real_path):
        print(f"Scanning 'real' audio files in {real_path}...")
        for filename in tqdm(os.listdir(real_path)):
            if filename.lower().endswith(supported_extensions):
                # We use os.path.abspath to ensure the path is not relative
                # This makes the manifest file more portable and reliable
                audio_path = os.path.abspath(os.path.join(real_path, filename))
                manifest_data.append({
                    'audio_path': audio_path,
                    'label': 1  # 1 for bonafide/real
                })

    # Process the 'fake' directory
    if os.path.isdir(fake_path):
        print(f"Scanning 'fake' audio files in {fake_path}...")
        for filename in tqdm(os.listdir(fake_path)):
            if filename.lower().endswith(supported_extensions):
                audio_path = os.path.abspath(os.path.join(fake_path, filename))
                manifest_data.append({
                    'audio_path': audio_path,
                    'label': 0  # 0 for spoof/fake
                })

    if not manifest_data:
        print("Error: No audio files found. Manifest file will not be created.")
        return

    df = pd.DataFrame(manifest_data)
    df = df.reset_index(drop=True)

    try:
        df.to_csv(output_path, index=False)
        print(f"\nSuccessfully created manifest file with {len(df)} entries at:")
        print(output_path)
    except Exception as e:
        print(f"\nError saving manifest file: {e}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Prepare a dataset manifest from a directory with 'real' and 'fake' subfolders."
    )
    parser.add_argument(
        '--source_dir',
        type=str,
        required=True,
        help="Path to the source dataset directory containing 'real' and 'fake' subfolders."
    )
    parser.add_argument(
        '--output_path',
        type=str,
        required=True,
        help="Path to save the output manifest CSV file (e.g., data/my_dataset.csv)."
    )
    args = parser.parse_args()

    output_dir = os.path.dirname(args.output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    create_manifest(args.source_dir, args.output_path)
