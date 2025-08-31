import torch
import importlib.util

def load_model_from_path(model_filepath, class_name, checkpoint_path, device):
    """
    Dynamically imports a model class from a Python file and loads its weights.

    Args:
        model_filepath (str): The path to the .py file (e.g., 'models/my_model.py').
        class_name (str): The name of the model class in the file.
        checkpoint_path (str): The path to the .pth model checkpoint.
        device (torch.device): The device to load the model onto.

    Returns:
        torch.nn.Module: The instantiated and loaded model.
    """
    spec = importlib.util.spec_from_file_location(class_name, model_filepath)
    model_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(model_module)
    
    # Get the class from the loaded module
    ModelClass = getattr(model_module, class_name)
    
    # Instantiate the model
    model = ModelClass()
    
    # Load the checkpoint
    model.load_state_dict(torch.load(checkpoint_path, map_location=device))
    model.to(device)
    model.eval() # Set model to evaluation mode
    
    return model
