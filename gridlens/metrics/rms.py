"""RMS value of a sampled signal."""
import numpy as np


def rms(signal):
    """Root mean square of a signal."""
    x = np.asarray(signal, dtype=float)
    return float(np.sqrt(np.mean(np.square(x))))


def rms_half_cycle(signal, fs, f0=50.0):
    """RMS over one cycle, refreshed every half cycle (as in IEC 61000-4-30).

    Returns (values, times): the RMS values and the time in seconds at
    which each one-cycle window starts.
    """
    x = np.asarray(signal, dtype=float)
    n = round(fs / f0)  # samples per cycle
    step = n // 2
    if step < 1:
        raise ValueError("Sampling rate is too low for this fundamental frequency")
    if x.size < n:
        raise ValueError("Signal is shorter than one cycle")

    csum = np.concatenate(([0.0], np.cumsum(x**2)))
    starts = np.arange(0, x.size - n + 1, step)
    values = np.sqrt((csum[starts + n] - csum[starts]) / n)
    return values, starts / fs