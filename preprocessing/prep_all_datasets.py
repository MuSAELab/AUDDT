import yaml
import argparse
import subprocess
import sys
import os

def prepare_all(config_path):
    """
    Reads a dataset configuration file and runs the preparation script for each entry,
    dynamically building arguments for each script.

    Args:
        config_path (str): Path to the datasets.yaml configuration file.
    """
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: Configuration file not found at {config_path}")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
        sys.exit(1)

    # --- 1. Get the root data path from the YAML itself ---
    data_root = config.get('ROOT_DATA')
    if not data_root:
        print("Error: 'ROOT_DATA' variable not defined at the top level of the YAML config.")
        sys.exit(1)
    
    # Expand user home directory if tilde is used (e.g., ~/data)
    data_root = os.path.expanduser(data_root)

    if 'datasets' not in config or not config['datasets']:
        print("Error: No 'datasets' found in the configuration file.")
        return

    # --- DEBUG: Print the detected root path ---
    print(f"DEBUG: Successfully read ROOT_DATA as: '{data_root}'")
    print("-" * 20)
    
    for i, dataset in enumerate(config['datasets']):
        name = dataset.get('name', f'Dataset {i+1}')
        script_path = dataset.get('script_path')
        args_dict = dataset.get('args')

        print("\n" + "="*80)
        print(f"({i+1}/{len(config['datasets'])}) Preparing: {name}")
        print("="*80)

        if not script_path or not args_dict:
            print(f"Skipping '{name}' due to missing 'script_path' or 'args' in config.")
            continue

        command = [sys.executable, script_path]
        
        for arg, value in args_dict.items():
            # --- DEBUG: Show original and processed values ---
            print(f"  - Processing arg: '{arg}' with original value: '{value}'")
            processed_value = value
            if isinstance(value, str):
                processed_value = value.replace('$ROOT_DATA', data_root)
                if processed_value != value:
                    print(f"    -> Placeholder found! New value: '{processed_value}'")
                else:
                    print(f"    -> No '$ROOT_DATA' placeholder found.")
            
            command.append(str(arg))
            command.append(str(processed_value))
        
        print(f"\nRunning command: {' '.join(command)}")

        try:
            result = subprocess.run(command, check=True, capture_output=True, text=True)
            print("--- Script Output ---")
            print(result.stdout)
            print("---------------------")
            print(f"Successfully prepared '{name}'.")
        except FileNotFoundError:
            print(f"Error: The script '{script_path}' was not found.")
        except subprocess.CalledProcessError as e:
            print(f"Error running script for '{name}'. Return code: {e.returncode}")
            print("--- Stderr ---")
            print(e.stderr)
            print("--------------")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Run dataset preparation for all datasets defined in a YAML config file."
    )
    parser.add_argument(
        '--config',
        type=str,
        default='configs/datasets.yaml',
        help="Path to the dataset configuration YAML file."
    )
    args = parser.parse_args()

    prepare_all(args.config)

