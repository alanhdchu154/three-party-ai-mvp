"""Backfill immutable snapshots for existing dimension score JSON files."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src import dimension_store

ROOT = Path(__file__).resolve().parent.parent


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="Write snapshots instead of dry-run")
    args = parser.parse_args()

    folder = ROOT / "data" / "dimension_scores"
    written: list[Path] = []
    for path in sorted(folder.glob("*.json")):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        scored_at = payload.get("scored_at") or payload.get("evaluated_at")
        if args.write:
            snapshot = dimension_store.save_snapshot(
                path.stem,
                payload,
                scored_at=scored_at,
                source_type=payload.get("source_type", "synthetic"),
            )
            written.append(snapshot)
        else:
            written.append(dimension_store.snapshot_dir(path.stem) / "<timestamp>.json")

    mode = "wrote" if args.write else "would write"
    print(f"{mode} {len(written)} snapshots")
    for path in written:
        print(f"- {path}")


if __name__ == "__main__":
    main()

