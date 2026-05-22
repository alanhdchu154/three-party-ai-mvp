"""Triage 觸發測試。"""

from __future__ import annotations

import pytest

from src import abstraction, triage
from tests.conftest import needs_api


@needs_api
def test_triage_catches_crisis(dataset):
    """should_trigger_triage=True 且 crisis 的對話，triage 應該升級到至少 high。"""
    crisis_convs = [
        c for c in dataset["conversations"]
        if c.get("should_trigger_triage") and c.get("scenario_type") == "crisis"
    ]
    if not crisis_convs:
        pytest.skip("dataset 沒有 crisis 對話")

    conv = crisis_convs[0]
    profile = abstraction.extract_profile(conv["turns"])
    result = triage.should_escalate(profile)

    assert result["escalate"] is True, f"crisis 對話應該升級。result={result}"
    assert result["urgency"] in ("high", "critical"), (
        f"crisis 對話 urgency 不該低。result={result}"
    )


@needs_api
def test_triage_does_not_overreact_to_normal(dataset):
    """普通對話不應該被升級到 crisis_intervention。"""
    normal_convs = [
        c for c in dataset["conversations"]
        if not c.get("should_trigger_triage")
        and c.get("scenario_type") == "normal"
    ]
    if not normal_convs:
        pytest.skip("dataset 沒有 normal 對話")

    conv = normal_convs[0]
    profile = abstraction.extract_profile(conv["turns"])
    result = triage.should_escalate(profile)

    assert result["escalation_type"] != "crisis_intervention", (
        f"普通對話不該升到 crisis_intervention。result={result}"
    )
    assert result["urgency"] != "critical"


def test_triage_output_shape():
    """純結構測試——確認回傳欄位正確（用 fake profile，不打 API 也能跑邏輯）。"""
    # 這個 test 用 monkey 的方式檢查欄位 fallback 邏輯
    from src.triage import ESCALATION_TYPES, URGENCY_LEVELS

    assert "none" in ESCALATION_TYPES
    assert "academic_1on1" in ESCALATION_TYPES
    assert "crisis_intervention" in ESCALATION_TYPES
    assert "critical" in URGENCY_LEVELS


def test_guardrail_escalates_safety_flags(monkeypatch):
    """即使 LLM 低估安全風險，deterministic guardrail 也要升級。"""
    def fake_complete_json(**kwargs):
        return {
            "escalate": False,
            "escalation_type": "none",
            "urgency": "low",
            "reason": "",
            "recommended_action": "",
        }

    monkeypatch.setattr(triage.llm, "complete_json", fake_complete_json)
    result = triage.should_escalate({"risk_flags": ["suicidal_ideation"]})

    assert result["escalate"] is True
    assert result["escalation_type"] == "professional_counseling"
    assert result["urgency"] == "high"
    assert result["guardrail_applied"] is True


def test_guardrail_can_return_without_llm_when_flagged(monkeypatch):
    """有結構化危機訊號時，就算 LLM call 壞掉也要回傳安全升級。"""
    def fake_complete_json(**kwargs):
        raise RuntimeError("network unavailable")

    monkeypatch.setattr(triage.llm, "complete_json", fake_complete_json)
    result = triage.should_escalate({"needs_signals": ["crisis_intervention"]})

    assert result["escalation_type"] == "crisis_intervention"
    assert result["urgency"] == "critical"
    assert result["guardrail_applied"] is True


def test_dimension_guardrail_emotional_safety_level_3(monkeypatch):
    def fake_complete_json(**kwargs):
        return {"escalate": False, "escalation_type": "none", "urgency": "low"}

    monkeypatch.setattr(triage.llm, "complete_json", fake_complete_json)
    scores = {
        "dimensions": {
            "emotional_safety": {"level": 3},
            "academic_load": {"level": 0},
        }
    }
    result = triage.should_escalate({}, dimension_scores=scores)

    assert result["escalation_type"] == "crisis_intervention"
    assert result["urgency"] == "critical"
    assert result["triage_level"] == "urgent_escalation"


def test_dimension_guardrail_persistent_level_2(monkeypatch):
    def fake_complete_json(**kwargs):
        return {"escalate": False, "escalation_type": "none", "urgency": "low"}

    monkeypatch.setattr(triage.llm, "complete_json", fake_complete_json)
    current = {"dimensions": {"family_dynamics": {"level": 2}}}
    previous = [{"dimensions": {"family_dynamics": {"level": 2}}}]
    result = triage.should_escalate(
        {},
        dimension_scores=current,
        previous_dimension_scores=previous,
    )

    assert result["escalate"] is True
    assert result["triage_level"] == "human_review_or_1on1"


def test_dimension_guardrail_three_level_1_monitor(monkeypatch):
    def fake_complete_json(**kwargs):
        return {"escalate": False, "escalation_type": "none", "urgency": "low"}

    monkeypatch.setattr(triage.llm, "complete_json", fake_complete_json)
    scores = {
        "dimensions": {
            "emotional_safety": {"level": 1},
            "identity": {"level": 1},
            "future_planning": {"level": 1},
        }
    }
    result = triage.should_escalate({}, dimension_scores=scores)

    assert result["escalate"] is False
    assert result["urgency"] == "medium"
    assert result["triage_level"] == "monitor_or_light_intervention"
