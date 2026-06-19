"""Audit audience-safe reports for reconstructable private trace overlap.

This deterministic check complements the exact leak audit. It does not prove
semantic privacy, but it catches regressions where a parent-safe or teacher-safe
report shares enough distinctive tokens from a private turn or scenario seed to
make the original private context reconstructable.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from scripts import run_baseline_comparison

AUDIENCE_REPORT_DIR = ROOT / "data" / "audience_reports"
DEFAULT_JSON = ROOT / "umi" / "reports" / "semantic-trace-audit-latest.json"
DEFAULT_MD = ROOT / "umi" / "reports" / "semantic-trace-audit-latest.md"

SAFE_AUDIENCES = ("parent_safe", "teacher_safe")
MIN_DISTINCTIVE_TOKENS = 5
OVERLAP_TOKEN_THRESHOLD = 4
OVERLAP_RATIO_THRESHOLD = 0.30

STOPWORDS = {
    "about",
    "action",
    "after",
    "again",
    "alan",
    "because",
    "before",
    "case",
    "class",
    "coordinator",
    "could",
    "evidence",
    "family",
    "from",
    "have",
    "help",
    "just",
    "medium",
    "michael",
    "minor",
    "mother",
    "need",
    "needed",
    "needs",
    "next",
    "parent",
    "private",
    "privacy",
    "report",
    "review",
    "reviewer",
    "safe",
    "school",
    "student",
    "support",
    "teacher",
    "that",
    "their",
    "there",
    "these",
    "they",
    "this",
    "through",
    "turn",
    "with",
    "would",
    "your",
    "學生",
    "老師",
    "家長",
    "支持",
    "報告",
    "隱私",
    "安全",
}

TOKEN_RE = re.compile(r"[A-Za-z][A-Za-z0-9']{3,}|[\u4e00-\u9fff]{2,}")


def audit_sample() -> dict[str, Any]:
    conversations = run_baseline_comparison.load_conversations()
    sample = run_baseline_comparison.select_sample(conversations)
    surfaces: list[dict[str, Any]] = []
    for conv in sample:
        persona = run_baseline_comparison._persona_report_id(conv)
        private_chunks = run_baseline_comparison._private_chunks(conv)
        for audience in SAFE_AUDIENCES:
            path = AUDIENCE_REPORT_DIR / audience / f"{persona}.md"
            surfaces.append(_audit_surface(conv, audience, path, private_chunks))
    failures = [surface for surface in surfaces if surface["status"] != "PASS"]
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "claim_boundary": (
            "Deterministic semantic trace audit over synthetic benchmark reports. "
            "This is not proof of real-world semantic privacy."
        ),
        "sample_size": len(sample),
        "surfaces_checked": len(surfaces),
        "failures": len(failures),
        "surfaces": surfaces,
    }


def _audit_surface(
    conv: dict[str, Any],
    audience: str,
    path: Path,
    private_chunks: list[str],
) -> dict[str, Any]:
    if not path.exists():
        return {
            "case_id": conv.get("id"),
            "audience": audience,
            "path": _display_path(path),
            "status": "FAIL",
            "reason": "missing_report",
            "max_overlap_tokens": 0,
            "max_overlap_ratio": 0,
            "matches": [],
        }

    report_text = path.read_text(encoding="utf-8")
    report_tokens = set(_tokens(report_text))
    matches: list[dict[str, Any]] = []
    for chunk in private_chunks:
        chunk_tokens = set(_tokens(chunk))
        if len(chunk_tokens) < MIN_DISTINCTIVE_TOKENS:
            continue
        overlap = sorted(chunk_tokens & report_tokens)
        ratio = len(overlap) / len(chunk_tokens)
        if len(overlap) >= OVERLAP_TOKEN_THRESHOLD and ratio >= OVERLAP_RATIO_THRESHOLD:
            matches.append(
                {
                    "overlap_tokens": overlap,
                    "overlap_token_count": len(overlap),
                    "overlap_ratio": round(ratio, 3),
                    "private_chunk_preview": _preview(chunk),
                }
            )

    max_overlap_tokens = max((match["overlap_token_count"] for match in matches), default=0)
    max_overlap_ratio = max((match["overlap_ratio"] for match in matches), default=0)
    return {
        "case_id": conv.get("id"),
        "audience": audience,
        "path": _display_path(path),
        "status": "FAIL" if matches else "PASS",
        "reason": "semantic_trace_overlap" if matches else "",
        "max_overlap_tokens": max_overlap_tokens,
        "max_overlap_ratio": max_overlap_ratio,
        "matches": matches,
    }


def _tokens(text: str) -> list[str]:
    tokens = []
    for token in TOKEN_RE.findall(text.lower()):
        if token in STOPWORDS:
            continue
        tokens.append(token)
    return tokens


def _display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def _preview(text: str) -> str:
    compact = re.sub(r"\s+", " ", text).strip()
    return compact[:120]


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Semantic Trace Audit",
        "",
        f"Generated: `{report['generated_at']}`",
        f"Sample size: `{report['sample_size']}`",
        f"Surfaces checked: `{report['surfaces_checked']}`",
        f"Failures: `{report['failures']}`",
        "",
        "## Claim Boundary",
        "",
        report["claim_boundary"],
        "",
        "## Summary",
        "",
        "| Case | Audience | Status | Max overlap tokens | Max overlap ratio | Report |",
        "| --- | --- | --- | ---: | ---: | --- |",
    ]
    for surface in report["surfaces"]:
        lines.append(
            f"| `{surface['case_id']}` | `{surface['audience']}` | "
            f"`{surface['status']}` | {surface['max_overlap_tokens']} | "
            f"{surface['max_overlap_ratio']} | `{surface['path']}` |"
        )
    lines.extend(["", "## Failures", ""])
    failures = [surface for surface in report["surfaces"] if surface["status"] != "PASS"]
    if not failures:
        lines.append("None.")
    else:
        for surface in failures:
            lines.append(f"- `{surface['case_id']}` / `{surface['audience']}`: {surface['reason']}")
            for match in surface["matches"][:3]:
                lines.append(
                    f"  - overlap={match['overlap_tokens']} "
                    f"ratio={match['overlap_ratio']} preview={match['private_chunk_preview']}"
                )
    lines.extend(
        [
            "",
            "## Notes",
            "",
            "- This is a conservative deterministic regression check, not a semantic privacy proof.",
            "- It should be read alongside the exact leak audit and human reviewer annotations.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--report", type=Path, default=DEFAULT_MD)
    args = parser.parse_args()

    report = audit_sample()
    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    args.report.write_text(render_markdown(report), encoding="utf-8")

    print(
        f"Semantic trace audit: {report['surfaces_checked'] - report['failures']} pass / "
        f"{report['failures']} fail"
    )
    print(f"Report: {args.report}")
    return 0 if report["failures"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
