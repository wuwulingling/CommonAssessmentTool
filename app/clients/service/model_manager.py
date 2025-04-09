"""
Model Manager

Loads and manages machine learning models saved as .pkl files.
Provides functions to switch between them and retrieve current model info.
"""

import os
import pickle

# Get absolute path of current file
BASE_DIR = os.path.dirname(__file__)

# Map of model names to .pkl filenames
model_files = {
    "random_forest": "model_rf.pkl",
    "linear_regression": "model_lr.pkl",
    "decision_tree": "model_dt.pkl"
}

# Load all models on startup
models = {}
try:
    for name, path in model_files.items():
        # Try to load the model
        try:
            with open(path, 'rb') as f:
                models[name] = pickle.load(f)
        except (ModuleNotFoundError, ImportError):
            # If loading fails, create a dummy model instance
            print(f"Warning: Could not load model '{name}' from {path}. Using a placeholder model.")
            from sklearn.ensemble import RandomForestRegressor
            models[name] = RandomForestRegressor()
except Exception as e:
    print(f"Error loading models: {e}")
    # Use a minimal dummy model dictionary to allow the app to start
    from sklearn.ensemble import RandomForestRegressor
    models = {"default": RandomForestRegressor()}

# === Public functions ===

def list_models():
    """
    Returns a list of all available model names.
    """
    return list(models.keys())

def get_current_model_name():
    """
    Returns the name of the currently active model.
    """
    return current_model_name

def get_current_model():
    """
    Returns the actual model object currently in use.
    """
    return current_model

def switch_model(model_name: str):
    """
    Switches the currently active model to the given one.
    
    Args:
        model_name (str): One of the keys in model_files
        
    Raises:
        ValueError: If the model_name is not available
    """
    global current_model_name, current_model

    if model_name not in models:
        raise ValueError(f"Model '{model_name}' not found. Available: {list_models()}")

    current_model_name = model_name
    current_model = models[model_name]
