"""Triage 模組——判斷是否升級到人類介入。

升級類別：
- academic_1on1：學科 1 對 1（→ 杰尼）
- professional_counseling：心理諮商
- crisis_intervention：緊急介入
- none：不需要升級
"""

from __future__ import annotations

import json
from typing import Any

from . import llm

ESCALATION_TYPES = {
    "none",
    "academic_1on1",
    "professional_counseling",
    "crisis_intervention",
}
URGENCY_LEVELS = {"low", "medium", "high", "critical"}


def should_escalate(
    profile: dict[str, Any],
    recent_signals: str | None = None,
) -> dict[str, Any]:
    """判斷是否升級。

    Args:
        profile: 學生 profile（abstraction 的輸出）
        recent_signals: 額外的近期觀察（可選；例如「最近三次對話都提到失眠」）

    Returns:
        {
            "escalate": bool,
            "escalation_type": one of ESCALATION_TYPES,
            "urgency": one of URGENCY_LEVELS,
            "reason": str,
            "recommended_action": str
        }
    """
    system = llm.load_prompt("triage")

    user_msg = (
        "以下是學生狀態與訊號：\n\n"
        "## 學生 profile（抽象化）\n"
        f"{json.dumps(profile, ensure_ascii=False, indent=2)}\n\n"
    )
    if recent_signals:
        user_msg += f"## 近期觀察\n{recent_signals.strip()}\n\n"
    user_msg += "請按系統提示輸出嚴格 JSON。"

    result = llm.complete_json(
        system=system,
        messages=[{"role": "user", "content": user_msg}],
        max_tokens=600,
        temperature=0.2,
    )

    # 容錯 + 預設值
    result.setdefault("escalate", False)
    etype = result.get("escalation_type", "none")
    if etype not in ESCALATION_TYPES:
        etype = "none"
    result["escalation_type"] = etype

    urgency = result.get("urgency", "low")
    if urgency not in URGENCY_LEVELS:
        urgency = "low"
    result["urgency"] = urgency

    result.setdefault("reason", "")
    result.setdefault("recommended_action", "")
    return result
