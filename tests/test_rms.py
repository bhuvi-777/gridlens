import numpy as np
import pytest

from gridlens.generator import sine_wave
from gridlens.metrics import rms


def test_rms_of_pure_sine():
    _, v = sine_wave(rms=230.0)
    assert rms(v) == pytest.approx(230.0, rel=1e-6)


def test_rms_of_dc():
    assert rms(np.full(100, 5.0)) == pytest.approx(5.0)


def test_rms_with_harmonic():
    # Total RMS = sqrt(V1^2 + V5^2) = 230 * sqrt(1 + 0.1^2)
    _, v = sine_wave(rms=230.0, harmonics={5: 0.1})
    expected = 230.0 * np.sqrt(1 + 0.1**2)
    assert rms(v) == pytest.approx(expected, rel=1e-6)