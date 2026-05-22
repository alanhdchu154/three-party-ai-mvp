"""Trajectory & Coordination Models v0.1 tests."""

from __future__ import annotations

from src import analysis_layer, signal_library, trajectory_model


def _corpus_for_student() -> analysis_layer.AnalysisCorpus:
    return analysis_layer.AnalysisCorpus(
        conversations={
            "michael": [
                {"id": "c1", "persona_id": "saga_a_michael", "source_type": "llm_generated"},
                {"id": "c2", "persona_id": "saga_a_michael", "source_type": "llm_generated"},
                {"id": "c3", "persona_id": "saga_a_michael", "source_type": "llm_generated"},
            ]
        },
        analysis_reports={
            "michael": {
                "student": "michael",
                "persona_id": "saga_a_michael",
                "_source_path": "data/analysis_reports/michael_analysis.json",
                "source_type": "synthetic",
                "student_profile": {
                    "needs_signals": ["需要被允許不知道自己想做什麼"],
                    "do_not_share": ["raw private event"],
                },
                "parent_input": "我擔心他是不是學業壓力太大，想一直問他。",
                "teacher_input": "作業質量沒掉，但 spark 不見，舉手次數明顯變少。",
                "analysis": {
                    "whats_really_happening": "學生用炫技與 hypothetical language 掩蓋 autonomy loss。",
                    "privacy_kept": ["raw private event"],
                    "this_week": {"for_parent": {"do": ["降低追問"], "dont": []}},
                },
            }
        },
        dimension_scores={
            "michael": {
                "_source_path": "data/dimension_scores/michael.json",
                "source_type": "synthetic",
                "dimensions": {
                    "academic_load": {"level": 1},
                    "future_planning": {"level": 1},
                    "identity": {"level": 2},
                    "family_dynamics": {"level": 2},
                    "emotional_safety": {"level": 1},
                },
            }
        },
    )


def test_signal_library_contains_required_signals():
    required = {
        "masking_language",
        "disclosure_drop",
        "strategic_compliance",
        "autonomy_loss",
        "parent_monitoring_increase",
        "future_planning_collapse",
        "emotional_flattening",
        "social_withdrawal",
        "perfectionism_pressure",
    }

    assert required <= set(signal_library.list_signals())
    for signal_id in required:
        entry = signal_library.get_signal(signal_id)
        assert entry["description"]
        assert entry["possible_interpretations"]
        assert entry["risk_relevance"]
        assert entry["false_positive_risks"]


def test_signal_detection_finds_expected_patterns():
    corpus = _corpus_for_student()
    context = trajectory_model._case_context("michael", corpus)
    hits = trajectory_model.detect_signals("michael", context)
    hit_ids = {hit["signal_id"] for hit in hits}

    assert "masking_language" in hit_ids
    assert "disclosure_drop" in hit_ids
    assert "autonomy_loss" in hit_ids
    assert "perfectionism_pressure" in hit_ids


def test_trajectory_consistency_schema_and_evidence_refs():
    trajectories = trajectory_model.detect_trajectories("michael", _corpus_for_student())

    burnout = next(item for item in trajectories if item["trajectory_id"] == "burnout_risk")

    assert burnout["trajectory_name"] == "Burnout Risk"
    assert burnout["observed_patterns"]
    assert burnout["contributing_signals"]
    assert burnout["stabilizing_factors"]
    assert burnout["destabilizing_factors"]
    assert burnout["likely_outcomes_if_unchanged"]
    assert burnout["recommended_interventions"]
    assert burnout["confidence"] in {"low", "medium", "high"}
    assert burnout["evidence_refs"]
    assert all(ref["synthetic_only"] is True for ref in burnout["evidence_refs"])


def test_false_positive_protection_with_sparse_evidence():
    corpus = analysis_layer.AnalysisCorpus(
        dimension_scores={
            "quiet_student": {
                "source_type": "synthetic",
                "dimensions": {"academic_load": {"level": 0}},
            }
        }
    )

    trajectories = trajectory_model.detect_trajectories("quiet_student", corpus)

    assert len(trajectories) == 1
    assert trajectories[0]["trajectory_id"] == "insufficient_evidence"
    assert trajectories[0]["confidence"] == "low"


def test_missing_evidence_downgrades_confidence():
    corpus = analysis_layer.AnalysisCorpus(
        analysis_reports={
            "student_a": {
                "student": "student_a",
                "source_type": "synthetic",
                "teacher_input": "spark 不見，舉手次數明顯變少。",
                "analysis": {"whats_really_happening": "可能有 masking language。"},
            }
        }
    )

    trajectories = trajectory_model.detect_trajectories("student_a", corpus)

    assert trajectories[0]["confidence"] in {"low", "medium"}
    assert any("No dimension score" in item for item in trajectories[0]["missing_evidence"])


def test_trajectory_report_is_privacy_safe():
    trajectories = trajectory_model.detect_trajectories("michael", _corpus_for_student())
    report = trajectory_model.render_trajectory_report("michael", trajectories)

    assert "possible risk patterns" in report
    assert "raw private event" not in report
    assert "diagnoses" in report


def test_reviewer_calibration_downgrades_under_evidenced_trajectory():
    trajectories = trajectory_model.detect_trajectories("michael", _corpus_for_student())
    models = {"michael": trajectories}
    review_summary = {
        "artifacts": {
            "trajectory_report:michael:dependency_risk": {
                "calibration_status": "needs_calibration",
                "verdict_counts": {"under_evidenced": 1},
                "confidence_counts": {"medium": 1},
                "reviewers": ["Umi"],
                "action_items": ["Require explicit AI over-reliance evidence."],
            }
        }
    }

    calibrated = trajectory_model.apply_reviewer_calibration(
        models,
        review_summary=review_summary,
    )
    dependency = next(
        item for item in calibrated["michael"]
        if item["trajectory_id"] == "dependency_risk"
    )

    assert dependency["reviewer_calibration"]["status"] == "needs_calibration"
    assert dependency["calibrated_confidence"] == "low"


def test_unreviewed_synthetic_high_confidence_is_downgraded():
    trajectories = trajectory_model.detect_trajectories("michael", _corpus_for_student())
    calibrated = trajectory_model.apply_reviewer_calibration(
        {"michael": trajectories},
        review_summary={"artifacts": {}},
    )
    burnout = next(
        item for item in calibrated["michael"]
        if item["trajectory_id"] == "burnout_risk"
    )

    assert burnout["reviewer_calibration"]["status"] == "not_reviewed"
    assert burnout["confidence"] == "high"
    assert burnout["calibrated_confidence"] == "medium"
