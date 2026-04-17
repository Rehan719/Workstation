try:
    import cupy as cp
    HAS_CUPY = True
except ImportError:
    import numpy as cp
    HAS_CUPY = False

import numpy as np

def get_backend():
    """Return CuPy if available, else NumPy."""
    return cp if HAS_CUPY else np

def to_numpy(x):
    """Convert array to NumPy if it's a CuPy array."""
    if HAS_CUPY and hasattr(x, 'get'):
        return x.get()
    return x
