"""抽象化品質測試。

跑 synthetic dataset 裡的對話，檢查：
- profile 結構完整
- risk_flags 與 metadata 大致對得上
- profile 不包含學生原話（隱私牆）
"""

from __future__ import annotations

import pytest

from src import abstraction
from tests.conftest import needs_api


@needs_api
def test_abstraction_structure(dataset):
    """profile 應該包含所有必要欄位。"""
    conv = dataset["conversations"][0]
    profile = abstraction.extract_profile(conv["turns"])

    for key in abstraction.PROFILE_FIELDS:
        assert key in profile, f"profile 缺欄位：{key}"

    # 型別檢查
    assert isinstance(profile["key_concerns"], list)
    assert isinstance(profile["risk_flags"], list)
    assert isinstance(profile["needs_signals"], list)
    assert isinstance(profile["do_not_share"], list)


@needs_api
@pytest.mark.parametrize("conv_idx", [0, 1])
def test_abstraction_no_raw_quotes(dataset, conv_idx):
    """profile 不應包含學生講過的原句。"""
    if conv_idx >= len(dataset["conversations"]):
        pytest.skip("dataset 對話數不足")
    conv = dataset["conversations"][conv_idx]
    profile = abstraction.extract_profile(conv["turns"])
    leaked = abstraction.validate_no_raw_quotes(profile, conv["turns"])
    assert leaked == [], f"profile 洩漏原話：{leaked}"


@needs_api
def test_abstraction_picks_up_risk_signals(dataset):
    """高風險對話應該至少標到一個 risk_flag。"""
    crisis_convs = [
        c for c in dataset["conversations"]
        if c.get("scenario_type") in ("crisis", "stress_test")
        or c.get("expected_risk_flags")
    ]
    if not crisis_convs:
        pytest.skip("dataset 沒有 crisis 對話")

    conv = crisis_convs[0]
    profile = abstraction.extract_profile(conv["turns"])
    assert profile["risk_flags"], (
        f"crisis 對話沒有抓到任何 risk_flag。"
        f"profile={profile}"
    )


def test_empty_history_returns_defaults():
    """空對話應該回預設值，不該打 API。"""
    profile = abstraction.extract_profile([])
    for key, default in abstraction.PROFILE_FIELDS.items():
        assert profile[key] == default
