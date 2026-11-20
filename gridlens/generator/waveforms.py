

def apply_event(t, signal, start, duration, factor):
    """Scale a signal by `factor` between start and start + duration (seconds).

    factor < 1 makes a sag, factor > 1 a swell, factor = 0 an interruption.
    """
    out = np.array(signal, dtype=float, copy=True)
    mask = (t >= start) & (t < start + duration)
    out[mask] *= factor
    return out