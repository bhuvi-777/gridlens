"""Synthetic waveform generation for testing and teaching."""
import numpy as np


def sine_wave(freq=50.0, rms=230.0, fs=10_000.0, duration=0.2,
              harmonics=None, phase=0.0):
    """Generate a voltage waveform.

    Parameters
    ----------
    freq : fundamental frequency in Hz
    rms : RMS value of the fundamental component
    fs : sampling rate in Hz
    duration : length in seconds (use a whole number of cycles)
    harmonics : dict {order: amplitude relative to fundamental},
                e.g. {5: 0.1} adds a 5th harmonic at 10 % of the fundamental
    phase : phase of the fundamental in radians

    Returns
    -------
    t, signal : two numpy arrays
    """
    t = np.arange(round(fs * duration)) / fs
    peak = rms * np.sqrt(2)
    signal = np.sin(2 * np.pi * freq * t + phase)
    for order, ratio in (harmonics or {}).items():
        signal = signal + ratio * np.sin(2 * np.pi * order * freq * t)
    return t, peak * signal


def apply_event(t, signal, start, duration, factor):
    """Scale a signal by `factor` between start and start + duration (seconds).

    factor < 1 makes a sag, factor > 1 a swell, factor = 0 an interruption.
    """
    out = np.array(signal, dtype=float, copy=True)
    mask = (t >= start) & (t < start + duration)
    out[mask] *= factor
    return out