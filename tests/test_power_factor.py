import numpy as np
import pytest

from gridlens.generator import sine_wave
from gridlens.metrics import (
    active_power,
    apparent_power,
    power_factor,
    reactive_power,
)


def test_unity_power_factor():
    _, v = sine_wave(rms=230.0)
    _, i = sine_wave(rms=10.0)
    assert power_factor(v, i) == pytest.approx(1.0, rel=1e-9)
    assert active_power(v, i) == pytest.approx(2300.0, rel=1e-9)


def test_lagging_30_degrees():
    _, v = sine_wave(rms=230.0)
    _, i = sine_wave(rms=10.0, phase=-np.pi / 6)
    assert active_power(v, i) == pytest.approx(2300 * np.cos(np.pi / 6), rel=1e-6)
    assert apparent_power(v, i) == pytest.approx(2300.0, rel=1e-6)
    assert reactive_power(v, i) == pytest.approx(2300 * np.sin(np.pi / 6), rel=1e-6)
    assert power_factor(v, i) == pytest.approx(np.cos(np.pi / 6), rel=1e-6)


def test_quadrature_gives_zero_power_factor():
    _, v = sine_wave(rms=230.0)
    _, i = sine_wave(rms=10.0, phase=-np.pi / 2)
    assert power_factor(v, i) == pytest.approx(0.0, abs=1e-9)


def test_harmonic_current_lowers_power_factor():
    # Pure voltage, current with a 5th harmonic at 10 %:
    # P is unchanged but Irms grows by sqrt(1.01), so PF = 1 / sqrt(1.01).
    _, v = sine_wave(rms=230.0)
    _, i = sine_wave(rms=10.0, harmonics={5: 0.1})
    assert power_factor(v, i) == pytest.approx(1 / np.sqrt(1.01), rel=1e-6)


def test_length_mismatch_raises():
    with pytest.raises(ValueError):
        power_factor([1.0, 2.0, 3.0], [1.0, 2.0])