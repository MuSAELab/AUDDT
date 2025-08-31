import torch
import torchaudio
import pandas as pd
from torch.utils.data import Dataset

class AudioManifestDataset(Dataset):
    """
    A PyTorch Dataset for loading audio from a manifest file.
    Assumes a CSV with 'wav_path' and 'label' columns.
    """
    def __init__(self, manifest_path):
        self.df = pd.read_csv(manifest_path)
        # Convert labels ('bonafide', 'spoof') to numeric (0, 1)
        self.df['label'] = self.df['label'].apply(lambda x: 0 if x == 'bonafide' else 1)
        
    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        row = self.df.iloc[idx]
        wav_path = row['wav_path']
        label = row['label']
        
        # Load waveform
        try:
            waveform, sample_rate = torchaudio.load(wav_path)
            # You might want to resample here if your models expect a specific sample rate
            return waveform, label
        except Exception as e:
            print(f"Error loading file {wav_path}: {e}")
            # Return a dummy tensor and label on error
            return torch.zeros(1, 16000), -1
