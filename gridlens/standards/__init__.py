"""Power-quality standards compliance checks."""

from collections.abc import Callable
from typing import Any

from .base import Check, ComplianceResult
from .en50160 import check_en50160
from .ieee519 import check_ieee519_voltage


def get_standard(name: str) -> Callable[..., Any]:
    """Return a standards check function by registry name."""
    registry = {
        "en50160": check_en50160,
        "ieee519": check_ieee519_voltage,
    }
    try:
        return registry[name.lower()]
    except KeyError as exc:
        raise ValueError(
            f"Unknown standard '{name}'. Supported standards: en50160, ieee519"
        ) from exc


__all__ = [
    "Check",
    "ComplianceResult",
    "check_en50160",
    "check_ieee519_voltage",
    "get_standard",
]