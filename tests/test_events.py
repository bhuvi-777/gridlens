import pytest

from gridlens.events import detect_events
from gridlens.generator import apply_event, sine_wave
from gridlens.metrics import rms_half_cycle

FS = 10_000


def make(factor):
    t, v = sine_wave(rms=230.0, fs=FS, duration=1.0)
    return apply_event(t, v, start=0.30, duration=0.10, factor=factor)


def test_rms_half_cycle_of_pure_sine():
    _, v = sine_wave(rms=230.0, fs=FS, duration=0.2)
    values, times = rms_half_cycle(v, fs=FS, f0=50)
    assert len(values) == 19
    assert values == pytest.approx(230.0, rel=1e-9)
    assert times[1] == pytest.approx(0.01)


def test_clean_signal_has_no_events():
    _, v = sine_wave(rms=230.0, fs=FS, duration=1.0)
    assert detect_events(v, fs=FS) == []


def test_mild_dip_is_not_a_sag():
    assert detect_events(make(0.95), fs=FS) == []


def test_detects_sag():
    events = detect_events(make(0.5), fs=FS)
    assert len(events) == 1
    ev = events[0]
    assert ev.kind == "sag"
    assert ev.start == pytest.approx(0.30, abs=0.02)
    assert ev.duration == pytest.approx(0.10, abs=0.02)
    assert ev.extreme == pytest.approx(115.0, rel=1e-6)
    assert ev.extreme_pct == pytest.approx(50.0, rel=1e-6)


def test_detects_swell():
    events = detect_events(make(1.2), fs=FS)
    assert len(events) == 1
    assert events[0].kind == "swell"
    assert events[0].extreme == pytest.approx(276.0, rel=1e-6)


def test_detects_interruption():
    events = detect_events(make(0.0), fs=FS)
    assert len(events) == 1
    assert events[0].kind == "interruption"
    assert events[0].extreme == pytest.approx(0.0, abs=1e-6)