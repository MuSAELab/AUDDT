import numpy as np
import torch
import torch.nn as nn
from models.baseline_model import Model

class AudioDeepfakeDetector(nn.Module):
    def __init__(self, pretrained_model):
        super().__init__()
        self.model = pretrained_model
    
    def get_prediction_score(self, x):
        """
        Retrieve the raw score output from the pretrained model.
        If model gives two/more output neurons, indexing is needed to obtain a single score.
        """
        # x = self.shape_transform(x)
        raw_output = self.model(x)
        if raw_output.dim() > 1 and raw_output.size(1) > 1:
            # Assumes the score for the positive class (e.g., fake) is the second neuron
            score = raw_output[:, 1]
        else:
            score = raw_output.squeeze()
        return score

    def forward(self, x):
        return self.get_prediction_score(x)
    
    def shape_transform(self, x):
        return x.unsqueeze(1)