import numpy as np
import pandas as pd

from gridlens.reports import build_report, html_report, write_report
from gridlens.standards.base import Check, ComplianceResult
from gridlens.waveform import Waveform


def test_html_report_escape_and_write(tmp_path):
    result = ComplianceResult(
        "Test",
        [Check("Voltage", "Check", "230", "230", "V", True)],
        {},
    )
    html = build_report(result, title="<script>alert('x')</script>")
    assert "<script>" not in html
    assert "PASS" in html
    output = tmp_path / "report.html"
    write_report(output, result, intervals=None)
    assert output.read_text(encoding="utf-8").startswith("<!doctype html>")


def test_html_report_with_intervals(tmp_path):
    result = ComplianceResult(
        "Test",
        [Check("Voltage", "Check", "230", "250", "V", False)],
        {},
    )
    intervals = pd.DataFrame({
        "start": [0.0, 600.0],
        "urms": [230.0, 231.0],
        "freq": [50.0, 50.0],
        "thd": [1.0, 1.0],
        "h2": [0.1, 0.1],
    })
    html = build_report(result, intervals=intervals)
    assert "FAIL" in html


def test_waveform_figure_zooms_into_first_0_2_seconds(monkeypatch):
    t = np.arange(600_000) / 10_000
    wave = Waveform(t=t, voltage=np.sin(2 * np.pi * 50 * t))
    captured = {}

    def capture_figure(figure):
        captured["time"] = figure.axes[0].lines[0].get_xdata()
        captured["xlabel"] = figure.axes[0].get_xlabel()
        html_report.plt.close(figure)
        return ""

    monkeypatch.setattr(html_report, "_figure_png", capture_figure)

    html_report._wave_figure(wave)

    assert captured["time"][0] == 0
    assert captured["time"][-1] <= 0.2
    assert captured["time"][-1] > 0.19
    assert captured["xlabel"] == "Time (s), first 0.2 s"
