"""Analysis Layer v0.1 tests."""

from __future__ import annotations

from src import analysis_layer


def _sample_corpus() -> analysis_layer.AnalysisCorpus:
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
                    "key_concerns": ["身份焦慮"],
                    "needs_signals": ["需要穩定成人支持"],
                    "do_not_share": ["raw secret should not appear", "信託文件"],
                },
                "parent_input": "我擔心他最近是不是學業壓力太大。",
                "teacher_input": "作業品質還在，但課堂 spark 下降。",
                "analysis": {
                    "whats_really_happening": "學生正在處理信託文件造成的身份焦慮。",
                    "privacy_kept": ["信託文件"],
                    "this_week": {
                        "for_parent": {"do": ["留出低壓對話空間"], "dont": []},
                    },
                    "watch_for": ["是否進一步退縮"],
                    "needs_external_intervention": False,
                },
            }
        },
        dimension_scores={
            "michael": {
                "_source_path": "data/dimension_scores/michael.json",
                "source_type": "synthetic",
                "dimensions": {
                    "identity": {
                        "level": 2,
                        "signals_observed": ["信託文件讓身份焦慮升高"],
                        "reasoning": "身份焦慮影響 agency。",
                    },
                    "emotional_safety": {
                        "level": 1,
                        "signals_observed": ["反芻但無 active ideation"],
                        "reasoning": "維持功能。",
                    },
                },
                "highest_concern_dimension": "identity",
                "cumulative_strain": 3,
            }
        },
    )


def test_case_summary_schema():
    summary = analysis_layer.build_case_summary("michael", _sample_corpus())

    required = {
        "student_id",
        "character_id",
        "source_type",
        "observed_signals",
        "inferred_needs",
        "risk_dimensions",
        "privacy_constraints",
        "party_profiles",
        "coordination_snapshot",
        "recommended_actions",
        "confidence_level",
        "evidence_refs",
        "missing_information",
        "next_watch_signals",
    }

    assert required <= set(summary)
    assert summary["student_id"] == "michael"
    assert summary["character_id"] == "saga_a_michael"
    assert "parent" in summary["coordination_snapshot"]
    assert "teacher" in summary["coordination_snapshot"]


def test_evidence_refs_required_for_major_conclusions():
    summary = analysis_layer.build_case_summary("michael", _sample_corpus())

    assert summary["evidence_refs"]
    for ref in summary["evidence_refs"]:
        assert ref["source"]
        assert ref["source_kind"] in {
            "raw_conversation",
            "abstracted_profile",
            "coordinator_report",
            "dimension_score",
            "triage",
        }
        assert ref["confidence"] in {"low", "medium", "high"}
        assert "synthetic_only" in ref


def test_contradiction_detection_profile_vs_parent_teacher():
    summary = analysis_layer.build_case_summary("michael", _sample_corpus())

    kinds = {item["kind"] for item in summary["contradictions"]}

    assert "perspective_gap" in kinds


def test_synthetic_only_warning_and_no_raw_secret_in_report():
    summary = analysis_layer.build_case_summary("michael", _sample_corpus())
    report = analysis_layer.render_case_report(summary)

    assert summary["synthetic_only_warning"] is True
    assert "synthetic Saga A data only" in report
    assert "raw secret should not appear" not in report
    assert "信託文件" not in report


def test_three_party_snapshot_includes_party_guidance_without_raw_inputs():
    summary = analysis_layer.build_case_summary("michael", _sample_corpus())
    snapshot = summary["coordination_snapshot"]
    rendered = analysis_layer.render_case_report(summary)

    assert snapshot["parent"]["what_they_can_offer"]
    assert snapshot["teacher"]["what_they_can_offer"]
    assert "Three-Party Coordination Snapshot" in rendered
    assert "我擔心他最近是不是學業壓力太大" not in rendered


def test_dimension_level_3_without_external_intervention_is_flagged():
    corpus = _sample_corpus()
    corpus.dimension_scores["michael"]["dimensions"]["emotional_safety"]["level"] = 3

    summary = analysis_layer.build_case_summary("michael", corpus)
    kinds = {item["kind"] for item in summary["contradictions"]}

    assert "dimension_vs_coordinator" in kinds
