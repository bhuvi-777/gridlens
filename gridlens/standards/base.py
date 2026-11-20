"""Shared compliance result types."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pandas as pd


@dataclass
class Check:
    """One pass/fail condition in a compliance assessment."""

    name: str
    description: str
    limit: Any
    measured: Any
    unit: str
    passed: bool
    note: str = ""


@dataclass
class ComplianceResult:
    """Results for a power-quality standard check."""

    standard: str
    checks: list[Check]
    events: dict[str, int]

    @property
    def passed(self) -> bool:
        """Whether every pass/fail check passed."""
        return all(check.passed for check in self.checks)

    def summary(self) -> str:
        """Return a readable multi-line summary."""
        status = "PASS" if self.passed else "FAIL"
        lines = [f"{self.standard}: {status}"]
        for check in self.checks:
            check_status = "PASS" if check.passed else "FAIL"
            lines.append(
                f"{check_status} - {check.name}: measured={check.measured} "
                f"{check.unit}, limit={check.limit}"
            )
            if check.note:
                lines.append(f"  Note: {check.note}")
        return "\n".join(lines)

    def to_dict(self) -> dict[str, Any]:
        """Return the result as a JSON-serializable dictionary."""
        return {
            "standard": self.standard,
            "passed": self.passed,
            "checks": [
                {
                    "name": c.name,
                    "description": c.description,
                    "limit": c.limit,
                    "measured": c.measured,
                    "unit": c.unit,
                    "passed": c.passed,
                    "note": c.note,
                }
                for c in self.checks
            ],
            "events": self.events,
        }

    def to_dataframe(self) -> pd.DataFrame:
        """Return checks as a pandas DataFrame."""
        return pd.DataFrame(
            [
                {
                    "name": c.name,
                    "description": c.description,
                    "limit": c.limit,
                    "measured": c.measured,
                    "unit": c.unit,
                    "passed": c.passed,
                    "note": c.note,
                }
                for c in self.checks
            ]
        )
