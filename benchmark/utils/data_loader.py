import torch
import pandas as pd
import torchaudio
from torch.utils.data import Dataset
from .audio_preprocessing import WaveformProcessor

class AudioManifestDataset(Dataset):
    """
    A PyTorch Dataset for loading and preprocessing audio from a manifest file.
    Assumes a CSV with 'audio_path' and 'label' columns.
    """
    def __init__(self, manifest_path, target_sample_rate=16000, target_length=64000):
        """
        Initializes the dataset.

        Args:
            manifest_path (str): Path to the manifest CSV file.
            target_sample_rate (int): The target sample rate for all audio files.
            target_length (int, optional): The fixed number of samples for all
                                          waveforms. If None, no padding or
                                          trimming is performed.
        """
        # Specify dtype for column 4 to prevent DtypeWarning
        self.df = pd.read_csv(manifest_path, dtype={4: str})
        self.df['label'] = self.df['label'].apply(lambda x: 0 if x == 'bonafide' else 1)
        # Instantiate the waveform processor with the target length
        self.processor = WaveformProcessor(
            target_sample_rate=target_sample_rate,
            target_length=target_length
        )
        
    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        row = self.df.iloc[idx]
        audio_path = row['audio_path']
        label = row['label']
        
        try:
            waveform, sample_rate = torchaudio.load(audio_path)
            processed_waveform = self.processor(waveform, sample_rate)
            return processed_waveform, label
        
        except Exception as e:
            print(f"Error loading or processing file {audio_path}: {e}")
            # Return a dummy tensor with the correct shape on error
            dummy_waveform = torch.zeros(self.processor.target_length)
            return dummy_waveform, -1
