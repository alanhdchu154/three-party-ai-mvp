"""Backfill source_type metadata on existing JSON artifacts.

This does not generate new conversations. It only annotates existing files.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src import source_types

ROOT = Path(__file__).resolve().parent.parent


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="Write changes instead of dry-run")
    args = parser.parse_args()

    targets = [
        (ROOT / "data" / "generated_conversations", "llm_generated"),
        (ROOT / "data" / "analysis_reports", "synthetic"),
        (ROOT / "data" / "dimension_scores", "synthetic"),
    ]
    changed: list[Path] = []
    for folder, default_source in targets:
        if not folder.exists():
            continue
        for path in sorted(folder.glob("*.json")):
            payload = _read_json(path)
            if payload is None:
                continue
            normalized = _attach_source_type(payload, default_source)
            if normalized != payload:
                changed.append(path)
                if args.write:
                    path.write_text(json.dumps(normalized, ensure_ascii=False, indent=2), encoding="utf-8")

    mode = "updated" if args.write else "would update"
    print(f"{mode} {len(changed)} files")
    for path in changed:
        print(f"- {path}")


def _attach_source_type(payload: Any, default_source: str) -> Any:
    if isinstance(payload, dict):
        updated = dict(payload)
        updated["source_type"] = source_types.normalize_source_type(updated.get("source_type") or default_source)
        if "conversations" in updated and isinstance(updated["conversations"], list):
            updated["conversations"] = [
                _attach_source_type(item, default_source)
                for item in updated["conversations"]
            ]
        return updated
    return payload


def _read_json(path: Path) -> Any | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


if __name__ == "__main__":
    main()

