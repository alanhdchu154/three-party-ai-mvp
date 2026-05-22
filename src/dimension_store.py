"""File-based storage for cumulative strain dimension score snapshots."""

from __future__ import annotations

import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any

DIMENSION_DIR = Path(__file__).resolve().parent.parent / "data" / "dimension_scores"
SNAPSHOT_DIR_NAME = "snapshots"


def _safe_id(student_id: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_\-]", "_", student_id.strip())
    if not cleaned:
        raise ValueError("student_id cannot be empty")
    return cleaned


def latest_path(student_id: str) -> Path:
    DIMENSION_DIR.mkdir(parents=True, exist_ok=True)
    return DIMENSION_DIR / f"{_safe_id(student_id)}.json"


def snapshot_dir(student_id: str) -> Path:
    path = DIMENSION_DIR / SNAPSHOT_DIR_NAME / _safe_id(student_id)
    path.mkdir(parents=True, exist_ok=True)
    return path


def load_latest(student_id: str | None) -> dict[str, Any] | None:
    if not student_id:
        return None
    for candidate in _candidate_ids(student_id):
        path = latest_path(candidate)
        if path.exists():
            return _read_json(path)
    return None


def load_snapshots(student_id: str | None, *, limit: int | None = None) -> list[dict[str, Any]]:
    if not student_id:
        return []
    snapshots: list[dict[str, Any]] = []
    for candidate in _candidate_ids(student_id):
        path = DIMENSION_DIR / SNAPSHOT_DIR_NAME / _safe_id(candidate)
        if not path.exists():
            continue
        for item in sorted(path.glob("*.json")):
            payload = _read_json(item)
            if payload is not None:
                snapshots.append(payload)
    snapshots.sort(key=lambda item: str(item.get("scored_at") or item.get("created_at") or ""))
    if limit is not None:
        return snapshots[-limit:]
    return snapshots


def save_snapshot(
    student_id: str,
    scores: dict[str, Any],
    *,
    scored_at: str | None = None,
    source_type: str | None = None,
) -> Path:
    """Persist latest score and append an immutable timestamped snapshot."""
    safe_id = _safe_id(student_id)
    timestamp = scored_at or datetime.utcnow().isoformat() + "Z"
    payload = {
        **scores,
        "student_id": safe_id,
        "scored_at": timestamp,
    }
    if source_type:
        payload["source_type"] = source_type

    latest = latest_path(safe_id)
    _atomic_write_json(latest, payload)

    snapshot_name = re.sub(r"[^A-Za-z0-9_\-]", "_", timestamp)
    snapshot = snapshot_dir(safe_id) / f"{snapshot_name}.json"
    _atomic_write_json(snapshot, payload)
    return snapshot


def _candidate_ids(student_id: str) -> list[str]:
    candidates = [student_id]
    if student_id.startswith("saga_a_"):
        candidates.append(student_id.removeprefix("saga_a_"))
    return candidates


def _read_json(path: Path) -> dict[str, Any] | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def _atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(tmp, path)

