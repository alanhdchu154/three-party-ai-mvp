"""Crisis handoff packet creation.

This module intentionally does not send notifications or contact external
services. It only creates the minimum abstract packet a human reviewer needs.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from . import abstraction


def is_crisis_triage(result: dict[str, Any]) -> bool:
    return (
        result.get("escalation_type") == "crisis_intervention"
        or result.get("urgency") == "critical"
        or result.get("triage_level") == "urgent_escalation"
    )


def build_handoff_packet(
    *,
    student_id: str,
    triage_result: dict[str, Any],
    profile: dict[str, Any] | None = None,
    dimension_scores: dict[str, Any] | None = None,
    reviewer: str = "unassigned",
) -> dict[str, Any]:
    """Create a non-verbatim crisis handoff packet for human review."""
    profile = profile or {}
    dimension_scores = dimension_scores or {}
    packet = {
        "student_id": student_id,
        "created_at": datetime.utcnow().isoformat() + "Z",
        "reviewer": reviewer,
        "status": "needs_human_review",
        "trigger": {
            "escalation_type": triage_result.get("escalation_type", "none"),
            "urgency": triage_result.get("urgency", "low"),
            "triage_level": triage_result.get("triage_level", ""),
            "guardrail_applied": bool(triage_result.get("guardrail_applied")),
        },
        "abstract_concern": triage_result.get("reason", ""),
        "recommended_human_action": triage_result.get("recommended_action", ""),
        "dimension_summary": _dimension_summary(dimension_scores),
        "profile_summary": {
            "emotional_state": profile.get("emotional_state", ""),
            "risk_flags": list(profile.get("risk_flags") or []),
            "needs_signals": list(profile.get("needs_signals") or []),
        },
        "ai_must_stop": [
            "Do not continue ordinary coaching or tutoring.",
            "Do not promise unlimited confidentiality.",
            "Do not ask for more sensitive details for analysis.",
            "Do not expose raw student statements to parents, teachers, or tutors.",
        ],
        "human_review_required": [
            "Confirm immediate safety and reachability.",
            "Review abstract profile and dimension scores.",
            "Decide parent/guardian, school counselor, external professional, or emergency escalation.",
            "Document minimum necessary action taken.",
        ],
    }
    return abstraction.sanitize_for_privacy(packet, protected_terms=profile.get("do_not_share", []))


def _dimension_summary(scores: dict[str, Any]) -> dict[str, Any]:
    dimensions = scores.get("dimensions") or {}
    levels: dict[str, int] = {}
    for key, value in dimensions.items():
        try:
            levels[key] = int(value.get("level", 0))
        except (AttributeError, TypeError, ValueError):
            levels[key] = 0
    return {
        "cumulative_strain": scores.get("cumulative_strain"),
        "highest_concern_dimension": scores.get("highest_concern_dimension", ""),
        "levels": levels,
        "trend_notes": scores.get("trend_notes", ""),
    }

