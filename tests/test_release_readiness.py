"""Release-readiness gate tests."""

from __future__ import annotations

from pathlib import Path

from scripts import run_release_readiness


def test_claim_boundary_scan_allows_negative_limitation_language(tmp_path: Path):
    doc = tmp_path / "README.md"
    doc.write_text(
        "\n".join(
            [
                "## What Is Not Proven",
                "- No real-student validation.",
                "- No clinical validity.",
                "- No deployment readiness for minors.",
                "- No outcome improvement claim.",
            ]
        ),
        encoding="utf-8",
    )

    assert run_release_readiness.scan_claim_boundaries([doc]) == []


def test_claim_boundary_scan_rejects_positive_overclaims(tmp_path: Path):
    doc = tmp_path / "README.md"
    doc.write_text(
        "\n".join(
            [
                "This system is validated for real students.",
                "It is safe for minors.",
                "The pipeline is deployment-ready for schools.",
            ]
        ),
        encoding="utf-8",
    )

    hits = run_release_readiness.scan_claim_boundaries([doc])

    assert [hit["line"] for hit in hits] == [1, 2, 3]


def test_claim_boundary_scan_allows_explicit_unsafe_example(tmp_path: Path):
    doc = tmp_path / "benchmark_datasheet.md"
    doc.write_text(
        "\n".join(
            [
                "Unsafe wording:",
                "",
                "> This system is validated for real students or school deployment.",
            ]
        ),
        encoding="utf-8",
    )

    assert run_release_readiness.scan_claim_boundaries([doc]) == []


def test_secret_scan_rejects_git_visible_api_keys(tmp_path: Path):
    doc = tmp_path / "config.md"
    fake_key = "AI" + "za" + "1234567890ABCDEFGHIJKLMNOP"
    env_name = "GEMINI" + "_API_KEY"
    doc.write_text(f"{env_name}={fake_key}\n", encoding="utf-8")

    hits = run_release_readiness.scan_secret_like_values([doc])

    assert hits
    assert hits[0]["line"] == 1


def test_secret_scan_allows_placeholders(tmp_path: Path):
    doc = tmp_path / ".env.example"
    doc.write_text("GEMINI_API_KEY=<your-key>\nANTHROPIC_API_KEY=sk-ant-...\n", encoding="utf-8")

    assert run_release_readiness.scan_secret_like_values([doc]) == []


def test_evaluate_readiness_passes_expected_v1_metrics():
    readiness = run_release_readiness.evaluate_readiness(
        command_results=[
            run_release_readiness.CommandResult("corpus_audit", ["cmd"], 0, "{}", ""),
            run_release_readiness.CommandResult("baseline_comparison", ["cmd"], 0, "", ""),
        ],
        metrics={
            "corpus": {
                "n_conversations": 348,
                "depth_counts": {"deep": 85, "shallow": 142, "medium": 121},
            },
            "baseline": {
                "sample_size": 11,
                "totals": {
                    "privacy_wall_pipeline": {
                        "raw_quote_leaks": 0,
                        "private_chunk_leaks": 0,
                        "private_key_or_path_hits": 0,
                        "reconstructability_risk_cases": 0,
                        "over_escalation_flags": 0,
                        "under_escalation_flags": 0,
                        "recommendation_without_evidence_flags": 0,
                        "missing_audience_report_cases": 0,
                    }
                },
            },
            "leak_audit": {"reports_checked": 18, "failures": 0},
            "semantic_trace_audit": {"surfaces_checked": 22, "failures": 0},
            "relationship_leak_audit": {"reports_checked": 18, "failures": 0},
            "reviewer_summary": {
                "n_notes": 37,
                "n_artifacts_reviewed": 22,
                "baseline_artifacts": 12,
                "audience_report_artifacts": 3,
                "second_reviewer_artifacts": 15,
            },
        },
        claim_hits=[],
        secret_hits=[],
    )

    assert readiness == {"status": "pass", "failures": []}


