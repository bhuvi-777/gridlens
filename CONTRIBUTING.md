# Contributing to GridLens

## Setup

Use Python 3.10 or later.

### Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
ruff check .
pytest
```

### Linux or macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
ruff check .
pytest
```

## Open a pull request

1. Fork the repository and clone your fork.
2. Create a focused branch, for example `git switch -c fix/describe-the-change`.
3. Make the change and add or update tests and documentation as needed.
4. Run `ruff check .` and `pytest` from the activated environment.
5. Push your branch and open a pull request against `main`. Describe the
   change, link the related issue, and include the exact validation commands.
6. Respond to review feedback and update your branch.

**Pull requests must pass the GitHub Actions CI checks before they can be
merged.** CI runs Ruff and pytest on Python 3.10, 3.12, and 3.13.

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
- [ ] GitHub Actions CI is green on all supported Python versions
- [ ] Public functions have type hints and NumPy-style docstrings
- [ ] Standard values cite edition/table/clause metadata
- [ ] Documentation and examples are updated

To propose a new standard, open a feature issue containing jurisdiction,
official documents, applicability, averaging periods, and source clauses.