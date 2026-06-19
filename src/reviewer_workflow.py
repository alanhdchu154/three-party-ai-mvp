"""Human reviewer workflow for case and trajectory calibration.

This layer stores lightweight JSON notes. It does not edit source artifacts,
call LLMs, or treat synthetic results as validation.
"""

from __future__ import annotations

import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
REVIEWER_NOTES_DIR = DATA_DIR / "reviewer_notes"
REVIEWER_SUMMARIES_DIR = DATA_DIR / "reviewer_summaries"

ARTIFACT_TYPES = {
    "audience_report",
    "baseline_comparison",
    "case_summary",
    "coordination_snapshot",
    "trajectory_report",
}
VERDICTS = {
    "agree",
    "disagree",
    "minor_issue",
    "needs_more_evidence",
    "not_actionable",
    "over_escalated",
    "privacy_concern",
    "safe",
    "true_positive",
    "false_positive",
    "under_escalated",
    "under_evidenced",
}
CONFIDENCE_LEVELS = {"low", "medium", "high"}


def build_review_note(
    *,
    artifact_type: str,
    artifact_id: str,
    reviewer: str,
    verdict: str,
    confidence: str = "medium",
    evidence_ref_ids: list[str] | None = None,
    comments: str = "",
    privacy_concerns: list[str] | None = None,
    action_items: list[str] | None = None,
    source_path: str = "",
    protected_terms: list[str] | None = None,
) -> dict[str, Any]:
    """Create a normalized reviewer note payload."""
    note = {
        "review_id": _review_id(artifact_type, artifact_id, reviewer),
        "artifact_type": artifact_type,
        "artifact_id": artifact_id,
        "source_path": source_path,
        "reviewer": reviewer,
        "verdict": verdict,
        "confidence": confidence,
        "evidence_ref_ids": evidence_ref_ids or [],
        "comments": comments,
        "privacy_concerns": privacy_concerns or [],
        "action_items": action_items or [],
        "created_at": datetime.utcnow().isoformat() + "Z",
        "synthetic_only_warning_acknowledged": True,
    }
    note = _sanitize_review_note(note, protected_terms=protected_terms or [])
    validate_review_note(note)
    return note


def validate_review_note(note: dict[str, Any]) -> None:
    if note.get("artifact_type") not in ARTIFACT_TYPES:
        raise ValueError(f"artifact_type must be one of {sorted(ARTIFACT_TYPES)}")
    if not note.get("artifact_id"):
        raise ValueError("artifact_id is required")
    if not note.get("reviewer"):
        raise ValueError("reviewer is required")
    if note.get("verdict") not in VERDICTS:
        raise ValueError(f"verdict must be one of {sorted(VERDICTS)}")
    if note.get("confidence") not in CONFIDENCE_LEVELS:
        raise ValueError(f"confidence must be one of {sorted(CONFIDENCE_LEVELS)}")
    if not isinstance(note.get("evidence_ref_ids", []), list):
        raise ValueError("evidence_ref_ids must be a list")
    if not isinstance(note.get("privacy_concerns", []), list):
        raise ValueError("privacy_concerns must be a list")
    if not isinstance(note.get("action_items", []), list):
        raise ValueError("action_items must be a list")


