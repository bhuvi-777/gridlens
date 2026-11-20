# Good First Issue Drafts

## 1. Add Indian harmonic limits
Description: Research and encode official CEA limit tables.
Acceptance: Limit table has source metadata and unit tests; uncertain values remain TODO.
Files: `gridlens/standards/india.py`, `docs/india-standards.md`
Label: `good first issue`

## 2. Three-phase voltage unbalance
Description: Add positive/negative sequence voltage unbalance metrics.
Acceptance: Deterministic synthetic tests cover balanced and unbalanced cases.
Files: `gridlens/metrics/`, `gridlens/metrics/__init__.py`
Label: `good first issue`

## 3. Fortescue symmetrical components
Description: Implement a sequence-component helper for three-phase arrays.
Acceptance: ABC and positive/negative/zero values are tested.
Files: `gridlens/metrics/`
Label: `good first issue`

## 4. Flicker Pst/Plt
Description: Add a validated flicker analysis extension point.
Acceptance: Uses documented test data or deterministic synthetic input.
Files: `gridlens/metrics/`, `docs/`
Label: `good first issue`

## 5. IEEE 519 current TDD
Description: Implement optional current distortion/TDD checks.
Acceptance: Bus/load basis and all sources are documented.
Files: `gridlens/standards/ieee519.py`
Label: `good first issue`

## 6. PQDIF loader
Description: Add an optional PQDIF loader.
Acceptance: Reads small fixtures and returns `Waveform`.
Files: `gridlens/loaders/`
Label: `good first issue`

## 7. WAV loader
Description: Support PCM WAV waveform imports.
Acceptance: Stereo/multi-channel tests and clear errors.
Files: `gridlens/loaders/`
Label: `good first issue`

## 8. LTspice loader
Description: Parse LTspice `.raw` or `.txt` exports.
Acceptance: Time/voltage columns map to `Waveform`.
Files: `gridlens/loaders/`
Label: `good first issue`

## 9. PDF export
Description: Convert HTML reports to optional PDF output.
Acceptance: HTML remains the default and no required dependency is added.
Files: `gridlens/reports/`, `pyproject.toml`
Label: `good first issue`

## 10. Streamlit web UI
Description: Create an optional upload/analyze UI.
Acceptance: Uses library APIs and documents an optional extra.
Files: `examples/`, `pyproject.toml`
Label: `good first issue`
