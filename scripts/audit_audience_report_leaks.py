"""Audit parent/teacher-safe reports for raw private-detail leakage.

This is a deterministic guard for the synthetic Saga A rehearsal layer. It does
not prove a report is safe for real students, but it catches regressions where a
safe audience report starts quoting raw turns, scenario seeds, file paths, or
other reconstructable private details.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent

SAFE_AUDIENCES = ("parent_safe", "teacher_safe")
REPORT_ROOT = ROOT / "data" / "audience_reports"
CONVERSATION_ROOT = ROOT / "data" / "generated_conversations"
DEFAULT_REPORT = ROOT / "umi" / "reports" / "audience-report-leak-audit-latest.md"

FORBIDDEN_PATTERNS = {
    "raw_file_path": re.compile(r"data/(?:generated_conversations|case_summaries|analysis_reports)/"),
    "scenario_seed": re.compile(r"\bscenario_seed(?:_id)?\b", re.IGNORECASE),
    "raw_turn_label": re.compile(r"\b(?:raw_conversation|transcript|turns)\b", re.IGNORECASE),
    "private_json_ref": re.compile(r"\b[a-z0-9_./-]+\.json\b", re.IGNORECASE),
}
SENTENCE_RE = re.compile(r"[。！？!?\.\n]+")
LONG_QUOTED_TEXT_RE = re.compile(r"[「『\"]([^」』\"]{12,})[」』\"]")


def _split_sentences(text: str) -> list[str]:
    return [part.strip() for part in SENTENCE_RE.split(text) if part.strip()]


def _load_private_chunks() -> dict[str, list[str]]:
    chunks: dict[str, list[str]] = {}
    for path in sorted(CONVERSATION_ROOT.glob("*.json")):
        if path.name == "index.json":
            continue
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        persona = str(payload.get("persona_id") or "").replace("saga_a_", "")
        turns = payload.get("turns") or []
        if not persona or not isinstance(turns, list):
            continue
        persona_chunks = chunks.setdefault(persona, [])
        seed = str(payload.get("scenario_seed") or "")
        persona_chunks.extend(chunk for chunk in _split_sentences(seed) if len(chunk) >= 12)
        for turn in turns:
            if not isinstance(turn, dict) or turn.get("role") != "user":
                continue
            content = str(turn.get("content") or "")
            persona_chunks.extend(chunk for chunk in _split_sentences(content) if len(chunk) >= 12)
    return chunks


def _pattern_hits(text: str) -> list[dict[str, str]]:
    hits: list[dict[str, str]] = []
    for name, pattern in FORBIDDEN_PATTERNS.items():
        for match in pattern.finditer(text):
            hits.append({"type": name, "match": match.group(0)})
    return hits


def _exact_private_hits(text: str, private_chunks: list[str]) -> list[str]:
    hits: list[str] = []
    for chunk in private_chunks:
        if chunk in text:
            hits.append(chunk)
    return sorted(set(hits))


def _audit_report(path: Path, private_chunks_by_persona: dict[str, list[str]]) -> dict[str, Any]:
    audience = path.parent.name
    persona = path.stem
    text = path.read_text(encoding="utf-8")
    exact_hits = _exact_private_hits(text, private_chunks_by_persona.get(persona, []))
    patterns = _pattern_hits(text)
    long_quotes = [match.group(1) for match in LONG_QUOTED_TEXT_RE.finditer(text)]
    fail_reasons: list[str] = []
    if exact_hits:
        fail_reasons.append("exact_private_chunk")
    if patterns:
        fail_reasons.append("forbidden_pattern")
    if long_quotes:
        fail_reasons.append("long_quote")
    return {
        "path": str(path.relative_to(ROOT)),
        "audience": audience,
        "persona": persona,
        "status": "FAIL" if fail_reasons else "PASS",
        "fail_reasons": sorted(set(fail_reasons)),
        "exact_private_chunks": len(exact_hits),
        "long_quotes": len(long_quotes),
        "pattern_hits": patterns,
    }


def _render_markdown(results: list[dict[str, Any]]) -> str:
    failures = [result for result in results if result["status"] != "PASS"]
    lines = [
        "# Audience Report Leak Audit",
        "",
        f"Reports checked: {len(results)}",
        f"Failures: {len(failures)}",
        "",
        "## Summary",
        "",
    ]
    for audience in SAFE_AUDIENCES:
        audience_results = [result for result in results if result["audience"] == audience]
        failed = [result for result in audience_results if result["status"] != "PASS"]
        lines.append(f"- {audience}: {len(audience_results) - len(failed)} pass / {len(failed)} fail")
    lines.extend(["", "## Failures", ""])
    if not failures:
        lines.append("None.")
    else:
        for result in failures:
            lines.append(
                f"- `{result['path']}`: {', '.join(result['fail_reasons'])}; "
                f"exact_private_chunks={result['exact_private_chunks']} "
                f"long_quotes={result['long_quotes']} "
                f"patterns={len(result['pattern_hits'])}"
            )
    lines.extend(
        [
            "",
            "## Policy",
            "",
            "- Parent-safe and teacher-safe reports must not include raw conversation paths, scenario seeds, raw turns, or reconstructable private event detail.",
            "- Internal reviewer reports are intentionally excluded from this safe-surface audit.",
            "- This deterministic audit is a regression guard, not a substitute for human review before a real pilot.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--json", type=Path, default=None)
    args = parser.parse_args()

    private_chunks = _load_private_chunks()
    results: list[dict[str, Any]] = []
    for audience in SAFE_AUDIENCES:
        for path in sorted((REPORT_ROOT / audience).glob("*.md")):
            results.append(_audit_report(path, private_chunks))

    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(_render_markdown(results), encoding="utf-8")
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")

    failures = [result for result in results if result["status"] != "PASS"]
    print(f"Audience report leak audit: {len(results) - len(failures)} pass / {len(failures)} fail")
    print(f"Report: {args.report}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
