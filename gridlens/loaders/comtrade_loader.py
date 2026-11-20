"""COMTRADE loader using the optional comtrade package."""
from __future__ import annotations

from pathlib import Path

import numpy as np

from ..waveform import Waveform


def _channel_index(comtrade_file: object, channel: str | int | None, prefix: str) -> int | None:
    if channel is None:
        return None
    names = getattr(comtrade_file, "analog_channel_names", [])
    ids = getattr(comtrade_file, "analog_channel_ids", [])
    if isinstance(channel, int):
        if channel < 0 or channel >= len(names):
            raise ValueError(f"{prefix} channel index {channel} is out of range")
        return channel
    for index, value in enumerate([*names, *ids]):
        if str(value).lower() == channel.lower():
            return index if index < len(names) else index - len(names)
    raise ValueError(f"{prefix} channel '{channel}' was not found")


def load_comtrade(
    path: str | Path,
    voltage_channel: str | int | None = None,
    current_channel: str | int | None = None,
) -> Waveform:
    """Load voltage and optional current channels from COMTRADE files."""
    try:
        from comtrade import Comtrade
    except ImportError as exc:
        raise ImportError(
            'COMTRADE support requires the optional package. '
            'Install it with pip install "gridlens[comtrade]"'
        ) from exc

    path = Path(path)
    cfg = path if path.suffix.lower() == ".cfg" else path.with_suffix(".cfg")
    dat = path if path.suffix.lower() == ".dat" else path.with_suffix(".dat")
    if not cfg.exists() or not dat.exists():
        raise FileNotFoundError(f"COMTRADE cfg/dat pair not found for '{path}'")

    reader = Comtrade()
    reader.load(str(cfg), str(dat))
    names = list(getattr(reader, "analog_channel_names", []))
    voltage_index = _channel_index(reader, voltage_channel, "Voltage")
    current_index = _channel_index(reader, current_channel, "Current")
    if voltage_index is None:
        candidates = [
            index for index, name in enumerate(names)
            if "voltage" in str(name).lower() or str(name).lower().startswith("v")
        ]
        voltage_index = candidates[0] if candidates else 0
    if not names:
        raise ValueError("COMTRADE file contains no analog channels")

    scales = getattr(reader, "analog_channel_scale_factors", [1.0] * len(names))
    offsets = getattr(reader, "analog_channel_offsets", [0.0] * len(names))
    analog = getattr(reader, "analog", None)
    if analog is not None:
        raw = np.asarray(analog)
        if raw.ndim == 2:
            raw = raw.T
    else:
        raw_arrays = getattr(reader, "analog_channel_samples", None)
        if raw_arrays is None:
            raise ValueError("COMTRADE reader did not expose analog samples")
        raw = np.asarray(raw_arrays)

    def engineering(index: int) -> np.ndarray:
        values = np.asarray(raw[index], dtype=float)
        scale = float(scales[index]) if index < len(scales) else 1.0
        offset = float(offsets[index]) if index < len(offsets) else 0.0
        return values * scale + offset

    time = getattr(reader, "time", None)
    if time is None:
        fs = float(getattr(reader, "sampling_frequency", 0.0))
        if fs <= 0:
            raise ValueError("COMTRADE file did not provide a time axis or sampling frequency")
        t = np.arange(raw.shape[-1], dtype=float) / fs
    else:
        t = np.asarray(time, dtype=float)
    voltage = engineering(voltage_index)
    current = engineering(current_index) if current_index is not None else None
    return Waveform(t=t, voltage=voltage, current=current)
