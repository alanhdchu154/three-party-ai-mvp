"""Audit generated conversation corpus depth/type balance.

This is read-only. It checks whether Saga A is drifting into all-deep,
all-stress-test conversations instead of the intended daily-life mix.

Usage:
    python scripts/audit_conversation_quality.py
    python scripts/audit_conversation_quality.py --json
"""

from __future__ import annotations

import argparse
import json
import statistics
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent
GENERATED_DIR = PROJECT_ROOT / "data" / "generated_conversations"

TARGET_DEPTH_SHARE = {
    "shallow": 0.40,
    "medium": 0.35,
    "deep": 0.25,
}


def load_conversations() -> list[dict[str, Any]]:
    conversations: list[dict[str, Any]] = []
    for path in sorted(GENERATED_DIR.glob("*.json")):
        if path.name == "index.json":
            continue
        payload = json.loads(path.read_text(encoding="utf-8"))
        payload["_path"] = str(path.relative_to(PROJECT_ROOT))
        conversations.append(payload)
    return conversations


def audit(conversations: list[dict[str, Any]]) -> dict[str, Any]:
    depth_counts: Counter[str] = Counter()
    type_counts: Counter[str] = Counter()
    persona_counts: Counter[str] = Counter()
    persona_depths: dict[str, Counter[str]] = defaultdict(Counter)
    missing_depth: list[str] = []
    missing_type: list[str] = []
    turns: list[int] = []

    for conv in conversations:
        persona = conv.get("persona_id", "unknown")
        depth = conv.get("depth") or "<missing>"
        scenario_type = conv.get("scenario_type") or "<missing>"
        n_turns = len(conv.get("turns", []))

        persona_counts[persona] += 1
        depth_counts[depth] += 1
        type_counts[scenario_type] += 1
        persona_depths[persona][depth] += 1
        turns.append(n_turns)

        if depth == "<missing>":
            missing_depth.append(conv["_path"])
        if scenario_type == "<missing>":
            missing_type.append(conv["_path"])

    n = len(conversations)
    depth_share = {
        depth: (count / n if n else 0)
        for depth, count in depth_counts.items()
    }

    warnings: list[str] = []
    if missing_depth:
        warnings.append(f"{len(missing_depth)} conversations are missing depth.")
    if missing_type:
        warnings.append(f"{len(missing_type)} conversations are missing scenario_type.")
    if n and depth_share.get("deep", 0) > 0.45:
        warnings.append("Deep conversations exceed 45%; corpus may over-pathologize normal use.")
    if n and depth_share.get("shallow", 0) < 0.25:
        warnings.append("Shallow conversations are below 25%; add daily-life usage.")
    if type_counts and type_counts.most_common(1)[0][1] / n > 0.50:
        top_type, top_count = type_counts.most_common(1)[0]
        warnings.append(f"Scenario type `{top_type}` is {top_count}/{n}; type diversity is too low.")
    if turns and statistics.mean(turns) > 30:
        warnings.append("Average conversation length is above 30 turns; likely too many deep arcs.")

    return {
        "n_conversations": n,
        "depth_counts": dict(depth_counts),
        "depth_share": {k: round(v, 3) for k, v in sorted(depth_share.items())},
        "target_depth_share": TARGET_DEPTH_SHARE,
        "scenario_type_counts": dict(type_counts),
        "persona_counts": dict(persona_counts),
        "persona_depths": {persona: dict(counter) for persona, counter in sorted(persona_depths.items())},
        "turns": {
            "min": min(turns) if turns else 0,
            "avg": round(statistics.mean(turns), 1) if turns else 0,
            "max": max(turns) if turns else 0,
        },
        "missing_depth_examples": missing_depth[:10],
        "missing_type_examples": missing_type[:10],
        "warnings": warnings,
    }


def print_text(report: dict[str, Any]) -> None:
    print("Conversation Quality Audit")
    print("==========================")
    print(f"Conversations: {report['n_conversations']}")
    print(f"Turns: min {report['turns']['min']} / avg {report['turns']['avg']} / max {report['turns']['max']}")
    print()
    print("Depth counts:")
    for depth, count in report["depth_counts"].items():
        share = report["depth_share"].get(depth, 0)
        print(f"- {depth}: {count} ({share:.1%})")
    print()
    print("Scenario types:")
    for scenario_type, count in sorted(report["scenario_type_counts"].items(), key=lambda item: (-item[1], item[0])):
        print(f"- {scenario_type}: {count}")
    print()
    print("Persona depth matrix:")
    for persona, depths in report["persona_depths"].items():
        print(f"- {persona}: {depths}")
    if report["warnings"]:
        print()
        print("Warnings:")
        for warning in report["warnings"]:
            print(f"- {warning}")
    if report["missing_depth_examples"]:
        print()
        print("Missing depth examples:")
        for path in report["missing_depth_examples"]:
            print(f"- {path}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    args = parser.parse_args()

    report = audit(load_conversations())
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print_text(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
