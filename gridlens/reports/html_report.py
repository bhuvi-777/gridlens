"""Self-contained HTML report generation."""
from __future__ import annotations

import base64
from html import escape
from io import BytesIO
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from ..standards.base import ComplianceResult
from ..waveform import Waveform


def _figure_png(figure) -> str:
    buffer = BytesIO()
    figure.savefig(buffer, format="png", bbox_inches="tight")
    plt.close(figure)
    buffer.seek(0)
    return base64.b64encode(buffer.read()).decode("ascii")


def _wave_figure(wave: Waveform) -> str:
    figure, axis = plt.subplots(figsize=(8, 3))
    window_end = wave.t[0] + 0.2 if wave.t.size else 0.0
    window_stop = (
        int(np.searchsorted(wave.t, window_end, side="right"))
        if wave.t.size
        else 0
    )
    time = wave.t[:window_stop]
    voltage = wave.voltage[:window_stop]
    step = max(1, len(time) // 20_000)
    axis.plot(time[::step], voltage[::step], label="Voltage")
    axis.set_xlabel(
        "Time (s), first 0.2 s"
        if wave.t.size and wave.t[-1] - wave.t[0] > 0.2
        else "Time (s)"
    )
    axis.set_ylabel("Voltage (V)")
    axis.grid(True, alpha=0.3)
    return _figure_png(figure)


def _rms_figure(intervals: pd.DataFrame) -> str:
    figure, axis = plt.subplots(figsize=(8, 3))
    axis.plot(intervals["start"], intervals["urms"], marker=".", linewidth=1)
    axis.axhspan(207, 253, color="green", alpha=0.15)
    axis.set_xlabel("Time (s)")
    axis.set_ylabel("RMS voltage (V)")
    axis.grid(True, alpha=0.3)
    return _figure_png(figure)


def _harmonic_figure(intervals: pd.DataFrame) -> str:
    columns = [column for column in intervals if column.startswith("h")]
    orders = [int(column[1:]) for column in columns]
    values = intervals[columns].mean().to_numpy(dtype=float) if columns else np.array([])
    figure, axis = plt.subplots(figsize=(8, 3))
    if columns:
        axis.bar(orders, values)
    axis.set_xlabel("Harmonic order")
    axis.set_ylabel("Magnitude (%)")
    axis.grid(True, alpha=0.3)
    return _figure_png(figure)


def build_report(
    result: ComplianceResult,
    wave: Waveform | None = None,
    events: list | None = None,
    intervals: pd.DataFrame | None = None,
    title: str = "GridLens power quality report",
) -> str:
    """Build a self-contained HTML report."""
    safe_title = escape(title)
    marker = "PASS" if result.passed else "FAIL"
    marker_class = "pass" if result.passed else "fail"
    check_rows = []
    for check in result.checks:
        status = "PASS" if check.passed else "FAIL"
        status_class = "pass" if check.passed else "fail"
        check_rows.append(
            "<tr>"
            f"<td>{escape(check.name)}</td><td>{escape(check.description)}</td>"
            f"<td>{escape(str(check.limit))}</td><td>{escape(str(check.measured))}</td>"
            f"<td>{escape(check.unit)}</td>"
            f"<td class=\"{status_class}\">{status}</td>"
            f"<td>{escape(check.note)}</td></tr>"
        )
    event_rows = []
    for event in events or []:
        event_rows.append(
            "<tr>"
            f"<td>{escape(str(getattr(event, 'kind', '')))}</td>"
            f"<td>{escape(str(getattr(event, 'start', '')))}</td>"
            f"<td>{escape(str(getattr(event, 'duration', '')))}</td>"
            f"<td>{escape(str(getattr(event, 'extreme_pct', '')))}%</td></tr>"
        )
    figures = []
    if wave is not None:
        figures.append(("Voltage waveform", _wave_figure(wave)))
    if intervals is not None:
        if {"start", "urms"} <= set(intervals.columns):
            figures.append(("RMS trend", _rms_figure(intervals)))
        figures.append(("Harmonics", _harmonic_figure(intervals)))
    figure_html = "".join(
        f'<section><h2>{escape(label)}</h2><img alt="{escape(label)}" '
        f'src="data:image/png;base64,{data}"></section>'
        for label, data in figures
    )
    event_body = "".join(event_rows) or '<tr><td colspan="4">No events</td></tr>'
    event_section = (
        "<h2>Events</h2><table><thead><tr><th>Kind</th><th>Start (s)</th>"
        "<th>Duration (s)</th><th>Extreme</th></tr></thead>"
        f"<tbody>{event_body}"
        "</tbody></table>"
    )
    return f"""<!doctype html>
<html><head><meta charset="utf-8"><title>{safe_title}</title>
<style>
:root {{ color-scheme:light dark; --bg:#fff; --text:#222; --border:#ccc; }}
@media (prefers-color-scheme:dark) {{ :root {{ --bg:#171717; --text:#eee; --border:#555; }} }}
body {{ background:var(--bg); color:var(--text); font-family:Arial,sans-serif; margin:2rem; }}
table {{ border-collapse:collapse; width:100%; margin-bottom:1rem; }}
th,td {{ border:1px solid var(--border); padding:.5rem; text-align:left; }}
.pass {{ color:#16833a; font-weight:bold; }} .fail {{ color:#c62828; font-weight:bold; }}
img {{ max-width:100%; height:auto; }} .summary {{ font-size:1.5rem; }}
</style></head><body>
<h1>{safe_title}</h1><p class="summary {marker_class}">{marker}</p>
<h2>Compliance checks</h2>
<table><thead><tr><th>Name</th><th>Description</th><th>Limit</th>
<th>Measured</th><th>Unit</th><th>Status</th><th>Note</th></tr></thead>
<tbody>{''.join(check_rows)}</tbody></table>
{event_section}{figure_html}</body></html>"""


def write_report(path: str | Path, *args, **kwargs) -> str:
    """Build and write a report; return the HTML string."""
    html = build_report(*args, **kwargs)
    Path(path).write_text(html, encoding="utf-8")
    return html