def save_review_note(note: dict[str, Any], *, notes_dir: Path = REVIEWER_NOTES_DIR) -> Path:
    validate_review_note(note)
    notes_dir.mkdir(parents=True, exist_ok=True)
    path = notes_dir / f"{_safe_id(note['review_id'])}.json"
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(note, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(tmp, path)
    return path


def load_review_notes(notes_dir: Path = REVIEWER_NOTES_DIR) -> list[dict[str, Any]]:
    if not notes_dir.exists():
        return []
    notes: list[dict[str, Any]] = []
    for path in sorted(notes_dir.glob("*.json")):
        try:
            note = json.loads(path.read_text(encoding="utf-8"))
            validate_review_note(note)
        except (OSError, json.JSONDecodeError, ValueError):
            continue
        note["_source_path"] = _rel(path)
        notes.append(note)
    return notes


def summarize_reviews(notes: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    notes = notes if notes is not None else load_review_notes()
    by_artifact: dict[str, dict[str, Any]] = {}
    for note in notes:
        key = f"{note['artifact_type']}:{note['artifact_id']}"
        bucket = by_artifact.setdefault(
            key,
            {
                "artifact_type": note["artifact_type"],
                "artifact_id": note["artifact_id"],
                "n_reviews": 0,
                "verdict_counts": {},
                "confidence_counts": {},
                "privacy_concerns": [],
                "action_items": [],
                "evidence_ref_ids": [],
                "source_paths": [],
                "reviewers": [],
            },
        )
        bucket["n_reviews"] += 1
        _inc(bucket["verdict_counts"], note["verdict"])
        _inc(bucket["confidence_counts"], note["confidence"])
        bucket["privacy_concerns"].extend(note.get("privacy_concerns") or [])
        bucket["action_items"].extend(note.get("action_items") or [])
        bucket["evidence_ref_ids"].extend(note.get("evidence_ref_ids") or [])
        if note.get("source_path"):
            bucket["source_paths"].append(note["source_path"])
        bucket["reviewers"].append(note["reviewer"])

    for bucket in by_artifact.values():
        bucket["privacy_concerns"] = sorted(set(bucket["privacy_concerns"]))
        bucket["action_items"] = sorted(set(bucket["action_items"]))
        bucket["evidence_ref_ids"] = sorted(set(bucket["evidence_ref_ids"]))
        bucket["source_paths"] = sorted(set(bucket["source_paths"]))
        bucket["reviewers"] = sorted(set(bucket["reviewers"]))
        bucket["calibration_status"] = _calibration_status(bucket)

    return {
        "n_notes": len(notes),
        "n_artifacts_reviewed": len(by_artifact),
        "artifacts": by_artifact,
    }


def artifact_calibration(
    summary: dict[str, Any],
    *,
    artifact_type: str,
    artifact_id: str,
) -> dict[str, Any] | None:
    """Return aggregated calibration for one artifact, if available."""
    return summary.get("artifacts", {}).get(f"{artifact_type}:{artifact_id}")


def render_reviewer_summary(
    summary: dict[str, Any],
    *,
    title: str = "Reviewer Calibration Summary",
) -> str:
    lines = [
        f"# {title}",
        "",
        "> Reviewer notes calibrate synthetic case and trajectory outputs. They do not convert synthetic data into real pilot validation.",
        "",
        "> Reviewer identity boundary: `Umi` is an AI-assisted internal reviewer label. `ReviewerB` is a local second-reviewer label seeded for screening coverage. These labels do not represent external independent human validation unless a separate external review record says so.",
        "",
        f"- Notes: `{summary['n_notes']}`",
        f"- Artifacts reviewed: `{summary['n_artifacts_reviewed']}`",
        "",
    ]
    if not summary["artifacts"]:
        lines.extend([
            "## No Reviews Yet",
            "- Add JSON notes under `data/reviewer_notes/` or use `src.reviewer_workflow.build_review_note()`.",
            "- Start with high-trigger trajectory reports such as `michael:burnout_risk`.",
            "",
        ])
        return "\n".join(lines)

    for key, artifact in sorted(summary["artifacts"].items()):
        lines.extend([
            f"## {key}",
            f"- Reviews: `{artifact['n_reviews']}`",
            f"- Status: `{artifact['calibration_status']}`",
            f"- Verdicts: `{artifact['verdict_counts']}`",
            f"- Confidence: `{artifact['confidence_counts']}`",
            f"- Reviewers: `{', '.join(artifact['reviewers'])}`",
            f"- Sources: `{', '.join(artifact['source_paths']) if artifact['source_paths'] else 'not recorded'}`",
            f"- Evidence refs: `{', '.join(artifact['evidence_ref_ids']) if artifact['evidence_ref_ids'] else 'not recorded'}`",
            "",
            "### Privacy Concerns",
            _bullets(artifact["privacy_concerns"]),
            "",
            "### Action Items",
            _bullets(artifact["action_items"]),
            "",
        ])
    return "\n".join(lines)


def generate_reviewer_summary(
    *,
    notes_dir: Path = REVIEWER_NOTES_DIR,
    output_dir: Path = REVIEWER_SUMMARIES_DIR,
    filename: str = "reviewer_calibration_summary.md",
    title: str = "Reviewer Calibration Summary",
) -> Path:
    notes = load_review_notes(notes_dir)
    summary = summarize_reviews(notes)
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / filename
    path.write_text(render_reviewer_summary(summary, title=title), encoding="utf-8")
    return path


def _calibration_status(bucket: dict[str, Any]) -> str:
    verdicts = bucket["verdict_counts"]
    if verdicts.get("privacy_concern"):
        return "privacy_review_needed"
    if verdicts.get("under_escalated"):
        return "under_escalation_review_needed"
    if verdicts.get("over_escalated"):
        return "over_escalation_review_needed"
    if (
        verdicts.get("false_positive")
        or verdicts.get("under_evidenced")
        or verdicts.get("needs_more_evidence")
        or verdicts.get("minor_issue")
        or verdicts.get("not_actionable")
    ):
        return "needs_calibration"
    if verdicts.get("agree") or verdicts.get("true_positive") or verdicts.get("safe"):
        return "reviewed_supported"
    return "reviewed_unclear"


def _review_id(artifact_type: str, artifact_id: str, reviewer: str) -> str:
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%S%fZ")
    return f"{artifact_type}__{artifact_id}__{reviewer}__{timestamp}"


def _safe_id(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_\-.]", "_", value.strip())


def _inc(counts: dict[str, int], key: str) -> None:
    counts[key] = counts.get(key, 0) + 1


def _bullets(items: list[str]) -> str:
    if not items:
        return "- None."
    return "\n".join(f"- {item}" for item in items)


def _sanitize_review_note(note: dict[str, Any], *, protected_terms: Iterable[str]) -> dict[str, Any]:
    """Redact caller-provided protected terms without rewriting benchmark metadata."""
    terms = [term.strip() for term in protected_terms if term and len(term.strip()) >= 2]
    if not terms:
        return note

    sanitized = dict(note)
    for key in ("comments",):
        sanitized[key] = _replace_terms(str(sanitized.get(key, "")), terms)
    for key in ("privacy_concerns", "action_items"):
        sanitized[key] = [_replace_terms(str(item), terms) for item in sanitized.get(key, [])]
    return sanitized


def _replace_terms(text: str, terms: list[str]) -> str:
    cleaned = text
    for term in sorted(terms, key=len, reverse=True):
        cleaned = cleaned.replace(term, "[redacted]")
    return cleaned


def _rel(path: Path) -> str:
    try:
        return str(path.relative_to(PROJECT_ROOT))
    except ValueError:
        return str(path)
