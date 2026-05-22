"""Human-readable signal library for trajectory modeling v0.1."""

from __future__ import annotations

from typing import Any

SIGNAL_LIBRARY: dict[str, dict[str, Any]] = {
    "masking_language": {
        "description": "Student uses intellectualized, joking, vague, or performative language to avoid direct disclosure.",
        "possible_interpretations": [
            "Protective self-presentation",
            "Fear of being judged",
            "Habitual communication style",
        ],
        "risk_relevance": "Can hide worsening strain behind apparently functional conversation.",
        "false_positive_risks": "Some students naturally use humor or abstract language without increased risk.",
    },
    "disclosure_drop": {
        "description": "Student shares less over time, becomes shorter, or avoids previously open topics.",
        "possible_interpretations": [
            "Trust erosion",
            "Fatigue with the tool",
            "Temporary busy period",
        ],
        "risk_relevance": "Can indicate loss of the AI as a truth-hearing channel.",
        "false_positive_risks": "May reflect schedule changes or fewer triggering events.",
    },
    "strategic_compliance": {
        "description": "Student appears compliant while privately disengaging or withholding real preference.",
        "possible_interpretations": [
            "Conflict avoidance",
            "Family pressure management",
            "Short-term pragmatic coping",
        ],
        "risk_relevance": "Can make adults overestimate stability.",
        "false_positive_risks": "Some compliance is healthy cooperation, not hidden disengagement.",
    },
    "autonomy_loss": {
        "description": "Student has difficulty naming personal wants outside external expectations.",
        "possible_interpretations": [
            "Identity strain",
            "Overcontrolled environment",
            "Normal adolescent uncertainty",
        ],
        "risk_relevance": "Relevant to disengagement, burnout, and future-planning collapse.",
        "false_positive_risks": "Uncertainty about future plans is developmentally common.",
    },
    "parent_monitoring_increase": {
        "description": "Parent or guardian increases checking, pressure, surveillance, or corrective questioning.",
        "possible_interpretations": [
            "Caregiver anxiety",
            "Escalating control loop",
            "Appropriate concern after a concrete risk signal",
        ],
        "risk_relevance": "Can reduce student disclosure if experienced as interrogation.",
        "false_positive_risks": "Some monitoring is protective when there is real safety risk.",
    },
    "future_planning_collapse": {
        "description": "Student cannot describe a future path, goal, or reason for continuing current effort.",
        "possible_interpretations": [
            "Burnout risk",
            "Identity exploration",
            "Mismatch between student values and imposed pathway",
        ],
        "risk_relevance": "Can precede disengagement or sharper escalation if combined with emotional safety signals.",
        "false_positive_risks": "May be a temporary reflective pause rather than collapse.",
    },
    "emotional_flattening": {
        "description": "Student remains functional but shows reduced spark, affect, or responsiveness.",
        "possible_interpretations": [
            "Emotional fatigue",
            "Protective shutdown",
            "Normal low-energy week",
        ],
        "risk_relevance": "Can signal hidden strain when external performance remains stable.",
        "false_positive_risks": "Sleep, workload, or ordinary mood variation can look similar.",
    },
    "social_withdrawal": {
        "description": "Student reduces peer/family contact, avoids eye contact, or retreats from normal interaction.",
        "possible_interpretations": [
            "Trust erosion",
            "Social threat perception",
            "Need for recovery space",
        ],
        "risk_relevance": "Relevant to disclosure collapse and emotional safety monitoring.",
        "false_positive_risks": "Some withdrawal is healthy boundary-setting.",
    },
    "perfectionism_pressure": {
        "description": "Student links worth, belonging, or safety to performance and achievement.",
        "possible_interpretations": [
            "Burnout risk",
            "Family expectation pressure",
            "High standards without impairment",
        ],
        "risk_relevance": "Can maintain outward success while increasing internal strain.",
        "false_positive_risks": "Achievement focus is not always harmful.",
    },
}


def get_signal(signal_id: str) -> dict[str, Any]:
    return SIGNAL_LIBRARY[signal_id]


def list_signals() -> list[str]:
    return sorted(SIGNAL_LIBRARY)

