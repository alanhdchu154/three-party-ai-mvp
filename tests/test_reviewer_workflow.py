"""Reviewer workflow tests."""

from __future__ import annotations

import json

import pytest

from src import reviewer_workflow


def test_build_review_note_schema_and_privacy_sanitization():
    note = reviewer_workflow.build_review_note(
        artifact_type="trajectory_report",
        artifact_id="michael:burnout_risk",
        reviewer="Umi",
        verdict="under_evidenced",
        confidence="medium",
        evidence_ref_ids=["traj_ev_001"],
        comments="Michael raw private event should not appear.",
        privacy_concerns=["raw private event"],
        action_items=["Need human calibration before pilot."],
        protected_terms=["Michael", "raw private event"],
    )
    rendered = json.dumps(note, ensure_ascii=False)

    assert note["artifact_type"] == "trajectory_report"
    assert note["artifact_id"] == "michael:burnout_risk"
    assert note["verdict"] == "under_evidenced"
    assert "Michael" not in rendered
    assert "raw private event" not in rendered


def test_invalid_review_note_rejected():
    with pytest.raises(ValueError):
        reviewer_workflow.build_review_note(
            artifact_type="unknown",
            artifact_id="michael",
            reviewer="Umi",
            verdict="agree",
        )

    with pytest.raises(ValueError):
        reviewer_workflow.build_review_note(
            artifact_type="case_summary",
            artifact_id="michael",
            reviewer="Umi",
            verdict="certain_diagnosis",
        )


def test_save_load_and_summarize_reviews(tmp_path):
    note_1 = reviewer_workflow.build_review_note(
        artifact_type="case_summary",
        artifact_id="michael",
        reviewer="Alan",
        verdict="agree",
        confidence="high",
        action_items=["Keep action reversible."],
    )
    note_2 = reviewer_workflow.build_review_note(
        artifact_type="case_summary",
        artifact_id="michael",
        reviewer="Umi",
        verdict="privacy_concern",
        confidence="medium",
        privacy_concerns=["One action feels too specific."],
    )

    reviewer_workflow.save_review_note(note_1, notes_dir=tmp_path)
    reviewer_workflow.save_review_note(note_2, notes_dir=tmp_path)
    notes = reviewer_workflow.load_review_notes(tmp_path)
    summary = reviewer_workflow.summarize_reviews(notes)

    artifact = summary["artifacts"]["case_summary:michael"]
    assert summary["n_notes"] == 2
    assert artifact["verdict_counts"]["agree"] == 1
    assert artifact["verdict_counts"]["privacy_concern"] == 1
    assert artifact["calibration_status"] == "privacy_review_needed"


def test_generate_empty_reviewer_summary(tmp_path):
    output = tmp_path / "out"

    path = reviewer_workflow.generate_reviewer_summary(
        notes_dir=tmp_path / "missing",
        output_dir=output,
    )
    rendered = path.read_text(encoding="utf-8")

    assert "No Reviews Yet" in rendered
    assert "synthetic data into real pilot validation" in rendered

