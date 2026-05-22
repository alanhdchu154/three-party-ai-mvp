"""Safety infrastructure tests for v0.1 pilot blockers."""

from __future__ import annotations

import json

from src import crisis_handoff, dimension_store, profile_store, source_types, triage


def test_source_type_normalization_and_profile_save(tmp_path, monkeypatch):
    monkeypatch.setattr(profile_store, "PROFILES_DIR", tmp_path)

    assert source_types.normalize_source_type("pilot_real_anonymized") == "pilot_real_anonymized"
    assert source_types.normalize_source_type("unknown") == "synthetic"

    path = profile_store.save_profile("student/../a", {"source_type": "unknown"})
    payload = json.loads(path.read_text(encoding="utf-8"))

    assert payload["student_id"] == "student____a"
    assert payload["source_type"] == "synthetic"


def test_dimension_store_saves_latest_and_snapshots(tmp_path, monkeypatch):
    monkeypatch.setattr(dimension_store, "DIMENSION_DIR", tmp_path)

    scores_v1 = {
        "cumulative_strain": 3,
        "dimensions": {"family_dynamics": {"level": 2}},
    }
    scores_v2 = {
        "cumulative_strain": 4,
        "dimensions": {"family_dynamics": {"level": 2}},
    }

    dimension_store.save_snapshot("saga_a_student", scores_v1, scored_at="2026-05-20T01:00:00Z")
    dimension_store.save_snapshot("saga_a_student", scores_v2, scored_at="2026-05-20T02:00:00Z")

    latest = dimension_store.load_latest("saga_a_student")
    snapshots = dimension_store.load_snapshots("saga_a_student")

    assert latest["cumulative_strain"] == 4
    assert [item["cumulative_strain"] for item in snapshots] == [3, 4]


def test_triage_uses_dimension_snapshots_for_persistence(tmp_path, monkeypatch):
    monkeypatch.setattr(dimension_store, "DIMENSION_DIR", tmp_path)

    def fake_complete_json(**kwargs):
        return {"escalate": False, "escalation_type": "none", "urgency": "low"}

    monkeypatch.setattr(triage.llm, "complete_json", fake_complete_json)
    dimension_store.save_snapshot(
        "student_a",
        {"dimensions": {"family_dynamics": {"level": 2}}},
        scored_at="2026-05-20T01:00:00Z",
    )
    dimension_store.save_snapshot(
        "student_a",
        {"dimensions": {"family_dynamics": {"level": 2}}},
        scored_at="2026-05-20T02:00:00Z",
    )

    result = triage.should_escalate({"student_id": "student_a"})

    assert result["escalate"] is True
    assert result["triage_level"] == "human_review_or_1on1"


def test_crisis_handoff_packet_is_abstract_and_non_sending():
    packet = crisis_handoff.build_handoff_packet(
        student_id="student_a",
        triage_result={
            "escalation_type": "crisis_intervention",
            "urgency": "critical",
            "triage_level": "urgent_escalation",
            "guardrail_applied": True,
            "reason": "Michael 提到信託文件後出現 Level 3。",
            "recommended_action": "人工 review。",
        },
        profile={
            "emotional_state": "high distress",
            "risk_flags": ["suicidal_ideation"],
            "needs_signals": ["crisis_intervention"],
            "do_not_share": ["Michael", "信託文件"],
        },
        dimension_scores={
            "cumulative_strain": 9,
            "highest_concern_dimension": "emotional_safety",
            "dimensions": {"emotional_safety": {"level": 3}},
        },
        reviewer="Alan",
    )
    rendered = json.dumps(packet, ensure_ascii=False)

    assert crisis_handoff.is_crisis_triage(packet["trigger"]) is True
    assert packet["status"] == "needs_human_review"
    assert "Michael" not in rendered
    assert "信託文件" not in rendered
    assert "human_review_required" in packet
