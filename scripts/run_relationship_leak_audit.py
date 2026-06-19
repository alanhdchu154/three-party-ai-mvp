"""Audit audience-safe reports for reconstructable relationship-context leaks.

This deterministic check complements the exact leak audit and semantic trace
audit. It catches parent-safe or teacher-safe reports that disclose enough
persona or family-system context to reconstruct private relationship dynamics,
even when no raw quote or exact private chunk is leaked.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
AUDIENCE_REPORT_DIR = ROOT / "data" / "audience_reports"
DEFAULT_JSON = ROOT / "umi" / "reports" / "relationship-leak-audit-latest.json"
DEFAULT_MD = ROOT / "umi" / "reports" / "relationship-leak-audit-latest.md"

SAFE_AUDIENCES = ("parent_safe", "teacher_safe")
PERSONAS = (
    "alan_teacher",
    "keer",
    "michael",
    "michael_mom",
    "rachel",
    "shen_mom",
    "shen_you",
    "stepdad",
    "uncle",
)


@dataclass(frozen=True)
class RelationshipMarker:
    persona: str
    marker_id: str
    description: str
    terms: tuple[str, ...]
    fail_threshold: int = 1


RELATIONSHIP_MARKERS = (
    RelationshipMarker(
        "michael",
        "conditional_belonging",
        "Private blended-family belonging and fairness-as-distance context.",
        (
            "conditional belonging",
            "fairness is not love",
            "fairness as distance",
            "special treatment",
            "not receiving special",
            "being unwanted",
            "unwanted in the family",
        ),
    ),
    RelationshipMarker(
        "keer",
        "sibling_ambiguity",
        "Private sibling-status, preference, and atmosphere-manager context.",
        (
            "half-sibling",
            "sibling status",
            "atmosphere manager",
            "easy child",
            "easier child",
            "favoritism",
        ),
    ),
    RelationshipMarker(
        "shen_you",
        "mediated_monitoring",
        "Private unsynced-space and adult-script resistance context.",
        (
            "unsynced private space",
            "adult scripts",
            "avoidance tactics",
            "known through intermediaries",
            "indirect monitoring",
            "provider coordination",
        ),
    ),
    RelationshipMarker(
        "rachel",
        "governed_autonomy",
        "Private writing, diary, and family-governance pressure context.",
        (
            "diary-like",
            "note-taker",
            "family governance",
            "assigned future",
            "quiet resistance",
            "family-control",
            "writerly autonomy",
        ),
    ),
    RelationshipMarker(
        "michael_mom",
        "parent_reverse_engineering",
        "Parent-side reverse-engineering and face/ranking context.",
        (
            "reverse-engineering",
            "ranking anxiety",
            "social face",
            "monitoring substitute",
            "mother-son contact",
        ),
    ),
    RelationshipMarker(
        "shen_mom",
        "surveillance_channel",
        "Parent-side surveillance-channel and family-disorder context.",
        (
            "marital instability",
            "surveillance channel",
            "indirect surveillance",
            "family disorder",
            "providers rather than direct trust",
            "mediated knowledge",
        ),
    ),
    RelationshipMarker(
        "stepdad",
        "procedural_care",
        "Stepparent emotional-asymmetry and procedural-care context.",
        (
            "fairness as distance",
            "emotional asymmetry",
            "easier affection",
            "procedural care",
            "business-like care",
        ),
    ),
    RelationshipMarker(
        "uncle",
        "authority_governance",
        "Authority, succession, and control context.",
        (
            "succession",
            "governance-minded",
            "administrative privilege",
            "tighten control",
            "authority pressure",
            "family governance",
        ),
    ),
)


def audit_reports() -> dict[str, Any]:
    reports: list[dict[str, Any]] = []
    for audience in SAFE_AUDIENCES:
        for persona in PERSONAS:
            path = AUDIENCE_REPORT_DIR / audience / f"{persona}.md"
            reports.append(_audit_report(audience, persona, path))
    failures = [report for report in reports if report["status"] != "PASS"]
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "claim_boundary": (
            "Deterministic relationship-context leak audit over synthetic "
            "benchmark reports. This is not proof of real-world semantic privacy."
        ),
        "reports_checked": len(reports),
        "failures": len(failures),
        "reports": reports,
    }


def _audit_report(audience: str, persona: str, path: Path) -> dict[str, Any]:
    if not path.exists():
        return {
            "audience": audience,
            "persona": persona,
            "path": _display_path(path),
            "status": "FAIL",
            "reason": "missing_report",
            "matches": [],
        }

    text = path.read_text(encoding="utf-8")
    markers = [marker for marker in RELATIONSHIP_MARKERS if marker.persona == persona]
    matches = [_marker_match(marker, text) for marker in markers]
    matches = [match for match in matches if match["status"] == "FAIL"]
    return {
        "audience": audience,
        "persona": persona,
        "path": _display_path(path),
        "status": "FAIL" if matches else "PASS",
        "reason": "relationship_context_leak" if matches else "",
        "matches": matches,
    }


def _marker_match(marker: RelationshipMarker, text: str) -> dict[str, Any]:
    hits = []
    for term in marker.terms:
        if _contains_term(text, term):
            hits.append(term)
    return {
        "marker_id": marker.marker_id,
        "description": marker.description,
        "status": "FAIL" if len(hits) >= marker.fail_threshold else "PASS",
        "hits": hits,
        "threshold": marker.fail_threshold,
    }


def _contains_term(text: str, term: str) -> bool:
    if re.search(r"[\u4e00-\u9fff]", term):
        return term in text
    pattern = r"\b" + re.escape(term).replace(r"\ ", r"\s+") + r"\b"
    return bool(re.search(pattern, text, re.IGNORECASE))


def _display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Relationship Leak Audit",
        "",
        f"Generated: `{report['generated_at']}`",
        f"Reports checked: `{report['reports_checked']}`",
        f"Failures: `{report['failures']}`",
        "",
        "## Claim Boundary",
        "",
        report["claim_boundary"],
        "",
        "## Summary",
        "",
        "| Audience | Persona | Status | Report |",
        "| --- | --- | --- | --- |",
    ]
    for item in report["reports"]:
        lines.append(
            f"| `{item['audience']}` | `{item['persona']}` | "
            f"`{item['status']}` | `{item['path']}` |"
        )

    lines.extend(["", "## Failures", ""])
    failures = [item for item in report["reports"] if item["status"] != "PASS"]
    if not failures:
        lines.append("None.")
    else:
        for item in failures:
            lines.append(f"- `{item['audience']}:{item['persona']}`: {item['reason']}")
            for match in item["matches"]:
                lines.append(
                    f"  - `{match['marker_id']}` hits={match['hits']} "
                    f"threshold={match['threshold']}"
                )

    lines.extend(
        [
            "",
            "## Notes",
            "",
            "- This audit allows broad support dimensions such as `family_dynamics`.",
            "- It flags more reconstructable relationship markers documented in the persona bible and relationship graph.",
            "- It should be read alongside the exact leak audit, semantic trace audit, and human reviewer annotations.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--report", type=Path, default=DEFAULT_MD)
    args = parser.parse_args()

    report = audit_reports()
    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    args.report.write_text(render_markdown(report), encoding="utf-8")

    print(
        f"Relationship leak audit: {report['reports_checked'] - report['failures']} pass / "
        f"{report['failures']} fail"
    )
    print(f"Report: {args.report}")
    return 0 if report["failures"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
