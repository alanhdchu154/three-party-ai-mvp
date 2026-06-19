"""Runtime trace privacy audit tests."""

from __future__ import annotations

import json
from pathlib import Path

from scripts import run_runtime_trace_privacy_audit


def test_audience_safe_surface_flags_raw_trace_marker(tmp_path: Path):
    report = tmp_path / "parent_safe.md"
    report.write_text("This summary reveals scenario_seed_id abc123.", encoding="utf-8")

    result = run_runtime_trace_privacy_audit._audit_audience_safe(report, "parent_safe", "michael")

    assert result["status"] == "FAIL"
    assert result["findings"][0]["policy"] == "no_raw_trace_markers"


def test_restricted_surface_requires_synthetic_boundary(tmp_path: Path):
    report = tmp_path / "internal_reviewer.md"
    report.write_text("Restricted reviewer note. Do not reveal raw turns.", encoding="utf-8")

    result = run_runtime_trace_privacy_audit._audit_restricted(report)

    assert result["status"] == "FAIL"
    assert result["findings"][0]["policy"] == "synthetic_boundary_required"


def test_restricted_surface_passes_with_boundary_language(tmp_path: Path):
    report = tmp_path / "internal_reviewer.md"
    report.write_text(
        "Synthetic-only reviewer note. Do not reveal raw turns.",
        encoding="utf-8",
    )

    result = run_runtime_trace_privacy_audit._audit_restricted(report)

    assert result["status"] == "PASS"


def test_audit_log_rejects_raw_payload_keys(tmp_path: Path):
    log = tmp_path / "audit_log.jsonl"
    event = {"timestamp": "now", "event_type": "x", "payload": {"turns": ["raw message"]}}
    log.write_text(json.dumps(event) + "\n", encoding="utf-8")

    result = run_runtime_trace_privacy_audit._audit_log(log)

    assert result["status"] == "FAIL"
    assert result["findings"][0]["policy"] == "metadata_only_payload"


def test_audit_log_allows_metadata_payload(tmp_path: Path):
    log = tmp_path / "audit_log.jsonl"
    event = {"timestamp": "now", "event_type": "x", "payload": {"path": "parent_safe.md"}}
    log.write_text(json.dumps(event) + "\n", encoding="utf-8")

    result = run_runtime_trace_privacy_audit._audit_log(log)

    assert result["status"] == "PASS"


def test_render_markdown_includes_claim_boundary():
    markdown = run_runtime_trace_privacy_audit.render_markdown(
        {
            "generated_at": "now",
            "surfaces_checked": 1,
            "failures": 0,
            "surface_counts": {"audit_log": 1},
            "claim_boundary": "Synthetic boundary.",
            "surfaces": [
                {
                    "path": "data/pilot_runs/x/audit_log.jsonl",
                    "surface_type": "audit_log",
                    "status": "PASS",
                    "findings": [],
                }
            ],
        }
    )

    assert "Synthetic boundary." in markdown
    assert "Failures: `0`" in markdown
