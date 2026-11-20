# GridLens

![tests](https://github.com/bhuvi-777/gridlens/actions/workflows/tests.yml/badge.svg)

**Vendor-neutral power quality analysis for Python.**
Load voltage and current waveforms, compute metrics, and (soon) check them
against standards like EN 50160 and IEEE 519, including Indian grid codes.

> Status: early development. The core metrics work; standards checks and
> reports are next. Contributions are welcome.

## Why

Power quality software is mostly tied to one instrument brand, and general
tools like MATLAB need you to rebuild the same loaders, limits and reports
every time. GridLens aims to be a free, scriptable layer that works on data
from any source.

## Install

```bash
git clone https://github.com/bhuvi-777/gridlens.git
cd gridlens
pip install -e ".[dev]"
pytest
```

## Quick example

```python
from gridlens.generator import sine_wave
from gridlens.metrics import power_factor, rms, thd

t, v = sine_wave(rms=230, harmonics={5: 0.08})   # 230 V with 8 % 5th harmonic
_, i = sine_wave(rms=10, phase=-0.5)             # 10 A, lagging

print(f"Voltage RMS:  {rms(v):.1f} V")
print(f"Voltage THD:  {thd(v, fs=10_000):.2%}")
print(f"Power factor: {power_factor(v, i):.3f}")
```

Load your own data:

```python
from gridlens.loaders import load_csv

wave = load_csv("capture.csv", voltage_col="v", current_col="i", fs=10_000)
```

## Roadmap

- [x] Synthetic waveform generator
- [x] RMS, THD, active/reactive/apparent power, power factor
- [x] CSV loader
- [x] Sag, swell and interruption detection
- [x] EN 50160 and IEEE 519 voltage compliance checks
- [ ] Indian grid code limits
- [x] COMTRADE loading (optional `comtrade`)
- [x] HTML compliance reports
- [x] Command-line tool
- [ ] PDF report and web UI

## Analyze a file

```powershell
gridlens analyze capture.csv --standard en50160 --nominal 230 --freq 50
gridlens analyze capture.csv --standard ieee519 --bus-kv 11 --report report.html
gridlens generate demo.csv --duration 60 --rms 230 --harmonic 5=0.06
```

Generate a demo CSV, then analyze it. Use `python -m gridlens --help` if the
console script is not on `PATH`.

## Standards supported

| Standard | Status |
| --- | --- |
| EN 50160 | Implemented for LV voltage, frequency, THD and harmonics |
| IEEE 519-2014/2022 | Voltage distortion implemented; current TDD planned |
| India CEA/grid code | Planned; limits are not implemented |

> Engineering guidance only. Compliance claims must be verified against the
> official standard text and edition, applicable system scope, and certified instruments.

## Contributing

Issues and pull requests are welcome. Run `ruff check .` and `pytest`
before opening a PR.

## License

MIT