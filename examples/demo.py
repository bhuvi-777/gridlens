from gridlens.events import detect_events
from gridlens.generator import apply_event, sine_wave

t, v = sine_wave(rms=230, fs=10_000, duration=1.0)
v = apply_event(t, v, start=0.30, duration=0.10, factor=0.5)   # 50 % sag

for ev in detect_events(v, fs=10_000):
    print(f"{ev.kind}: starts {ev.start:.2f} s, lasts {ev.duration:.2f} s, "
          f"down to {ev.extreme:.0f} V ({ev.extreme_pct:.0f} %)")