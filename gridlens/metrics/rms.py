"""RMS value of a sampled signal."""
import numpy as np


def rms(signal):
    """Root mean square of a signal."""
    x = np.asarray(signal, dtype=float)
    return float(np.sqrt(np.mean(np.square(x))))