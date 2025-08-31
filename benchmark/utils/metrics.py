import numpy as np
from sklearn.metrics import roc_curve, roc_auc_score, confusion_matrix

def calculate_metrics(labels, scores):
    """
    Calculates EER, Accuracy, TPR, TNR, and AUC.
    
    For datasets with only one class, returns -1 for all metrics that cannot be computed.
    
    Args:
        labels (list or np.array): True labels (0 for bonafide, 1 for spoof).
        scores (list or np.array): Raw prediction scores from the model.
        
    Returns:
        dict: A dictionary containing all calculated metrics.
    """
    labels = np.array(labels)
    scores = np.array(scores)

    # Handle the single-class case
    if len(np.unique(labels)) < 2:
        print("Warning: Only one class present in labels. Metrics cannot be computed.")
        return {'eer': -1, 'accuracy': -1, 'tpr': -1, 'tnr': -1, 'auc': -1}

    # --- EER and AUC Calculation ---
    fpr, tpr, thresholds = roc_curve(labels, scores, pos_label=1)
    fnr = 1 - tpr
    eer_index = np.nanargmin(np.abs(fnr - fpr))
    eer_threshold = thresholds[eer_index]
    eer = fpr[eer_index]
    auc = roc_auc_score(labels, scores)

    # --- Accuracy, TPR, TNR Calculation (at the EER threshold) ---
    # Apply the threshold that gives the EER to get binary predictions
    predictions = (scores >= eer_threshold).astype(int)
    
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

