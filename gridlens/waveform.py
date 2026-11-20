"""Common waveform container used across GridLens."""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np


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