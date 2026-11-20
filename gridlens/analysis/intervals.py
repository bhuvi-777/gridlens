"""Interval-based power-quality analysis."""
from __future__ import annotations

import numpy as np
import pandas as pd

from ..waveform import Waveform


def _window_frequency(t: np.ndarray, voltage: np.ndarray, f0: float) -> float:
    """Estimate frequency using rising-edge zero crossings."""
    indices = np.flatnonzero((voltage[:-1] < 0.0) & (voltage[1:] >= 0.0))
    if indices.size < 2:
        return f0
    cross = t[indices] - voltage[indices] * (
        t[indices + 1] - t[indices]
    ) / (voltage[indices + 1] - voltage[indices])
    return float((cross.size - 1) / (cross[-1] - cross[0]))


def compute_intervals(
    wave: Waveform,
    interval_s: float = 600.0,
    f0: float = 50.0,
    max_harmonic: int = 40,
) -> pd.DataFrame:
    """Compute 10-cycle or 12-cycle window metrics and interval aggregates.

    Harmonic magnitudes use the FFT bin nearest to ``order * f0`` Hz.
    Each interval reports the mean of the window harmonic values and THD.
    """
    if interval_s <= 0:
        raise ValueError("interval_s must be positive")
    if f0 not in (50.0, 60.0):
        raise ValueError("f0 must be 50 or 60 Hz")
    fs = wave.fs
    cycles = 12 if f0 == 60.0 else 10
    samples_per_cycle = fs / f0
    if not np.isclose(samples_per_cycle, round(samples_per_cycle), rtol=0.0, atol=1e-9):
        raise ValueError(
            "Sampling rate does not provide an integer number of samples per cycle; "
            "call gridlens.waveform.resample() first"
        )

    window_size = cycles * round(samples_per_cycle)
    windows = [
        (start, start + window_size)
        for start in range(0, len(wave.voltage) - window_size + 1, window_size)
    ]
    rows: list[dict[str, float]] = []
    for start, stop in windows:
        segment = np.asarray(wave.voltage[start:stop], dtype=float)
        segment_t = np.asarray(wave.t[start:stop], dtype=float)
        urms = float(np.sqrt(np.mean(segment**2)))
        freq = _window_frequency(segment_t, segment, f0)
        spectrum = np.abs(np.fft.rfft(segment))
        df = fs / segment.size
        fundamental = spectrum[round(f0 / df)]
        if fundamental == 0:
            harmonic_values = {f"h{order}": 0.0 for order in range(2, max_harmonic + 1)}
            thd = 0.0
        else:
            harmonic_values = {}
            harmonic_sum = 0.0
            for order in range(2, max_harmonic + 1):
                magnitude = spectrum[round(order * f0 / df)]
                percent = 100.0 * magnitude / fundamental
                harmonic_values[f"h{order}"] = percent
                harmonic_sum += percent**2
            thd = float(np.sqrt(harmonic_sum))
        window_start = float(wave.t[start])
        rows.append({
            "start": window_start,
            "urms": urms,
            "freq": freq,
            "thd": thd,
            **harmonic_values,
        })

    if not rows:
        return pd.DataFrame(
            {"start": [], "urms": [], "freq": [], "thd": [],
             **{f"h{order}": [] for order in range(2, max_harmonic + 1)}}
        )

    frame = pd.DataFrame(rows)
    interval_starts = np.floor(frame["start"] / interval_s) * interval_s
    frame["interval"] = interval_starts
    aggregate_columns = ["urms", "freq", "thd"] + [
        f"h{order}" for order in range(2, max_harmonic + 1)
    ]
    result = frame.groupby("interval", sort=True)[aggregate_columns].mean().reset_index()
    result = result.rename(columns={"interval": "start"})
    return result
