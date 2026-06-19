"""Semantic trace audit tests."""

from __future__ import annotations

import json
from pathlib import Path

from scripts import run_semantic_trace_audit


def test_tokens_remove_generic_support_words():
    tokens = run_semantic_trace_audit._tokens(
        "Student support report says the parent and teacher need next action."
    )

    assert "student" not in tokens
    assert "support" not in tokens
    assert "parent" not in tokens
    assert "teacher" not in tokens


def test_audit_surface_passes_without_distinctive_private_overlap(tmp_path: Path):
    report = tmp_path / "parent_safe.md"
    report.write_text("Offer a calm weekly support check and keep communication concrete.", encoding="utf-8")

    result = run_semantic_trace_audit._audit_surface(
        {"id": "case_a"},
        "parent_safe",
        report,
        [
            "I hid the blue notebook behind the piano after the scholarship panic call.",
        ],
    )

    assert result["status"] == "PASS"
    assert result["matches"] == []


def test_audit_surface_flags_reconstructable_semantic_trace(tmp_path: Path):
    report = tmp_path / "teacher_safe.md"
    report.write_text(
        "The learner may connect stress to a blue notebook, piano practice, and scholarship panic.",
        encoding="utf-8",
    )

    result = run_semantic_trace_audit._audit_surface(
        {"id": "case_b"},
        "teacher_safe",
        report,
        [
            "I hid the blue notebook behind the piano after the scholarship panic call.",
        ],
    )

    assert result["status"] == "FAIL"
    assert result["reason"] == "semantic_trace_overlap"
    assert result["max_overlap_tokens"] >= 4


def test_render_markdown_includes_claim_boundary():
    markdown = run_semantic_trace_audit.render_markdown(
        {
            "generated_at": "now",
            "sample_size": 1,
            "surfaces_checked": 1,
            "failures": 0,
            "claim_boundary": "Synthetic boundary.",
            "surfaces": [
                {
                    "case_id": "case_a",
                    "audience": "parent_safe",
                    "status": "PASS",
                    "max_overlap_tokens": 0,
                    "max_overlap_ratio": 0,
                    "path": "data/audience_reports/parent_safe/x.md",
                    "matches": [],
                }
            ],
        }
    )

    assert "Synthetic boundary." in markdown
    assert "Failures: `0`" in markdown
