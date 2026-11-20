"""Common waveform container used across GridLens."""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.signal import resample_poly


@dataclass
class Waveform:
    """Sampled voltage (and optionally current) with a time axis in seconds."""

    t: np.ndarray
    voltage: np.ndarray
    current: np.ndarray | None = None

    @property
    def fs(self) -> float:
        """Sampling rate in Hz, estimated from the time axis."""
        if self.t.size < 2:
            raise ValueError("Need at least two samples to find the sampling rate")
        return float(1.0 / np.median(np.diff(self.t)))


def resample(wave: Waveform, fs_new: float) -> Waveform:
    """Resample a waveform to a new sampling rate.

    Parameters
    ----------
    wave : Waveform
        Waveform to resample.
    fs_new : float
        Desired sampling rate in Hz.
    """
    if fs_new <= 0:
        raise ValueError("fs_new must be positive")
    fs_old = wave.fs
    duration = wave.t[-1] - wave.t[0] if wave.t.size > 1 else 0.0
    from fractions import Fraction

    ratio = Fraction(fs_new / fs_old).limit_denominator(1000)
    up = ratio.numerator
    down = ratio.denominator
    t = np.arange(round(duration * fs_new) + 1) / fs_new
    t = t[t <= duration]
    voltage = resample_poly(wave.voltage, up, down)
    voltage = voltage[: t.size]
    current = None
    if wave.current is not None:
        current = resample_poly(wave.current, up, down)[: t.size]
    return Waveform(t=t, voltage=voltage, current=current)