# GridLens Roadmap

This roadmap outlines the planned direction for **GridLens** (currently `v0.2.0`). Priorities may shift based on community feedback and contributor interest.

If you want to work on any item below, check the [Issues](https://github.com/bhuvi-777/gridlens/issues) tab first or open a new issue to discuss your approach.

---

## v0.3.0 — Standards, Loaders & Reliability

Focus: expanding real-world standards coverage and hardening data ingestion.

- [ ] **IEEE 519 current TDD and current harmonic limits**
  - Short-circuit ratio ($I_{sc}/I_L$) aware limits.
  - Support for both 2014 and 2022 editions.
  - Per-harmonic findings and aggregate TDD reporting.
- [ ] **Indian CEA / IEGC grid code compliance module**
  - Configurable regional standards with edition metadata.
  - Voltage, frequency, harmonics, and interruption criteria as applicable.
  - Clear distinction between regulatory limits and engineering guidance.
- [ ] **COMTRADE loader compatibility**
  - Detect and validate `.cfg` and ASCII/binary `.dat` variants.
  - Support multiple file encodings and timestamp formats.
  - Clear error messages for unsupported COMTRADE configurations.
- [ ] **CSV loader validation**
  - Detect missing/duplicate timestamps, inconsistent sample rates, and `NaN` values.
  - Validate voltage/current column units and surface them in metadata.
- [ ] **Structured JSON output**
  - Stable schema for metrics, events, standards checks, and report metadata.
  - CLI support for `--format json`.
- [ ] **Signal quality diagnostics**
  - Detect clipping, dropped samples, clock drift, DC offset, and implausible RMS values.
  - Emit warnings when analysis results may be unreliable.

---

## v0.4.0 — Three-Phase Analysis & Batch Workflows

Focus: multi-phase metrics, multi-file pipelines, and richer reports.

- [ ] **Three-phase unbalance and sequence components**
  - NEMA voltage unbalance and symmetrical component VUF ($V_2 / V_1$).
- [ ] **Residual and neutral-current metrics**
- [ ] **Batch and folder analysis**
  - Analyze all captures in a directory using glob patterns with continue-on-error support.
  - Generate a single aggregate HTML/JSON summary.
- [ ] **Multi-run aggregation**
  - Combine multiple recordings into 95th-percentile, 99th-percentile, and maximum summaries.
  - Track missing intervals and overlapping captures.
- [ ] **Waveform plotting and event zoom views**
  - Dedicated plots for detected sags, swells, and interruptions.
- [ ] **PDF report export (optional extra)**
  - Print-ready PDF export from the existing HTML report via `pip install "gridlens[pdf]"` to keep core installs lightweight.

---

## Future / Long-Term

Larger research-grade and ecosystem features.

- [ ] **IEC 61000-4-30 & IEC 61000-4-7 alignment** (measurement aggregation and interharmonics)
- [ ] **Flicker analysis** (IEC 61000-4-15 short-term $P_{st}$ and long-term $P_{lt}$)
- [ ] **Transient and inrush detection**
- [ ] **PQDIF loader** (IEEE 1159.3)
- [ ] **Interactive Streamlit web demo** for zero-install CSV analysis

---

## Developer Experience & Quality (Ongoing)

- [ ] **End-to-end CLI tests** using temporary real-style captures
- [ ] **Property-based tests** for RMS, THD, and power-factor calculations
- [ ] **API reference** auto-generated from docstrings
- [ ] **Benchmark recordings** with reference expected results
- [ ] **Versioned standards-limit changelog** and release notes
