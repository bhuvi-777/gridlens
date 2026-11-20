"""Detection of voltage sags, swells and interruptions."""
from dataclasses import dataclass

from ..metrics.rms import rms_half_cycle


@dataclass
class VoltageEvent:
    """One detected event. Time resolution is half a cycle."""

    kind: str          # "sag", "swell" or "interruption"
    start: float       # start time in seconds
    duration: float    # duration in seconds
    extreme: float     # lowest (sag/interruption) or highest (swell) RMS, in volts
    extreme_pct: float  # the same value as a percentage of nominal


def _find_runs(urms, below, threshold, hysteresis):
    """Return (start, stop) index pairs where urms crosses the threshold."""
    runs = []
    start = None
    for k, u in enumerate(urms):
        if start is None:
            if (u < threshold) if below else (u > threshold):
                start = k
        else:
            if below:
                released = u >= threshold + hysteresis
            else:
                released = u <= threshold - hysteresis
            if released:
                runs.append((start, k))
                start = None
    if start is not None:
        runs.append((start, len(urms)))
    return runs


def detect_events(voltage, fs, nominal=230.0, f0=50.0, sag=0.90, swell=1.10,
                  interruption=0.05, hysteresis=0.02):
    """Find sags, swells and interruptions in a voltage waveform.

    Thresholds are fractions of the nominal RMS voltage. Events are
    returned in time order.
    """
    if nominal <= 0:
        raise ValueError("nominal must be positive")

    urms, times = rms_half_cycle(voltage, fs, f0)
    half_period = 0.5 / f0
    hyst = hysteresis * nominal
    events = []

    for a, b in _find_runs(urms, True, sag * nominal, hyst):
        low = float(urms[a:b].min())
        kind = "interruption" if low < interruption * nominal else "sag"
        events.append(VoltageEvent(kind, float(times[a]), (b - a) * half_period,
                                   low, 100 * low / nominal))

    for a, b in _find_runs(urms, False, swell * nominal, hyst):
        high = float(urms[a:b].max())
        events.append(VoltageEvent("swell", float(times[a]), (b - a) * half_period,
                                   high, 100 * high / nominal))

    events.sort(key=lambda e: e.start)
    return events