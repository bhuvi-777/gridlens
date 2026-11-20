"""Generate, analyze, and report a demo waveform."""

from pathlib import Path

from gridlens.analysis import compute_intervals
from gridlens.generator import sine_wave
from gridlens.reports import write_report
from gridlens.standards import check_en50160
from gridlens.waveform import Waveform

t, voltage = sine_wave(rms=230, fs=10_000, duration=60)
wave = Waveform(t=t, voltage=voltage)
intervals = compute_intervals(wave, interval_s=60)
result = check_en50160(intervals)

output = Path(__file__).parent / "output"
output.mkdir(exist_ok=True)
write_report(output / "gridlens-report.html", result, wave=wave, intervals=intervals)
