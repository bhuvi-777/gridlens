"""Demonstrate voltage event detection."""

from gridlens.events import detect_events
from gridlens.generator import apply_event, sine_wave

t, voltage = sine_wave(rms=230, fs=10_000, duration=1.0)
voltage = apply_event(t, voltage, start=0.25, duration=0.1, factor=0.5)

for event in detect_events(voltage, fs=10_000):
    print(event.kind, event.start, event.duration)
