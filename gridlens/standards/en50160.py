"""EN 50160 low-voltage supply compliance checks."""
from __future__ import annotations

from collections.abc import Iterable

import numpy as np
import pandas as pd

from .base import Check, ComplianceResult

# EN 50160 voltage harmonic limits (%). Values require verification against
# the official standard text and edition used by the operator.
EN50160_HARMONIC_LIMITS: dict[int, float | None] = {
    2: 2.0, 3: 5.0, 4: 1.0, 5: 6.0, 6: 1.0, 7: 5.0,
    8: 1.0, 9: 1.5, 10: 1.0, 11: 3.5, 12: 1.0, 13: 3.0,
    14: 1.0, 15: 0.5, 16: 1.0, 17: 2.0, 18: 1.0, 19: 1.5,
    20: 1.0, 21: 0.5, 22: 1.0, 23: 1.5, 24: 1.0, 25: 1.5,
    **{order: None for order in range(26, 41)},
}
EN50160_HARMONIC_LIMIT_SOURCE = "EN 50160; voltage characteristics table"


def _fraction_within(values: np.ndarray, low: float, high: float) -> float:
    return float(np.mean((values >= low) & (values <= high)))


def _at_or_below(value: float, limit: float) -> bool:
    return value <= limit or bool(
        np.isclose(value, limit, rtol=1e-12, atol=1e-12)
    )


def _interval_duration(intervals: pd.DataFrame) -> float:
    if "interval_s" in intervals.attrs:
        return float(intervals.attrs["interval_s"])
    if "start" not in intervals or len(intervals) < 2:
        return 600.0
    diffs = np.diff(intervals["start"].to_numpy(dtype=float))
    return float(np.median(diffs)) if diffs.size else 600.0


def _recording_duration(intervals: pd.DataFrame, interval_s: float) -> float:
    if "start" not in intervals or len(intervals) == 0:
        return 0.0
    return float(len(intervals) * interval_s)


def check_en50160(
    intervals: pd.DataFrame,
    nominal: float = 230.0,
    f0: float = 50.0,
    events: Iterable | None = None,
) -> ComplianceResult:
    """Check ten-minute interval voltage, frequency, THD and harmonics."""
    interval_s = _interval_duration(intervals)
    notes: list[str] = []
    if interval_s != 600.0:
        notes.append("indicative only: interval_s is not 600 s")

    duration = _recording_duration(intervals, interval_s)
    if duration < 7 * 24 * 3600:
        notes.append(
            "indicative only: recording shorter than assessment period"
        )
    if f0 == 50.0 and duration < 365 * 24 * 3600:
        notes.append(
            "indicative only: recording shorter than assessment period"
        )
    indicative = "; ".join(dict.fromkeys(notes))

    urms = intervals["urms"].to_numpy(dtype=float)
    fraction_10 = _fraction_within(urms, nominal * 0.90, nominal * 1.10)
    fraction_all = _fraction_within(urms, nominal * 0.85, nominal * 1.10)
    checks = [
        Check(
            "Supply voltage +/-10%",
            "95% of 10-minute intervals within +/-10% of nominal",
            "95% <= +/-10%",
            round(fraction_10 * 100, 3),
            "%",
            fraction_10 >= 0.95,
            indicative,
        ),
        Check(
            "Supply voltage +10/-15%",
            "100% of 10-minute intervals within +10%/-15% of nominal",
            "100% within +10/-15%",
            round(_fraction_within(urms, nominal * 0.85, nominal * 1.10) * 100, 3),
            "%",
            fraction_all >= 1.0,
            indicative,
        ),
    ]

    freq = intervals["freq"].to_numpy(dtype=float)
    fraction_freq_1 = _fraction_within(freq, f0 * 0.99, f0 * 1.01)
    fraction_freq_wide = _fraction_within(freq, f0 * 0.94, f0 * 1.04)
    checks.extend([
        Check(
            "Frequency +/-1%",
            "99.5% of intervals within +/-1%",
            "99.5%",
            round(fraction_freq_1 * 100, 3),
            "%",
            fraction_freq_1 >= 0.995,
            indicative,
        ),
        Check(
            "Frequency +4/-6%",
            "100% of intervals within +4/-6%",
            "100% within +4/-6%",
            round(fraction_freq_wide * 100, 3),
            "%",
            fraction_freq_wide >= 1.0,
            indicative,
        ),
    ])

    thd = intervals["thd"].to_numpy(dtype=float)
    thd_fraction = float(np.mean(thd <= 8.0))
    checks.append(
        Check(
            "Voltage THD",
            "95% of 10-minute intervals with THD at most 8%",
            "8%",
            round(float(np.percentile(thd, 95)), 3),
            "%",
            thd_fraction >= 0.95,
            indicative,
        )
    )

    for order in range(2, 41):
        column = f"h{order}"
        if column not in intervals:
            continue
        limit = EN50160_HARMONIC_LIMITS.get(order)
        if limit is None:
            continue
        percentile = float(np.percentile(
            intervals[column].to_numpy(dtype=float), 95
        ))
        passed = _at_or_below(percentile, limit)
        checks.append(
            Check(
                f"Harmonic h{order}",
                "95th percentile of individual voltage harmonic",
                limit,
                round(percentile, 3),
                "%",
                passed,
                indicative,
            )
        )

    event_list = list(events or [])
    event_counts = {
        "sag": sum(getattr(event, "kind", None) == "sag" for event in event_list),
        "swell": sum(getattr(event, "kind", None) == "swell" for event in event_list),
        "interruption": sum(
            getattr(event, "kind", None) == "interruption" for event in event_list
        ),
    }
    return ComplianceResult("EN 50160", checks, event_counts)