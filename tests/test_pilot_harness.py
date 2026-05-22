"""Controlled pilot harness tests."""

from __future__ import annotations

import json

from src import analysis_layer, audit_log, pilot_harness


def _corpus() -> analysis_layer.AnalysisCorpus:
    return analysis_layer.AnalysisCorpus(
        conversations={
            "michael": [
                {
                    "id": "conv_1",
                    "persona_id": "saga_a_michael",
                    "scenario_seed": "raw secret should not appear",
                    "_source_path": "data/generated_conversations/conv_1.json",
                    "source_type": "llm_generated",
                }
            ]
        },
        analysis_reports={
            "michael": {
                "student": "michael",
                "persona_id": "saga_a_michael",
                "_source_path": "data/analysis_reports/michael_analysis.json",
                "source_type": "synthetic",
                "student_profile": {
                    "needs_signals": ["需要低壓支持"],
                    "do_not_share": ["raw secret should not appear"],
                },
                "teacher_input": "作業質量沒掉，但 spark 不見，舉手次數明顯變少。",
                "analysis": {
                    "whats_really_happening": "學生用 hypothetical language 掩蓋 agency loss。",
                    "privacy_kept": ["raw secret should not appear"],
                    "this_week": {"for_parent": {"do": ["降低追問"], "dont": []}},
                    "watch_for": ["是否進一步退縮"],
                },
            }
        },
        dimension_scores={
            "michael": {
                "_source_path": "data/dimension_scores/michael.json",
                "source_type": "synthetic",
                "dimensions": {
                    "identity": {"level": 2, "signals_observed": ["agency loss"]},
                    "future_planning": {"level": 1, "signals_observed": ["不知道未來"]},
                    "academic_load": {"level": 1, "signals_observed": ["performance pressure"]},
                },
                "highest_concern_dimension": "identity",
            }
        },
    )


def test_controlled_harness_writes_isolated_privacy_safe_run(tmp_path, monkeypatch):
    monkeypatch.setattr(analysis_layer, "load_corpus", lambda: _corpus())
    monkeypatch.setattr(
        pilot_harness.reviewer_workflow,
        "summarize_reviews",
        lambda: {"n_notes": 0, "artifacts": {}},
    )

    run_dir = pilot_harness.run_controlled_harness(
        "michael",
        run_id="test_run",
        output_dir=tmp_path,
    )

    expected = {
        "case_summary.json",
        "internal_reviewer.md",
        "parent_safe.md",
        "teacher_safe.md",
        "trajectory_report.md",
        "reviewer_calibration.json",
        "manifest.json",
        "audit_log.jsonl",
    }
    assert expected <= {path.name for path in run_dir.iterdir()}

    parent_safe = (run_dir / "parent_safe.md").read_text(encoding="utf-8")
    teacher_safe = (run_dir / "teacher_safe.md").read_text(encoding="utf-8")
    assert "raw secret should not appear" not in parent_safe
    assert "raw secret should not appear" not in teacher_safe

    manifest = json.loads((run_dir / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["run_id"] == "test_run"
    assert manifest["student_id"] == "michael"
    assert manifest["synthetic_only_warning"] is True
    assert "manifest.json" in manifest["files"]

    events = audit_log.load_events(run_dir / "audit_log.jsonl")
    assert events[0]["event_type"] == "harness_started"
    assert events[-1]["event_type"] == "harness_completed"
