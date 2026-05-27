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

VALID_TIMELINE_STAGES = {
    "middle_school",
    "grade_7",
    "grade_8",
    "grade_9",
    "grade_10",
    "grade_11",
    "grade_12",
    "current",
    "retrospective",
}

VALID_CONVERSATION_FRAMES = {
    "live_event",
    "recent_followup",
    "old_memory",
    "pattern_reflection",
}

VALID_LOOKBACK_WINDOWS = {
    "past_week",
    "past_month",
    "past_semester",
    "past_half_year",
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
    timeline_counts: Counter[str] = Counter()
    conversation_frame_counts: Counter[str] = Counter()
    lookback_counts: Counter[str] = Counter()
    missing_depth: list[str] = []
    missing_type: list[str] = []
    invalid_timeline_stage: list[str] = []
    invalid_conversation_frame: list[str] = []
    invalid_lookback_window: list[str] = []
    turns: list[int] = []

    for conv in conversations:
        persona = conv.get("persona_id", "unknown")
        depth = conv.get("depth") or "<missing>"
        scenario_type = conv.get("scenario_type") or "<missing>"
        timeline_stage = conv.get("timeline_stage")
        conversation_frame = conv.get("conversation_frame")
        lookback_window = conv.get("lookback_window")
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
        if timeline_stage:
            timeline_counts[str(timeline_stage)] += 1
            if timeline_stage not in VALID_TIMELINE_STAGES:
                invalid_timeline_stage.append(conv["_path"])
        if conversation_frame:
            conversation_frame_counts[str(conversation_frame)] += 1
            if conversation_frame not in VALID_CONVERSATION_FRAMES:
                invalid_conversation_frame.append(conv["_path"])
        if lookback_window:
            lookback_counts[str(lookback_window)] += 1
            if lookback_window not in VALID_LOOKBACK_WINDOWS:
                invalid_lookback_window.append(conv["_path"])

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
    if invalid_timeline_stage:
        warnings.append(f"{len(invalid_timeline_stage)} conversations use unknown timeline_stage values.")
    if invalid_conversation_frame:
        warnings.append(f"{len(invalid_conversation_frame)} conversations use unknown conversation_frame values.")
    if invalid_lookback_window:
        warnings.append(f"{len(invalid_lookback_window)} conversations use unknown lookback_window values.")
    timeline_n = sum(timeline_counts.values())
    if timeline_n >= 20 and lookback_counts.get("past_week", 0) / timeline_n > 0.75:
        warnings.append("Timeline-aware conversations are still too concentrated in `past_week`; add semester/half-year context.")

    return {
        "n_conversations": n,
        "depth_counts": dict(depth_counts),
        "depth_share": {k: round(v, 3) for k, v in sorted(depth_share.items())},
        "target_depth_share": TARGET_DEPTH_SHARE,
        "scenario_type_counts": dict(type_counts),
        "timeline_stage_counts": dict(timeline_counts),
        "conversation_frame_counts": dict(conversation_frame_counts),
        "lookback_window_counts": dict(lookback_counts),
        "persona_counts": dict(persona_counts),
        "persona_depths": {persona: dict(counter) for persona, counter in sorted(persona_depths.items())},
        "turns": {
            "min": min(turns) if turns else 0,
            "avg": round(statistics.mean(turns), 1) if turns else 0,
            "max": max(turns) if turns else 0,
        },
        "missing_depth_examples": missing_depth[:10],
        "missing_type_examples": missing_type[:10],
        "invalid_timeline_stage_examples": invalid_timeline_stage[:10],
        "invalid_conversation_frame_examples": invalid_conversation_frame[:10],
        "invalid_lookback_window_examples": invalid_lookback_window[:10],
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
    if report["timeline_stage_counts"]:
        print("Timeline stages:")
        for timeline_stage, count in sorted(report["timeline_stage_counts"].items(), key=lambda item: (-item[1], item[0])):
            print(f"- {timeline_stage}: {count}")
        print()
    if report["conversation_frame_counts"]:
        print("Conversation frames:")
        for frame, count in sorted(report["conversation_frame_counts"].items(), key=lambda item: (-item[1], item[0])):
            print(f"- {frame}: {count}")
        print()
    if report["lookback_window_counts"]:
        print("Lookback windows:")
        for window, count in sorted(report["lookback_window_counts"].items(), key=lambda item: (-item[1], item[0])):
            print(f"- {window}: {count}")
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
    if report["invalid_timeline_stage_examples"]:
        print()
        print("Invalid timeline_stage examples:")
        for path in report["invalid_timeline_stage_examples"]:
            print(f"- {path}")
    if report["invalid_conversation_frame_examples"]:
        print()
        print("Invalid conversation_frame examples:")
        for path in report["invalid_conversation_frame_examples"]:
            print(f"- {path}")
    if report["invalid_lookback_window_examples"]:
        print()
        print("Invalid lookback_window examples:")
        for path in report["invalid_lookback_window_examples"]:
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
