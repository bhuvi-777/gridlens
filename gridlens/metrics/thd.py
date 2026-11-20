"""Total harmonic distortion."""
import numpy as np


def thd(signal, fs, f0=50.0, max_harmonic=50):
    """Total harmonic distortion as a ratio (multiply by 100 for %).

    THD = sqrt(V2^2 + V3^2 + ... + Vn^2) / V1

    The signal should contain a whole number of fundamental cycles,
    otherwise spectral leakage will affect the result.
    """
    x = np.asarray(signal, dtype=float)
    spectrum = np.abs(np.fft.rfft(x))
    df = fs / x.size  # frequency resolution

    def magnitude(order):
        return spectrum[round(order * f0 / df)]

    top = min(max_harmonic, int((fs / 2) // f0))
    fundamental = magnitude(1)
    if fundamental == 0:
        raise ValueError("No fundamental component found at f0")

    harmonic_sum = sum(magnitude(h) ** 2 for h in range(2, top + 1))
    return float(np.sqrt(harmonic_sum) / fundamental)