# Contributing to GridLens

## Setup

Windows PowerShell:

```powershell
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
python -m pip install -e ".[dev]"
ruff check .
pytest
```

Linux:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
ruff check .
pytest
```

## Add a loader

Implement a loader in `gridlens/loaders/`, export it from
`gridlens/loaders/__init__.py`, and add dispatcher support in `load()`.
Keep public `Waveform` inputs and outputs consistent.

## Add a metric

Add the implementation under `gridlens/metrics/`, export it from the package
initializer, and cover normal and edge cases in `tests/`.

## Add a standard

Put limit tables in `gridlens/standards/` with a named source string and
verification comments. Export checks and registry entries from
`gridlens/standards/__init__.py`. Never guess a limit; leave uncertain values
as `None` with a TODO.

## Pull request checklist

- [ ] Tests are deterministic and pass
- [ ] `ruff check .` passes
- [ ] Public functions have type hints and NumPy-style docstrings
- [ ] Standard values cite edition/table/clause metadata
- [ ] Documentation and examples are updated

To propose a new standard, open a feature issue containing jurisdiction,
official documents, applicability, averaging periods, and source clauses.