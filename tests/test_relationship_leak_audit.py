"""Relationship-context leak audit tests."""

from __future__ import annotations

from pathlib import Path

from scripts import run_relationship_leak_audit


def test_contains_term_matches_case_insensitive_phrase():
    assert run_relationship_leak_audit._contains_term(
        "This report mentions Fairness As Distance.",
        "fairness as distance",
    )


def test_audit_report_allows_broad_family_dimension(tmp_path: Path):
    report = tmp_path / "teacher_safe.md"
    report.write_text(
        "Active Dimensions: `family_dynamics` Level 2. Offer quiet support.",
        encoding="utf-8",
    )

    result = run_relationship_leak_audit._audit_report("teacher_safe", "michael", report)

    assert result["status"] == "PASS"
    assert result["matches"] == []


def test_audit_report_flags_reconstructable_relationship_marker(tmp_path: Path):
    report = tmp_path / "parent_safe.md"
    report.write_text(
        "The student may experience fairness as distance in the family.",
        encoding="utf-8",
    )

    result = run_relationship_leak_audit._audit_report("parent_safe", "michael", report)

    assert result["status"] == "FAIL"
    assert result["reason"] == "relationship_context_leak"
    assert result["matches"][0]["marker_id"] == "conditional_belonging"


def test_render_markdown_includes_claim_boundary():
    markdown = run_relationship_leak_audit.render_markdown(
        {
            "generated_at": "now",
            "reports_checked": 1,
            "failures": 0,
            "claim_boundary": "Synthetic boundary.",
            "reports": [
                {
                    "audience": "parent_safe",
                    "persona": "michael",
                    "status": "PASS",
                    "path": "data/audience_reports/parent_safe/michael.md",
                    "matches": [],
                }
            ],
        }
    )

    assert "Synthetic boundary." in markdown
    assert "Failures: `0`" in markdown
