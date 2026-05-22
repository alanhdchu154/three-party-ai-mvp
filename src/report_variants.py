"""Audience-safe report variants for pilot readiness.

Variants deliberately avoid raw secrets, scenario seeds, and do-not-share
details. They are derived from already-normalized case summaries.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from . import analysis_layer

AUDIENCES = {"internal_reviewer", "parent_safe", "teacher_safe"}
OUTPUT_DIR = analysis_layer.DATA_DIR / "audience_reports"


def render_case_variant(summary: dict[str, Any], audience: str) -> str:
    if audience not in AUDIENCES:
        raise ValueError(f"audience must be one of {sorted(AUDIENCES)}")
    if audience == "internal_reviewer":
        return analysis_layer.render_case_report(summary)
    if audience == "parent_safe":
        return _render_parent_safe(summary)
    return _render_teacher_safe(summary)


def generate_case_variant_reports(
    summaries: list[dict[str, Any]] | None = None,
    *,
    output_dir: Path = OUTPUT_DIR,
) -> list[Path]:
    summaries = summaries or analysis_layer.build_case_summaries()
    paths: list[Path] = []
    for audience in sorted(AUDIENCES):
        audience_dir = output_dir / audience
        audience_dir.mkdir(parents=True, exist_ok=True)
        for summary in summaries:
            path = audience_dir / f"{summary['student_id']}.md"
            path.write_text(render_case_variant(summary, audience), encoding="utf-8")
            paths.append(path)
    return paths


def _render_parent_safe(summary: dict[str, Any]) -> str:
    snapshot = summary.get("coordination_snapshot") or {}
    parent = snapshot.get("parent") or {}
    safe_bridges = snapshot.get("safe_bridges") or []
    lines = [
        f"# Parent-Safe Summary — {summary['student_id']}",
        "",
        "> This report intentionally excludes raw student statements and private details.",
        "",
        "## What Adults Can Know",
        "- The student may be experiencing strain across one or more areas.",
        "- The current recommendation is to lower pressure and preserve trust.",
        "- This is not a clinical diagnosis or proof of misconduct.",
        "",
        "## What Helps",
        _bullets(_parent_guidance(parent, safe_bridges)),
        "",
        "## What You Can Offer",
        _bullets(parent.get("what_they_can_offer") or [
            "Create low-pressure space without demanding immediate disclosure.",
            "Respond calmly if the student volunteers something.",
            "Keep actions reversible and supportive.",
        ]),
        "",
        "## What Not To Do",
        "- Do not ask for hidden details from the AI.",
        "- Do not interrogate the student based on this summary.",
        "- Do not assume synthetic benchmark evidence validates a real student case.",
        "",
        "## Privacy Boundary",
        "- Student private wording and hidden details are not included.",
        "- Teacher private constraints are not included.",
        "- The system translates support patterns rather than exposing secrets.",
        "",
        "## Evidence Boundary",
        f"- Source type: `{summary.get('source_type', 'unknown')}`",
        f"- Confidence: `{summary.get('confidence_level', 'low')}`",
        "- High-specificity evidence is withheld from this audience.",
        "",
    ]
    return "\n".join(lines)


def _render_teacher_safe(summary: dict[str, Any]) -> str:
    snapshot = summary.get("coordination_snapshot") or {}
    teacher = snapshot.get("teacher") or {}
    dimensions = [
        f"`{item.get('dimension')}` Level {item.get('level')}"
        for item in summary.get("risk_dimensions", [])
        if item.get("level", 0) >= 1
    ]
    lines = [
        f"# Teacher-Safe Summary — {summary['student_id']}",
        "",
        "> This report is for educational support. It excludes raw student statements and private family details.",
        "",
        "## Classroom-Relevant Pattern",
        "- Watch for changes in participation, affect, consistency, or avoidance.",
        "- Do not publicly challenge the student about sensitive patterns.",
        "- Use low-pressure, reversible support.",
        "",
        "## Active Dimensions",
        _bullets(dimensions or ["No active dimension available."]),
        "",
        "## What Helps",
        _bullets(_teacher_guidance(teacher)),
        "",
        "## What You Can Offer",
        _bullets(teacher.get("what_they_can_offer") or [
            "Offer structure without exposing private context.",
            "Avoid making the student explain personal circumstances in public.",
            "Escalate to the assigned reviewer if risk level increases.",
        ]),
        "",
        "## Privacy Boundary",
        "- Student private disclosures are not included.",
        "- Family private details are not included.",
        "- Parent private constraints are not included.",
        "",
        "## Evidence Boundary",
        f"- Source type: `{summary.get('source_type', 'unknown')}`",
        f"- Confidence: `{summary.get('confidence_level', 'low')}`",
        "- High-specificity evidence is withheld from this audience.",
        "",
    ]
    return "\n".join(lines)


def _bullets(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def _parent_guidance(parent: dict[str, Any], safe_bridges: list[str]) -> list[str]:
    guidance = [
        "Use calm, low-pressure check-ins instead of asking for hidden details.",
        "Focus on what support you can offer now, not on proving what happened.",
    ]
    guidance.extend(str(item) for item in safe_bridges[:2])
    if parent.get("blind_spots"):
        guidance.append("Watch for the possibility that care may be received as pressure.")
    return guidance


def _teacher_guidance(teacher: dict[str, Any]) -> list[str]:
    guidance = [
        "Offer classroom support without asking the student to explain private context.",
        "Keep interventions reversible, quiet, and observable.",
        "Escalate to the assigned reviewer if risk increases.",
    ]
    if teacher.get("blind_spots"):
        guidance.append("Treat visible behavior as a signal to support, not as the full explanation.")
    return guidance
