import numpy as np

from gridlens.analysis import compute_intervals
from gridlens.generator import sine_wave
from gridlens.waveform import Waveform


def test_clean_intervals():
    t, v = sine_wave(freq=50, rms=230, fs=10_000, duration=60)
    result = compute_intervals(Waveform(t, v), interval_s=60)
    assert abs(result.iloc[0]["urms"] - 230) < 0.1
    assert abs(result.iloc[0]["freq"] - 50) < 0.01
    assert result.iloc[0]["thd"] < 0.1


def test_fifth_harmonic_intervals():
    t, v = sine_wave(freq=50, rms=230, fs=10_000, duration=60,
                     harmonics={5: 0.06})
    result = compute_intervals(Waveform(t, v), interval_s=1)
    assert abs(result.iloc[0]["h5"] - 6) < 0.2
    assert abs(result.iloc[0]["thd"] - 6) < 0.2


def test_resampling_is_required_for_fractional_samples():
    t = np.arange(500) / 7_513
    v = np.sin(2 * np.pi * 50 * t)
    try:
        compute_intervals(Waveform(t, v))
    except ValueError as exc:
        assert "resample()" in str(exc)
    else:
        raise AssertionError("Expected ValueError")
