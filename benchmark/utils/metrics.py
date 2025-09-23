import numpy as np
from sklearn.metrics import roc_curve, roc_auc_score, confusion_matrix

def calculate_metrics(labels, scores):
    """
    Calculates EER, Accuracy, TPR, TNR, and AUC.
    
    For datasets with only one class, returns metrics that can still be computed.
    
    Args:
        labels (list or np.array): True labels (0 for bonafide, 1 for spoof).
        scores (list or np.array): Raw prediction scores from the model.
        
    Returns:
        dict: A dictionary containing all calculated metrics.
    """
    labels = np.array(labels)
    scores = np.array(scores)

    # Check for single-class datasets
    unique_labels = np.unique(labels)
    if len(unique_labels) < 2:
        print("Warning: Only one class present in labels. EER and AUC cannot be computed.")
        
        # Determine the single class present
        single_class = unique_labels[0]
        
        # Calculate accuracy based on a threshold (e.g., 0.5)
        predictions = (scores >= 0.5).astype(int)
        accuracy = np.mean(predictions == labels)
        
        # Calculate TPR/TNR based on the single class
        if single_class == 1: # Spoof class
            tpr_val = np.mean(predictions[labels == 1] == 1) if len(labels[labels == 1]) > 0 else 0.0
            tnr_val = -1
        else: # Bonafide class
            tpr_val = -1
            tnr_val = np.mean(predictions[labels == 0] == 0) if len(labels[labels == 0]) > 0 else 0.0

        return {
            'eer': -1,
            'accuracy': accuracy,
            'tpr': tpr_val,
            'tnr': tnr_val,
            'auc': -1
        }

    # EER and AUC Calculation
    fpr, tpr, thresholds = roc_curve(labels, scores, pos_label=1)
    fnr = 1 - tpr
    eer_index = np.nanargmin(np.abs(fnr - fpr))
    eer_threshold = thresholds[eer_index]
    eer = fpr[eer_index]
    auc = roc_auc_score(labels, scores)

    # Accuracy, TPR, TNR Calculation
    predictions = (scores >= 0.5).astype(int)
    
    # Use confusion matrix to get TP, TN, FP, FN
    tn, fp, fn, tp = confusion_matrix(labels, predictions, labels=[0, 1]).ravel()
    
    accuracy = (tp + tn) / (tp + tn + fp + fn)
    
    # True Positive Rate (TPR) / Recall
    tpr_val = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    
    # True Negative Rate (TNR) / Specificity
    tnr_val = tn / (tn + fp) if (tn + fp) > 0 else 0.0

    return {
        'eer': eer,
        'auc': auc,
        'accuracy': accuracy,
        'tpr': tpr_val,
        'tnr': tnr_val
    }
