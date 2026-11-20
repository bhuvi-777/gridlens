# GridLens Architecture

The data flow is:

`loaders -> Waveform -> metrics/events/intervals -> standards -> reports/CLI`

- Loaders convert vendor-neutral source files into `gridlens.Waveform`.
- Metrics operate on sample arrays and return engineering values.
- Events detect sag, swell and interruption windows.
- Interval analysis creates standardized pandas DataFrames.
- Standards check interval and event data and return `ComplianceResult`.
- HTML reports, JSON output, and the CLI present library results.
