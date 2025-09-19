import torch
import torchaudio

class WaveformProcessor:
    """
    A class to handle common audio waveform preprocessing steps.
    """
    def __init__(self, target_sample_rate=16000):
        self.target_sample_rate = target_sample_rate

    def __call__(self, waveform, original_sample_rate):
        """
        Processes a raw waveform by applying resampling, mono conversion,
        and amplitude normalization.

        Args:
            waveform (torch.Tensor): The input waveform tensor of shape (channels, time).
            original_sample_rate (int): The original sample rate of the waveform.

        Returns:
            torch.Tensor: The processed waveform tensor.
        """
        # Resample to target sampling rate
        if original_sample_rate != self.target_sample_rate:
            resampler = torchaudio.transforms.Resample(
                orig_freq=original_sample_rate, 
                new_freq=self.target_sample_rate
            )
            waveform = resampler(waveform)

        # Convert to mono by averaging channels if necessary
        if waveform.shape[0] > 1:
            waveform = torch.mean(waveform, dim=0)

        # Amplitude normalization to [-1, 1]
        max_abs_val = torch.max(torch.abs(waveform))
        if max_abs_val > 0:
            waveform = waveform / (max_abs_val + 1e-8)
            
        return waveform
