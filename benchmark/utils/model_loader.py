import torch
import importlib.util
from pathlib import Path

def load_model_from_path(model_py_path, model_class_name, checkpoint_path, device, model_args=None):
    """
    Dynamically loads a model class from a .py file, instantiates it,
    and loads a pretrained checkpoint.

    Args:
        model_py_path (str): Path to the model's .py file.
        model_class_name (str): Name of the model class within the .py file.
        checkpoint_path (str): Path to the pretrained model checkpoint.
        device (torch.device): The device to load the model onto.
        model_args (dict, optional): Dictionary of arguments to pass to the model's __init__. Defaults to None.

    Returns:
        torch.nn.Module: The loaded and pretrained model.
    """
    model_path = Path(model_py_path)
    if not model_path.exists():
        raise FileNotFoundError(f"Model script not found at: {model_path}")

    # Dynamically import the model module
    spec = importlib.util.spec_from_file_location(model_path.stem, model_path)
    model_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(model_module)

    # Get the model class from the imported module
    ModelClass = getattr(model_module, model_class_name)

    # Use an empty dictionary if model_args is not provided
    if model_args is None:
        model_args = {}

    print(f"Instantiating model with args: {model_args} on device: {device}")
    model = ModelClass(**model_args)

    # Load the state dictionary
    print(f"Loading checkpoint from: {checkpoint_path}")
    state_dict = torch.load(checkpoint_path, map_location='cpu')
    
    # Handle potential DataParallel wrapper keys (e.g., 'module.')
    if list(state_dict.keys())[0].startswith('module.'):
        state_dict = {k.replace('module.', ''): v for k, v in state_dict.items()}

    model.load_state_dict(state_dict)
    
    # Move model to the specified device and set to evaluation mode
    model.to(device)
    model.eval()
    
    return model

