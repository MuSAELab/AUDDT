import torch
import pandas as pd
import numpy as np
import yaml
import argparse
from torch.utils.data import DataLoader
from tqdm import tqdm
import os
import sys

from benchmark.utils.data_loader import AudioManifestDataset
from benchmark.utils.metrics import calculate_metrics
from benchmark.utils.model_loader import load_model_from_path
from benchmark.generate_latex_table import generate_latex_from_metrics
from models.detector_wrapper import AudioDeepfakeDetector

def run_evaluation(model, dataloader, device):
    """
    Runs the model over the dataset and collects scores and labels.
    """
    all_scores = []
    all_labels = []
    
    with torch.no_grad():
        for waveforms, labels in tqdm(dataloader, desc="Evaluating"):
            # Skip batches with loading errors
            if -1 in labels:
                continue
            
            waveforms = waveforms.to(device)
            scores = model.get_prediction_score(waveforms)
            
            all_scores.extend(scores.cpu().numpy().flatten())
            all_labels.extend(labels.numpy().flatten())
            
    return all_labels, all_scores

def main(config):
    """
    Main function to orchestrate the evaluation pipeline, driven by a config dictionary.
    """
    # Extract config sections for clarity
    model_cfg = config['model']
    data_cfg = config['data']
    eval_cfg = config['evaluation_settings']
    
    # --- Device Configuration ---
    device_str = eval_cfg.get('device', 'auto')
    if device_str == 'auto':
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    else:
        try:
            device = torch.device(device_str)
            if 'cuda' in device_str:
                if not torch.cuda.is_available():
                     raise RuntimeError("CUDA is not available, but a CUDA device was specified.")
                torch.cuda.get_device_name(device)
        except Exception as e:
            print(f"\n--- ERROR ---")
            print(f"Could not initialize the specified device '{device_str}'.")
            print(f"Original error: {e}")
            sys.exit(1)

    print(f"Using device: {device}")
    
    # Create results directory
    os.makedirs(eval_cfg['results_dir'], exist_ok=True)
    
    # Get model-specific arguments from the config, defaulting to an empty dict
    model_args = model_cfg.get('model_args', {})
    
    # Load the raw pretrained detector
    print(f"Loading raw model '{model_cfg['class_name']}' from '{model_cfg['checkpoint']}'...")
    raw_model = load_model_from_path(
        model_py_path=model_cfg['path'], 
        model_class_name=model_cfg['class_name'], 
        checkpoint_path=model_cfg['checkpoint'], 
        device=device,
        model_args=model_args,
    )

    # Wrap the raw model with the new class
    # Pass the raw_model object itself, not the config arguments
    model = AudioDeepfakeDetector(raw_model)
    model.to(device) # Ensure the wrapped model is on the correct device

    # Determine which datasets to evaluate
    datasets_to_evaluate = []
    if data_cfg.get('manifest_path'):
        manifest_path = data_cfg['manifest_path']
        datasets_to_evaluate.append({"name": os.path.basename(manifest_path).split('.')[0], "manifest_path": manifest_path})
    elif data_cfg.get('group_name'):
        with open(data_cfg['groups_config_path'], 'r') as f:
            groups = yaml.safe_load(f)
        group_name = data_cfg['group_name']
        if group_name not in groups:
            raise ValueError(f"Dataset group '{group_name}' not found in {data_cfg['groups_config_path']}")
        datasets_to_evaluate = groups[group_name]
    else:
        raise ValueError("Config error: You must specify either 'manifest_path' or 'group_name' in the data section.")
    
    # Get dataset-specific arguments from the config, defaulting to an empty dict
    data_args = data_cfg.get('data_args', {})
    
    # --- Loop through each dataset and run the evaluation ---
    group_results = {}
    for dataset_info in datasets_to_evaluate:
        dataset_name = dataset_info['name']
        manifest_path = dataset_info['manifest_path']
        
        print(f"\n--- Evaluating on: {dataset_name} ---")
        if not os.path.exists(manifest_path):
            print(f"Warning: Manifest file not found at {manifest_path}. Skipping.")
            continue
            
        dataset = AudioManifestDataset(manifest_path, **data_args)
        dataloader = DataLoader(dataset, batch_size=eval_cfg['batch_size'], shuffle=False, num_workers=4)
        
        labels, scores = run_evaluation(model, dataloader, device)
        
        # Calculate metrics
        metrics = calculate_metrics(labels, scores)
        group_results[dataset_name] = metrics
        
        print(f"Results for {dataset_name}:")
        if metrics['eer'] == -1:
            print(f"  -> Single class dataset. Accuracy: {metrics.get('accuracy', 0)*100:.2f}%")
        else:
            print(f"  EER: {metrics['eer']*100:.2f}% | AUC: {metrics['auc']:.4f} | Accuracy: {metrics['accuracy']*100:.2f}%")
            print(f"  TPR: {metrics['tpr']*100:.2f}% | TNR: {metrics['tnr']*100:.2f}%")

        # Save detailed scores
        results_df = pd.DataFrame({'score': scores, 'label': labels})
        output_path = os.path.join(eval_cfg['results_dir'], f"{model_cfg['class_name']}_on_{dataset_name}_scores.csv")
        results_df.to_csv(output_path, index=False)
        print(f"Detailed scores saved to {output_path}")

    # --- Print summary if a group was evaluated ---
    if data_cfg.get('group_name'):
        group_name = data_cfg['group_name']
        print(f"\n--- Summary for group '{group_name}' ---")
        for name, metrics in group_results.items():
             if metrics['eer'] == -1:
                 print(f"- {name}: Single class dataset (Acc={metrics.get('accuracy', 0)*100:.2f}%)")
             else:
                 print(f"- {name}: EER={metrics['eer']*100:.2f}%, AUC={metrics['auc']:.4f}, Acc={metrics['accuracy']*100:.2f}%")

        valid_results = [m for m in group_results.values() if m['eer'] != -1]
        
        if valid_results:
            avg_eer = np.mean([m['eer'] for m in valid_results])
            avg_auc = np.mean([m['auc'] for m in valid_results])
            avg_acc = np.mean([m['accuracy'] for m in valid_results])
            avg_tpr = np.mean([m['tpr'] for m in valid_results])
            avg_tnr = np.mean([m['tnr'] for m in valid_results])
            
            print("---------------------------------")
            print("Average Metrics (for multi-class datasets):")
            print(f"  EER: {avg_eer*100:.2f}% | AUC: {avg_auc:.4f} | Accuracy: {avg_acc*100:.2f}%")
            print(f"  TPR: {avg_tpr*100:.2f}% | TNR: {avg_tnr*100:.2f}%")
        else:
            print("---------------------------------")
            print("No multi-class datasets were evaluated to calculate average metrics.")

    # --- Save consolidated metrics to a YAML file ---
    run_name = data_cfg.get('group_name') or os.path.basename(data_cfg['manifest_path']).split('.')[0]
    metrics_output_path = os.path.join(eval_cfg['results_dir'], f"{model_cfg['class_name']}_on_{run_name}_metrics.yaml")
    with open(metrics_output_path, 'w') as f:
        yaml.dump(group_results, f, default_flow_style=False, sort_keys=False)
    print(f"\nConsolidated metrics saved to {metrics_output_path}")

    # --- Generate LaTeX table if requested ---
    if eval_cfg.get('latex_output_path'):
        generate_latex_from_metrics(metrics_output_path, eval_cfg['latex_output_path'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Standalone Audio Deepfake Detection Benchmark")
    parser.add_argument(
        '--config', 
        type=str, 
        required=True, 
        help="Path to the evaluation setup YAML file (e.g., evaluate_setup.yaml)"
    )
    args = parser.parse_args()

    # Load configuration from the YAML file
    with open(args.config, 'r') as f:
        config = yaml.safe_load(f)
    
    # Run the main evaluation logic with the loaded config
    main(config)
