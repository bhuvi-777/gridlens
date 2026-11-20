"""Indian standards extension point."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class StandardProfile:
    """Metadata for a standards profile contributed for another jurisdiction."""

    name: str
    authority: str
    documents: tuple[str, ...]
    notes: str = ""


INDIA_PROFILE = StandardProfile(
    name="India",
    authority="Contributing jurisdiction",
    documents=(
        "CEA Grid Standards",
        "Electricity Rules",
        "Indian Electricity Grid Code",
    ),
    notes="No limit values are implemented yet.",
)


def check_india(*args: Any, **kwargs: Any) -> Any:
    """Raise a clear error until Indian limits are contributed."""
    raise NotImplementedError(
        "Indian standards checks are not implemented yet. "
        "See docs/india-standards.md for implementation guidance."
    )
