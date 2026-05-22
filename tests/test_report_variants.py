"""Audience-specific report variant tests."""

from __future__ import annotations

import pytest

from src import report_variants


def _summary() -> dict:
    return {
        "student_id": "michael",
        "character_id": "saga_a_michael",
        "source_type": "llm_generated",
        "observed_signals": ["identity Level 2: high-specificity details withheld."],
        "inferred_needs": ["Needs low-pressure adult support."],
        "risk_dimensions": [
            {"dimension": "identity", "level": 2, "evidence_count": 2},
            {"dimension": "emotional_safety", "level": 1, "evidence_count": 1},
        ],
        "privacy_constraints": ["Do not reveal raw turns, scenario seeds, or secret truths."],
        "coordination_snapshot": {
            "parent": {
                "blind_spots": ["may confuse care with pressure"],
                "what_they_can_offer": ["reduce pressure at home"],
            },
            "teacher": {
                "blind_spots": ["may see classroom behavior without home context"],
                "what_they_can_offer": ["offer quiet classroom support"],
            },
            "safe_bridges": ["Parent can support routines without requesting private details."],
        },
        "recommended_actions": ["Human review is justified."],
        "confidence_level": "medium",
        "evidence_refs": [
            {
                "id": "ev_001",
                "student_id": "michael",
                "source": "data/generated_conversations/private.json",
                "source_kind": "raw_conversation",
                "claim": "raw secret should not appear",
                "confidence": "medium",
                "synthetic_only": True,
            }
        ],
        "missing_information": ["No real pilot evidence."],
        "next_watch_signals": ["Watch for disclosure changes."],
        "contradictions": [],
        "synthetic_only_warning": True,
    }


def test_parent_safe_variant_excludes_raw_evidence_claims():
    report = report_variants.render_case_variant(_summary(), "parent_safe")

    assert "raw secret should not appear" not in report
    assert "private.json" not in report
    assert "High-specificity evidence is withheld" in report
    assert "This is not a clinical diagnosis" in report
    assert "reduce pressure at home" in report
    assert "Teacher private constraints are not included" in report


def test_teacher_safe_variant_keeps_dimensions_without_private_details():
    report = report_variants.render_case_variant(_summary(), "teacher_safe")

    assert "`identity` Level 2" in report
    assert "`emotional_safety` Level 1" in report
    assert "raw secret should not appear" not in report
    assert "private family details" in report
    assert "offer quiet classroom support" in report
    assert "Parent private constraints are not included" in report


def test_invalid_audience_rejected():
    with pytest.raises(ValueError):
        report_variants.render_case_variant(_summary(), "grandparent_safe")


def test_generate_case_variant_reports_to_tmp_dir(tmp_path):
    paths = report_variants.generate_case_variant_reports([_summary()], output_dir=tmp_path)

    assert len(paths) == 3
    assert (tmp_path / "parent_safe" / "michael.md").exists()
    assert (tmp_path / "teacher_safe" / "michael.md").exists()
    assert (tmp_path / "internal_reviewer" / "michael.md").exists()