def test_evaluate_readiness_fails_privacy_wall_and_reviewer_regression():
    readiness = run_release_readiness.evaluate_readiness(
        command_results=[
            run_release_readiness.CommandResult("corpus_audit", ["cmd"], 0, "{}", ""),
        ],
        metrics={
            "corpus": {
                "n_conversations": 348,
                "depth_counts": {"deep": 85, "shallow": 142, "medium": 121},
            },
            "baseline": {
                "sample_size": 11,
                "totals": {
                    "privacy_wall_pipeline": {
                        "raw_quote_leaks": 0,
                        "private_chunk_leaks": 0,
                        "private_key_or_path_hits": 0,
                        "reconstructability_risk_cases": 1,
                        "over_escalation_flags": 0,
                        "under_escalation_flags": 0,
                        "recommendation_without_evidence_flags": 0,
                        "missing_audience_report_cases": 0,
                    }
                },
            },
            "leak_audit": {"reports_checked": 18, "failures": 0},
            "semantic_trace_audit": {"surfaces_checked": 22, "failures": 0},
            "relationship_leak_audit": {"reports_checked": 18, "failures": 0},
            "reviewer_summary": {
                "n_notes": 21,
                "n_artifacts_reviewed": 22,
                "baseline_artifacts": 12,
                "audience_report_artifacts": 3,
                "second_reviewer_artifacts": 15,
            },
        },
        claim_hits=[{"path": "README.md", "line": 1, "text": "safe for minors"}],
        secret_hits=[],
    )

    assert readiness["status"] == "fail"
    assert "privacy_wall_reconstructability_risk_cases_nonzero" in readiness["failures"]
    assert "reviewer_note_coverage_low" in readiness["failures"]
    assert "positive_public_overclaim_detected" in readiness["failures"]


def test_evaluate_readiness_fails_semantic_trace_and_secret_hits():
    readiness = run_release_readiness.evaluate_readiness(
        command_results=[],
        metrics={
            "corpus": {
                "n_conversations": 348,
                "depth_counts": {"deep": 85, "shallow": 142, "medium": 121},
            },
            "baseline": {
                "sample_size": 11,
                "totals": {
                    "privacy_wall_pipeline": {
                        "raw_quote_leaks": 0,
                        "private_chunk_leaks": 0,
                        "private_key_or_path_hits": 0,
                        "reconstructability_risk_cases": 0,
                        "over_escalation_flags": 0,
                        "under_escalation_flags": 0,
                        "recommendation_without_evidence_flags": 0,
                        "missing_audience_report_cases": 0,
                    }
                },
            },
            "leak_audit": {"reports_checked": 18, "failures": 0},
            "semantic_trace_audit": {"surfaces_checked": 22, "failures": 1},
            "relationship_leak_audit": {"reports_checked": 18, "failures": 0},
            "reviewer_summary": {
                "n_notes": 37,
                "n_artifacts_reviewed": 22,
                "baseline_artifacts": 12,
                "audience_report_artifacts": 3,
                "second_reviewer_artifacts": 15,
            },
        },
        claim_hits=[],
        secret_hits=[{"path": "README.md", "line": 1, "pattern": "secret"}],
    )

    assert readiness["status"] == "fail"
    assert "semantic_trace_failures" in readiness["failures"]
    assert "secret_like_value_detected" in readiness["failures"]


def test_evaluate_readiness_fails_relationship_leak_regression():
    readiness = run_release_readiness.evaluate_readiness(
        command_results=[],
        metrics={
            "corpus": {
                "n_conversations": 348,
                "depth_counts": {"deep": 85, "shallow": 142, "medium": 121},
            },
            "baseline": {
                "sample_size": 11,
                "totals": {
                    "privacy_wall_pipeline": {
                        "raw_quote_leaks": 0,
                        "private_chunk_leaks": 0,
                        "private_key_or_path_hits": 0,
                        "reconstructability_risk_cases": 0,
                        "over_escalation_flags": 0,
                        "under_escalation_flags": 0,
                        "recommendation_without_evidence_flags": 0,
                        "missing_audience_report_cases": 0,
                    }
                },
            },
            "leak_audit": {"reports_checked": 18, "failures": 0},
            "semantic_trace_audit": {"surfaces_checked": 22, "failures": 0},
            "relationship_leak_audit": {"reports_checked": 18, "failures": 1},
            "reviewer_summary": {
                "n_notes": 37,
                "n_artifacts_reviewed": 22,
                "baseline_artifacts": 12,
                "audience_report_artifacts": 3,
                "second_reviewer_artifacts": 15,
            },
        },
        claim_hits=[],
        secret_hits=[],
    )

    assert readiness["status"] == "fail"
    assert "relationship_context_leak_failures" in readiness["failures"]
