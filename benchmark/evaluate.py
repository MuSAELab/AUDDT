import torch
import pandas as pd
import numpy as np
import yaml
import argparse
import os
from torch.utils.data import DataLoader
from tqdm import tqdm

from utils.data_loader import AudioManifestDataset
from utils.metrics import calculate_metrics
from utils.model_loader import load_model_from_path
from generate_latex_table import generate_latex_from_metrics

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
            
            # Get model predictions (assuming model returns raw scores/logits)
            scores = model(waveforms)
            
            all_scores.extend(scores.cpu().numpy().flatten())
            all_labels.extend(labels.numpy().flatten())
            
    return all_labels, all_scores

def main(args):
    """
    Main function to orchestrate the evaluation pipeline.
    """

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")
    
    # Create results directory
    os.makedirs(args.results_dir, exist_ok=True)
    
    # Load the pretrained detector
    print(f"Loading model '{args.model_name}' from '{args.checkpoint_path}'...")
    model = load_model_from_path(args.model_path, args.model_name, args.checkpoint_path, device)

    # Determine which datasets to evaluate
    datasets_to_evaluate = []
    if args.data_csv:
        datasets_to_evaluate.append({"name": os.path.basename(args.data_csv).split('.')[0], "manifest_path": args.data_csv})
    else: # A group was specified
        with open(args.groups_config, 'r') as f:
            groups = yaml.safe_load(f)
        if args.dataset_group not in groups:
            raise ValueError(f"Dataset group '{args.dataset_group}' not found in {args.groups_config}")
        datasets_to_evaluate = groups[args.dataset_group]

    # --- Loop through each dataset and run the evaluation ---
    group_results = {}
    for dataset_info in datasets_to_evaluate:
        dataset_name = dataset_info['name']
        manifest_path = dataset_info['manifest_path']
        
        print(f"\n--- Evaluating on: {dataset_name} ---")
        if not os.path.exists(manifest_path):
            print(f"Warning: Manifest file not found at {manifest_path}. Skipping.")
            continue
            
        dataset = AudioManifestDataset(manifest_path)
        dataloader = DataLoader(dataset, batch_size=args.batch_size, shuffle=False)
        
        labels, scores = run_evaluation(model, dataloader, device)
        
        # Calculate metrics
        metrics = calculate_metrics(labels, scores)
        group_results[dataset_name] = metrics
        
        print(f"Results for {dataset_name}:")
        if metrics['eer'] == -1:
            # We only calculate accuracy for the ones that do not have both classes
            print(f"  -> Single class dataset. Accuracy: {metrics.get('accuracy', 0)*100:.2f}%")
        else:
            print(f"  EER: {metrics['eer']*100:.2f}% | AUC: {metrics['auc']:.4f} | Accuracy: {metrics['accuracy']*100:.2f}%")
            print(f"  TPR: {metrics['tpr']*100:.2f}% | TNR: {metrics['tnr']*100:.2f}%")

        # Save detailed scores
        results_df = pd.DataFrame({'score': scores, 'label': labels})
        output_path = os.path.join(args.results_dir, f"{args.model_name}_on_{dataset_name}_scores.csv")
        results_df.to_csv(output_path, index=False)
        print(f"Detailed scores saved to {output_path}")

    # --- Print summary if a group was evaluated ---
    if args.dataset_group:
        print(f"\n--- Summary for group '{args.dataset_group}' ---")
        for name, metrics in group_results.items():
             if metrics['eer'] == -1:
                 print(f"- {name}: Single class dataset (Acc={metrics.get('accuracy', 0)*100:.2f}%)")
             else:
                 print(f"- {name}: EER={metrics['eer']*100:.2f}%, AUC={metrics['auc']:.4f}, Acc={metrics['accuracy']*100:.2f}%")

        # Calculate and print average metrics, ignoring single-class datasets
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
    run_name = args.dataset_group if args.dataset_group else os.path.basename(args.data_csv).split('.')[0]
    metrics_output_path = os.path.join(args.results_dir, f"{args.model_name}_on_{run_name}_metrics.yaml")
    with open(metrics_output_path, 'w') as f:
        # Use sort_keys=False to maintain the order from the config file
        yaml.dump(group_results, f, default_flow_style=False, sort_keys=False)
    print(f"\nConsolidated metrics saved to {metrics_output_path}")

    # --- Generate LaTeX table if requested ---
    if args.latex_output_path:
        generate_latex_from_metrics(metrics_output_path, args.latex_output_path)


if __name__ == '__main__':
    # --- Argument Parsing ---
    parser = argparse.ArgumentParser(description="Standalone Audio Deepfake Detection Benchmark")
    
    # Model arguments
    parser.add_argument('--model_path', type=str, required=True, help="Path to the model's .py file (e.g., models/custom_model.py)")
    parser.add_argument('--model_name', type=str, required=True, help="Name of the model class within the .py file (e.g., MyModel)")
    parser.add_argument('--checkpoint_path', type=str, required=True, help="Path to the pretrained model checkpoint (.pth file)")
    
    # Data arguments
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--data_csv', type=str, help="Path to a single manifest CSV file for evaluation.")
    group.add_argument('--dataset_group', type=str, help="Name of a dataset group defined in the groups config file.")
    
    # Config and runtime arguments
    parser.add_argument('--groups_config', type=str, default='benchmarks/hparams/dataset_groups.yaml', help="Path to the dataset groups YAML file.")
    parser.add_argument('--results_dir', type=str, default='results', help="Directory to save evaluation results.")
    parser.add_argument('--batch_size', type=int, default=16, help="Batch size for evaluation.")
    parser.add_argument('--latex_output_path', type=str, help="Optional: Path to save a LaTeX .tex file with the results table.")
    
    args = parser.parse_args()
    
    # --- Run the main evaluation logic ---
    main(args)

