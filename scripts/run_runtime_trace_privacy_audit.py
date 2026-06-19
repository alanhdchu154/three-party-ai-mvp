"""Audit runtime trace surfaces for privacy-boundary policy.

This deterministic audit checks generated runtime artifacts across the local
pipeline, not only final audience reports. It classifies surfaces as
audience-safe, restricted reviewer/internal, or metadata-only audit logs, then
applies a surface-specific privacy policy.

It is still a synthetic benchmark audit. Passing does not prove real-world
semantic privacy or deployment readiness.
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

from scripts import run_relationship_leak_audit

DATA_DIR = ROOT / "data"
DEFAULT_JSON = ROOT / "umi" / "reports" / "runtime-trace-privacy-latest.json"
DEFAULT_MD = ROOT / "umi" / "reports" / "runtime-trace-privacy-latest.md"

RAW_TRACE_RE = re.compile(
    r"(scenario_seed|scenario_seed_id|raw_conversation|raw turns|raw turns:|"
    r"transcript|generated_conversations|secret truths?|do_not_share|"
    r"private chunk|private_chunk|conversation artifact)",
    re.IGNORECASE,
)
AUDIT_LOG_FORBIDDEN_KEYS = {
    "content",
    "conversation",
    "messages",
    "prompt",
    "raw",
    "raw_conversation",
    "scenario_seed",
    "scenario_seed_id",
    "secret",
    "transcript",
    "turns",
}
AUDIT_LOG_ALLOWED_KEYS = {
    "audience",
    "manifest",
    "path",
    "review_notes",
    "run_id",
    "student_id",
}


def audit_runtime_traces() -> dict[str, Any]:
    surfaces: list[dict[str, Any]] = []
    for path in _audience_safe_paths():
        audience, persona = _audience_and_persona(path)
        surfaces.append(_audit_audience_safe(path, audience, persona))
    for path in _restricted_paths():
        surfaces.append(_audit_restricted(path))
    for path in _audit_log_paths():
        surfaces.append(_audit_log(path))
    failures = [surface for surface in surfaces if surface["status"] != "PASS"]
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "claim_boundary": (
            "Deterministic runtime trace privacy audit over synthetic benchmark "
            "artifacts. This is not proof of real-world semantic privacy."
        ),
        "surfaces_checked": len(surfaces),
        "failures": len(failures),
        "surface_counts": _surface_counts(surfaces),
        "surfaces": surfaces,
    }


def _audience_safe_paths() -> list[Path]:
    paths = sorted((DATA_DIR / "audience_reports" / "parent_safe").glob("*.md"))
    paths += sorted((DATA_DIR / "audience_reports" / "teacher_safe").glob("*.md"))
    paths += sorted((DATA_DIR / "pilot_runs").glob("*/*_safe.md"))
    return paths


def _restricted_paths() -> list[Path]:
    paths = sorted((DATA_DIR / "audience_reports" / "internal_reviewer").glob("*.md"))
    paths += sorted((DATA_DIR / "case_summaries").glob("*.md"))
    paths += sorted((DATA_DIR / "trajectory_reports").glob("*.md"))
    paths += sorted((DATA_DIR / "pilot_runs").glob("*/internal_reviewer.md"))
    paths += sorted((DATA_DIR / "pilot_runs").glob("*/trajectory_report.md"))
    paths += sorted((DATA_DIR / "pilot_runs").glob("*/case_summary.json"))
    return paths


def _audit_log_paths() -> list[Path]:
    return sorted((DATA_DIR / "pilot_runs").glob("*/audit_log.jsonl"))


def _audit_audience_safe(path: Path, audience: str, persona: str) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    findings: list[dict[str, Any]] = []
    raw_hits = sorted(set(RAW_TRACE_RE.findall(text)))
    if raw_hits:
        findings.append({"policy": "no_raw_trace_markers", "hits": raw_hits})

    relationship = run_relationship_leak_audit._audit_report(audience, persona, path)
    if relationship["status"] != "PASS":
        findings.append({"policy": "no_relationship_context_leak", "hits": relationship["matches"]})

    return _surface_result(path, "audience_safe", findings)


def _audit_restricted(path: Path) -> dict[str, Any]:
    text = _read_surface_text(path)
    findings: list[dict[str, Any]] = []
    if "synthetic" not in text.lower():
        findings.append({"policy": "synthetic_boundary_required", "hits": []})
    boundary_ok = bool(re.search(r"(do not reveal|not diagnoses?|not diagnosis|not real-world)", text, re.IGNORECASE))
    if not boundary_ok:
        findings.append({"policy": "restricted_boundary_required", "hits": []})
    return _surface_result(path, "restricted_reviewer", findings)


def _audit_log(path: Path) -> dict[str, Any]:
    findings: list[dict[str, Any]] = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            findings.append({"policy": "valid_jsonl", "line": line_no, "hits": [line[:80]]})
            continue
        payload = event.get("payload")
        if not isinstance(payload, dict):
            findings.append({"policy": "metadata_payload_object", "line": line_no, "hits": []})
            continue
        bad_keys = sorted(_nested_forbidden_keys(payload))
        if bad_keys:
            findings.append({"policy": "metadata_only_payload", "line": line_no, "hits": bad_keys})
        unexpected = sorted(set(payload) - AUDIT_LOG_ALLOWED_KEYS)
        if unexpected:
            findings.append({"policy": "unexpected_payload_keys", "line": line_no, "hits": unexpected})
    return _surface_result(path, "audit_log", findings)


def _nested_forbidden_keys(value: Any) -> set[str]:
    hits: set[str] = set()
    if isinstance(value, dict):
        for key, child in value.items():
            if str(key).lower() in AUDIT_LOG_FORBIDDEN_KEYS:
                hits.add(str(key))
            hits.update(_nested_forbidden_keys(child))
    elif isinstance(value, list):
        for item in value:
            hits.update(_nested_forbidden_keys(item))
    return hits


def _read_surface_text(path: Path) -> str:
    if path.suffix == ".json":
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return path.read_text(encoding="utf-8", errors="replace")
        return json.dumps(payload, ensure_ascii=False)
    return path.read_text(encoding="utf-8")


def _surface_result(path: Path, surface_type: str, findings: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "path": _display_path(path),
        "surface_type": surface_type,
        "status": "FAIL" if findings else "PASS",
        "findings": findings,
    }


def _surface_counts(surfaces: list[dict[str, Any]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for surface in surfaces:
        key = str(surface["surface_type"])
        counts[key] = counts.get(key, 0) + 1
    return counts


def _audience_and_persona(path: Path) -> tuple[str, str]:
    if path.parent.name in {"parent_safe", "teacher_safe"}:
        return path.parent.name, path.stem
    audience = path.stem
    run_id = path.parent.name
    persona = run_id.removeprefix("v0_8_smoke_")
    return audience, persona


def _display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Runtime Trace Privacy Audit",
        "",
        f"Generated: `{report['generated_at']}`",
        f"Surfaces checked: `{report['surfaces_checked']}`",
        f"Failures: `{report['failures']}`",
        f"Surface counts: `{report['surface_counts']}`",
        "",
        "## Claim Boundary",
        "",
        report["claim_boundary"],
        "",
        "## Summary",
        "",
        "| Surface type | Status | Path |",
        "| --- | --- | --- |",
    ]
    for surface in report["surfaces"]:
        lines.append(f"| `{surface['surface_type']}` | `{surface['status']}` | `{surface['path']}` |")

    lines.extend(["", "## Failures", ""])
    failures = [surface for surface in report["surfaces"] if surface["status"] != "PASS"]
    if not failures:
        lines.append("None.")
    else:
        for surface in failures:
            lines.append(f"- `{surface['path']}` / `{surface['surface_type']}`")
            for finding in surface["findings"]:
                lines.append(f"  - `{finding['policy']}` hits={finding.get('hits', [])}")

    lines.extend(
        [
            "",
            "## Notes",
            "",
            "- Audience-safe surfaces are checked for raw trace markers and relationship-context leaks.",
            "- Restricted reviewer/internal surfaces must carry synthetic and restricted-boundary language.",
            "- Audit logs must remain metadata-only and must not store prompts, transcripts, turns, or raw scenario fields.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--report", type=Path, default=DEFAULT_MD)
    args = parser.parse_args()

    report = audit_runtime_traces()
    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    args.report.write_text(render_markdown(report), encoding="utf-8")

    print(
        f"Runtime trace privacy audit: {report['surfaces_checked'] - report['failures']} pass / "
        f"{report['failures']} fail"
    )
    print(f"Report: {args.report}")
    return 0 if report["failures"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
