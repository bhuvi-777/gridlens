"""IEEE 519 voltage distortion compliance checks."""
from __future__ import annotations

import numpy as np
import pandas as pd

from .base import Check, ComplianceResult

# IEEE 519-2014/2022 voltage distortion planning limits.
# verify against the official standard text and edition.
IEEE519_VOLTAGE_LIMITS = {
    "<=1 kV": {"individual": 5.0, "thd": 8.0},
    "1-69 kV": {"individual": 3.0, "thd": 5.0},
    "69-161 kV": {"individual": 1.5, "thd": 2.5},
    ">161 kV": {"individual": 1.0, "thd": 1.5},
}


def check_ieee519_voltage(
    intervals: pd.DataFrame,
    bus_voltage_kv: float,
) -> ComplianceResult:
    """Check 95th-percentile voltage individual harmonic and THD limits."""
    if bus_voltage_kv <= 1:
        bus_class = "<=1 kV"
    elif bus_voltage_kv <= 69:
        bus_class = "1-69 kV"
    elif bus_voltage_kv <= 161:
        bus_class = "69-161 kV"
    else:
        bus_class = ">161 kV"
    limits = IEEE519_VOLTAGE_LIMITS[bus_class]

    thd_values = intervals["thd"].to_numpy(dtype=float)
    thd_95 = float(np.percentile(thd_values, 95))
    checks = [
        Check(
            "Voltage THD",
            f"95th-percentile voltage THD for {bus_class}",
            limits["thd"],
            round(thd_95, 3),
            "%",
            thd_95 <= limits["thd"],
            "indicative only: interval assessment basis should be verified",
        )
    ]

    for order in range(2, 41):
        column = f"h{order}"
        if column not in intervals:
            continue
        value_95 = float(np.percentile(
            intervals[column].to_numpy(dtype=float), 95
        ))
        checks.append(
            Check(
                f"Individual harmonic h{order}",
                f"95th-percentile individual harmonic for {bus_class}",
                limits["individual"],
                round(value_95, 3),
                "%",
                value_95 <= limits["individual"],
                "indicative only: interval assessment basis should be verified",
            )
        )

    # TODO: Add current distortion/TDD limits for IEEE 519 when limits are
    # verified against the applicable edition and system study basis.
    return ComplianceResult("IEEE 519", checks, {})
