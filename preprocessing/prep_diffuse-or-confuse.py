import pandas as pd
import argparse
from pathlib import Path
from tqdm import tqdm

def prepare_dataset(source_dir, output_path):
    """
    Prepares a manifest file for DiffuseOrConfuse.

    The script first builds a mapping of model names (e.g., 'wavegrad2') to their
    full path (e.g., '/path/to/dataset_01/wavegrad2'). It then reads all
    '_proto.txt' files from the 'protocols' directory and uses the mapping to
    resolve the full audio path for each entry.

    Args:
        source_dir (str): The root directory of the dataset.
        output_path (str): The path to save the final manifest CSV file.
    """
    source_path = Path(source_dir).resolve()
    protocols_path = source_path / 'metadata' / 'metadata' / 'protocols'

    if not source_path.is_dir() or not protocols_path.is_dir():
        print(f"Error: Source directory '{source_path}' or protocols directory '{protocols_path}' not found.")
        return

    print("Building a map of model audio locations...")
    model_path_map = {}
    dataset_dirs = [d for d in source_path.iterdir() if d.is_dir() and d.name.startswith('dataset_')]
    
    for d_dir in tqdm(dataset_dirs, desc="Scanning dataset folders"):
        model_dirs = [m for m in d_dir.iterdir() if m.is_dir()]
        for m_dir in model_dirs:
            model_path_map[m_dir.name] = m_dir

    if not model_path_map:
        print("Error: No model subfolders (e.g., 'wavegrad2') found within any 'dataset_xx' directory.")
        return
    print(f"Found {len(model_path_map)} unique model folders.")

    # Process all protocol files
    protocol_files = list(protocols_path.glob('*_proto.txt'))
    if not protocol_files:
        print(f"Error: No '*_proto.txt' files found in '{protocols_path}'.")
        return

    print(f"\nProcessing {len(protocol_files)} protocol files...")
    all_records = []

    for proto_file in tqdm(protocol_files, desc="Processing protocols"):
        try:
            df = pd.read_csv(proto_file, sep='|')
            
            for _, row in df.iterrows():
                record = row.to_dict()
                relative_path_str = row['FILE_PATH']
                
                # The model name is the first part of the relative path
                model_name = Path(relative_path_str).parts[0]
                
                if model_name in model_path_map:

                    base_model_path = model_path_map[model_name]
                    audio_path = base_model_path / row['FILE_NAME']
                    
                    if audio_path.exists():
                        record['audio_path'] = str(audio_path)
                        label_str = str(row['TYPE']).lower()
                        record['label'] = 'spoof' if 'spoof' in label_str else 'bonafide'
                        all_records.append(record)
                    else:
                        # This can happen if the FILE_PATH has deeper nesting
                        # Fallback to the full relative path from the protocol
                        audio_path_fallback = base_model_path.parent / relative_path_str
                        if audio_path_fallback.exists():
                             record['audio_path'] = str(audio_path_fallback)
                             label_str = str(row['TYPE']).lower()
                             record['label'] = 'spoof' if 'spoof' in label_str else 'bonafide'
                             all_records.append(record)
                        else:
                            # print(f"Warning: Audio file not found at '{audio_path}' or '{audio_path_fallback}'. Skipping.")
                            pass

                else:
                    # print(f"Warning: Model '{model_name}' from protocol '{proto_file.name}' not found in any dataset folder. Skipping.")
                    pass

        except Exception as e:
            print(f"Warning: Could not process protocol file {proto_file.name}. Error: {e}")

    if not all_records:
        print("Error: No valid audio records could be processed from the protocol files.")
        return

    final_df = pd.DataFrame(all_records)
    
    # Reorder columns for consistency
    original_cols = list(pd.read_csv(protocol_files[0], sep='|').columns)
    final_cols = ['audio_path', 'label'] + original_cols
    final_df = final_df[final_cols]

    print(f"\nFinal manifest size: {len(final_df)} entries.")
    
    output_path_obj = Path(output_path)
    output_path_obj.parent.mkdir(parents=True, exist_ok=True)
    final_df.to_csv(output_path_obj, index=False)
    
    print(f"Manifest file successfully created at: {output_path_obj}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Prepare a dataset manifest from a complex protocol-based structure."
    )
    parser.add_argument(
        '--source_dir',
        type=str,
        required=True,
        help="The root directory containing 'dataset_xx' and 'protocols' folders."
    )
    parser.add_argument(
        '--output_path',
        type=str,
        required=True,
        help="The path to save the final manifest CSV file."
    )
    
    args = parser.parse_args()
    prepare_dataset(args.source_dir, args.output_path)
