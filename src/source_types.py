"""Data source labeling for demo, benchmark, and pilot safety boundaries."""

from __future__ import annotations

from typing import Any

SYNTHETIC_SOURCE_TYPES = {"handcrafted_gold", "llm_generated", "synthetic"}
PILOT_SOURCE_TYPES = {"pilot_real_anonymized"}
ALLOWED_SOURCE_TYPES = SYNTHETIC_SOURCE_TYPES | PILOT_SOURCE_TYPES
DEFAULT_SOURCE_TYPE = "synthetic"


def normalize_source_type(source_type: str | None) -> str:
    """Return a known source type, defaulting unknown values to synthetic."""
    value = (source_type or DEFAULT_SOURCE_TYPE).strip().lower()
    return value if value in ALLOWED_SOURCE_TYPES else DEFAULT_SOURCE_TYPE


def is_pilot_source(source_type: str | None) -> bool:
    return normalize_source_type(source_type) in PILOT_SOURCE_TYPES


def is_synthetic_source(source_type: str | None) -> bool:
    return normalize_source_type(source_type) in SYNTHETIC_SOURCE_TYPES


def attach_source_type(payload: dict[str, Any], source_type: str | None = None) -> dict[str, Any]:
    """Copy a payload and attach a normalized source_type."""
    return {**payload, "source_type": normalize_source_type(source_type or payload.get("source_type"))}

