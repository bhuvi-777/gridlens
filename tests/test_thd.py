import pytest

from gridlens.generator import sine_wave
from gridlens.metrics import thd


def test_thd_of_pure_sine_is_zero():
    _, v = sine_wave()
    assert thd(v, fs=10_000, f0=50) == pytest.approx(0.0, abs=1e-6)


def test_thd_with_single_harmonic():
    _, v = sine_wave(harmonics={5: 0.10})
    assert thd(v, fs=10_000, f0=50) == pytest.approx(0.10, abs=1e-6)


def test_thd_with_two_harmonics():
    # sqrt(0.1^2 + 0.2^2) = 0.2236...
    _, v = sine_wave(harmonics={3: 0.10, 5: 0.20})
    assert thd(v, fs=10_000, f0=50) == pytest.approx(0.2236068, abs=1e-6)