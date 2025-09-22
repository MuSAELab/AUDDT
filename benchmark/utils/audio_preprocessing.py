import torch
import torchaudio

class WaveformProcessor:
    """
    A class to handle common audio waveform preprocessing steps, including
    resampling, mono conversion, amplitude normalization, and padding/trimming.
    """
    def __init__(self, target_sample_rate=16000, target_length=64000):
        """
        Initializes the waveform processor.

        Args:
            target_sample_rate (int): The target sample rate for all audio files.
            target_length (int, optional): The fixed number of samples for all
                                          waveforms. If None, no padding or
                                          trimming is performed.
        """
        self.target_sample_rate = target_sample_rate
        self.target_length = target_length

    def __call__(self, waveform, original_sample_rate):
        """
        Processes a raw waveform by applying resampling, mono conversion,
        and amplitude normalization, followed by padding/trimming.

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
        
        waveform = waveform.squeeze()

        # Convert to mono by averaging channels if necessary
        if waveform.ndim > 1:
            waveform = torch.mean(waveform, dim=0, keepdim=False)
            waveform = waveform.squeeze()

        # Amplitude normalization to [-1, 1]
        max_abs_val = torch.max(torch.abs(waveform))
        if max_abs_val > 0:
            waveform = waveform / (max_abs_val + 1e-8)
        
        # Apply padding or trimming to a fixed length
        if self.target_length is not None:
            current_len = waveform.shape[-1]
            if current_len < self.target_length:
                # Pad with zeros
                pad_len = self.target_length - current_len
                waveform = torch.nn.functional.pad(waveform, (0, pad_len))
            elif current_len > self.target_length:
                # Trim the waveform from the end
                waveform = waveform[:self.target_length]
            
        return waveform
