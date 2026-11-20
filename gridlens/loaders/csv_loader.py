"""Load waveform data from CSV files."""
import numpy as np
import pandas as pd

from ..waveform import Waveform


def load_csv(path, time_col="time", voltage_col="voltage",
             current_col=None, fs=None):
    """Read a CSV file into a Waveform.

    If the file has no time column, pass the sampling rate `fs` in Hz
    and the time axis is built for you.
    """
    df = pd.read_csv(path)

    for col in (voltage_col, current_col):
        if col is not None and col not in df.columns:
            raise KeyError(
                f"Column '{col}' not found. Available columns: {list(df.columns)}"
            )

    if time_col in df.columns:
        t = df[time_col].to_numpy(dtype=float)
    elif fs is not None:
        t = np.arange(len(df)) / fs
    else:
        raise ValueError(
            f"No '{time_col}' column in the file. Pass fs=<sampling rate in Hz>."
        )

    voltage = df[voltage_col].to_numpy(dtype=float)
    current = None if current_col is None else df[current_col].to_numpy(dtype=float)
    return Waveform(t=t, voltage=voltage, current=current)