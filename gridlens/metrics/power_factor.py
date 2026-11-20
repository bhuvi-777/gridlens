"""Power and power factor from sampled voltage and current."""
import numpy as np

from .rms import rms


def _prepare(voltage, current):
    v = np.asarray(voltage, dtype=float)
    i = np.asarray(current, dtype=float)
    if v.shape != i.shape:
        raise ValueError("voltage and current must have the same length")
    return v, i


def active_power(voltage, current):
    """Active (real) power P = mean(v * i), in watts.

    Use a whole number of cycles for an exact result.
    """
    v, i = _prepare(voltage, current)
    return float(np.mean(v * i))


def apparent_power(voltage, current):
    """Apparent power S = Vrms * Irms, in volt-amperes."""
    v, i = _prepare(voltage, current)
    return rms(v) * rms(i)


def reactive_power(voltage, current):
    """Non-active power Q = sqrt(S^2 - P^2), in var.

    With distorted waveforms this also includes distortion power.
    """
    p = active_power(voltage, current)
    s = apparent_power(voltage, current)
    return float(np.sqrt(max(s**2 - p**2, 0.0)))


def power_factor(voltage, current):
    """True power factor PF = P / S (between -1 and 1)."""
    s = apparent_power(voltage, current)
    if s == 0:
        raise ValueError("Apparent power is zero, so power factor is undefined")
    return active_power(voltage, current) / s