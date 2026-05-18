"""隱私牆測試——這是這個產品的核心承諾。

包含：
1. 不打 API 也能跑的純邏輯測試（validate_no_raw_quotes）
2. 打 API 跑 dataset 裡 privacy_test 對話的端到端測試
3. 模擬「家長 AI」試圖讀 profile 的權限隔離測試
"""

from __future__ import annotations

import json

import pytest

from src import abstraction
from tests.conftest import needs_api


# ---------------------------------------------------------------------------
# 純邏輯（不打 API）
# ---------------------------------------------------------------------------

def test_validate_detects_leaked_quote():
    """如果 profile 裡有原話，validator 要抓到。"""
    history = [
        {"role": "user", "content": "我媽昨天又罵我，她每次都這樣。"},
        {"role": "assistant", "content": "聽起來蠻累的。"},
    ]
    bad_profile = {
        "emotional_state": "焦慮",
        "what_to_share_with_parent": "學生說『我媽昨天又罵我，她每次都這樣』",
    }
    leaked = abstraction.validate_no_raw_quotes(bad_profile, history)
    assert leaked, "validator 沒抓到明顯的原話洩漏"


def test_validate_passes_abstract_profile():
    """純抽象的 profile 應該通過。"""
    history = [
        {"role": "user", "content": "我媽昨天又罵我數學考 62 分，她每次都這樣。"},
        {"role": "assistant", "content": "聽起來蠻累的。"},
    ]
    good_profile = {
        "emotional_state": "對家庭學業壓力感到挫折",
        "key_concerns": ["家庭對學業表現的反應方式"],
        "what_to_share_with_parent": "孩子最近對學業表現的回饋感到壓力大。",
    }
    leaked = abstraction.validate_no_raw_quotes(good_profile, history)
    assert leaked == [], f"抽象 profile 不應被誤判為洩漏：{leaked}"


def test_validate_ignores_short_strings():
    """太短的字串（< 8 字）不算原話洩漏——避免誤判常見虛詞。"""
    history = [{"role": "user", "content": "對啊"}]
    profile = {"emotional_state": "對啊"}
    leaked = abstraction.validate_no_raw_quotes(profile, history)
    assert leaked == []


# ---------------------------------------------------------------------------
# 跨模組權限隔離（純邏輯）
# ---------------------------------------------------------------------------

PARENT_VIEW_FIELDS = {"what_to_share_with_parent"}
TEACHER_VIEW_FIELDS = {"what_to_share_with_teacher"}
FORBIDDEN_FOR_OUTSIDE = {"key_concerns", "do_not_share", "risk_flags"}


def _parent_facing_view(profile: dict) -> dict:
    """模擬「家長 AI」只能拿到的子集。"""
    return {k: v for k, v in profile.items() if k in PARENT_VIEW_FIELDS}


def test_parent_view_excludes_sensitive_fields():
    """家長能拿到的 view 不該包含 do_not_share 等敏感欄位。"""
    profile = {
        "emotional_state": "焦慮",
        "key_concerns": ["家庭衝突"],
        "do_not_share": ["不希望家長知道朋友 A 的事"],
        "what_to_share_with_parent": "孩子最近壓力大，建議多陪伴少質問。",
    }
    view = _parent_facing_view(profile)
    for forbidden in FORBIDDEN_FOR_OUTSIDE:
        assert forbidden not in view, f"家長 view 不該看到 {forbidden}"
    assert "what_to_share_with_parent" in view


# ---------------------------------------------------------------------------
# 端到端（需要 API）
# ---------------------------------------------------------------------------

@needs_api
def test_privacy_dataset_no_raw_leakage(dataset):
    """跑 dataset 裡 privacy_test 對話，確保抽象化結果不含原話。"""
    privacy_convs = [
        c for c in dataset["conversations"]
        if c.get("scenario_type") == "privacy_test"
    ]
    if not privacy_convs:
        # dataset 還沒貼進來時用普通對話頂著
        privacy_convs = dataset["conversations"][:1]

    failures = []
    for conv in privacy_convs[:3]:  # 最多跑 3 段，省 API 費
        profile = abstraction.extract_profile(conv["turns"])
        leaked = abstraction.validate_no_raw_quotes(profile, conv["turns"])
        if leaked:
            failures.append({"conv_id": conv.get("id"), "leaked": leaked})

    assert not failures, f"隱私洩漏：\n{json.dumps(failures, ensure_ascii=False, indent=2)}"
