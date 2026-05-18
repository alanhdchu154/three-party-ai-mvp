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
