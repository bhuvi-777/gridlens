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
- [ ] Sag, swell and interruption detection
- [ ] EN 50160 and IEEE 519 compliance checks
- [ ] Indian grid code limits
- [ ] COMTRADE loading (via `python-comtrade`)
- [ ] HTML/PDF compliance reports
- [ ] Command-line tool and web UI

## Contributing

Issues and pull requests are welcome. Run `ruff check .` and `pytest`
before opening a PR.

## License

MIT