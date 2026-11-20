"""Waveform loaders."""
from pathlib import Path

from .comtrade_loader import load_comtrade
from .csv_loader import load_csv


def load(path: str | Path, **kwargs):
    """Load a supported waveform file by extension."""
    suffix = Path(path).suffix.lower()
    if suffix == ".csv":
        return load_csv(path, **kwargs)
    if suffix in (".cfg", ".dat"):
        return load_comtrade(path, **kwargs)
    raise ValueError(
        f"Unsupported file format '{suffix or '(none)'}'. "
        "Supported formats: .csv, .cfg, .dat"
    )


__all__ = ["load", "load_comtrade", "load_csv"]