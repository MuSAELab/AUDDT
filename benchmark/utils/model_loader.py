import torch
import importlib.util
from pathlib import Path
import sys
import os

def load_model_from_path(model_py_path, model_class_name, checkpoint_path, device, model_args=None):
    """
    Dynamically loads a model class from a .py file, instantiates it,
    and loads a pretrained checkpoint. This function is designed to handle
    loading both raw models and wrapper models that themselves load a raw model.

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
    
    # Temporarily add the model's directory to the sys.path to allow relative imports
    model_dir = str(model_path.parent)
    if model_dir not in sys.path:
        sys.path.insert(0, model_dir)
        
    try:
        spec.loader.exec_module(model_module)

        # Get the model class from the imported module
        ModelClass = getattr(model_module, model_class_name)

        # Use an empty dictionary if model_args is not provided
        if model_args is None:
            model_args = {}

        # Special handling for the wrapper class
        if model_class_name == "AudioDeepfakeDetector":
            print("Detected wrapper model. Loading raw model first.")
            
            # Extract raw model arguments from the wrapper's model_args
            raw_model_path = model_args['raw_model_path']
            raw_model_class_name = model_args['raw_model_class_name']
            raw_model_args = model_args.get('raw_model_args', {})

            # Load the raw model
            raw_model = load_model_from_path(
                model_py_path=raw_model_path,
                model_class_name=raw_model_class_name,
                checkpoint_path=checkpoint_path,
                device=device,
                model_args=raw_model_args
            )
            # Instantiate the wrapper with the raw model
            model = ModelClass(raw_model)
        else:
            # Standard instantiation for a raw model
            print(f"Instantiating model with args: {model_args} on device: {device}")
            model = ModelClass(**model_args)
            
            # Load the state dictionary
            print(f"Loading checkpoint from: {checkpoint_path}")
            state_dict = torch.load(checkpoint_path, map_location='cpu')
            
            # Handle potential DataParallel wrapper keys (e.g., 'module.')
            if list(state_dict.keys())[0].startswith('module.'):
                state_dict = {k.replace('module.', ''): v for k, v in state_dict.items()}

            model.load_state_dict(state_dict)
    finally:
        # Clean up the sys.path modification
        if model_dir in sys.path:
            sys.path.remove(model_dir)

    # Move model to the specified device and set to evaluation mode
    model.to(device)
    model.eval()
    
    return model
