import pandas as pd

from gridlens.reports import build_report, write_report
from gridlens.standards.base import Check, ComplianceResult


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
