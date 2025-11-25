"""
Utility functions for handling JSON data with NaN values
"""

import math

# Try to import numpy, but handle case where it's not available
try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False
    np = None

def sanitize_json_data(data):
    """
    Recursively sanitize data to remove NaN values that are not valid in JSON
    
    Args:
        data: Any data structure (dict, list, float, etc.)
        
    Returns:
        Sanitized data with NaN values replaced by None
    """
    if isinstance(data, dict):
        return {key: sanitize_json_data(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [sanitize_json_data(item) for item in data]
    elif isinstance(data, float):
        # Check for NaN values
        if math.isnan(data) or math.isinf(data):
            return None
        return float(data)
    elif HAS_NUMPY and np is not None and isinstance(data, (np.float32, np.float64)):
        # Check for NaN values in numpy floats
        if np.isnan(data) or np.isinf(data):
            return None
        return float(data)
    elif HAS_NUMPY and np is not None and isinstance(data, (np.integer, np.int32, np.int64)):
        return int(data)
    elif HAS_NUMPY and np is not None and isinstance(data, np.bool_):
        return bool(data)
    else:
        return data

def safe_jsonify(data):
    """
    Safely prepare data for JSON serialization by handling NaN values
    
    Args:
        data: Dictionary containing data to be JSON serialized
        
    Returns:
        Sanitized dictionary safe for JSON serialization
    """
    return sanitize_json_data(data)