"""Coordinator 模組。

收三方輸入（學生 profile + 家長 dummy + 老師 dummy），產出協調方案
與分別給三方的訊息。
"""

from __future__ import annotations

import json
from typing import Any

from . import llm


def synthesize(
    student_profile: dict[str, Any],
    parent_input: str,
    teacher_input: str,
) -> dict[str, Any]:
    """合成三方輸入，產出協調方案。

    Args:
        student_profile: abstraction.extract_profile 的輸出
        parent_input: 家長對情況的看法（dummy 字串）
        teacher_input: 老師對情況的看法（dummy 字串）

    Returns: 新 schema（v2）
        {
            "whats_really_happening": str,    # 水面下的診斷
            "who_knows_what": {
                "parent_sees": str,
                "teacher_sees": str,
                "student_knows_alone": str,
            },
            "privacy_kept": [str, ...],       # 系統保護的事項清單
            "this_week": {
                "for_student": {"do": [str], "dont": [str]},
                "for_parent":  {"do": [str], "dont": [str]},
                "for_teacher": {"do": [str], "dont": [str]},
            },
            "watch_for": [str, ...],
            "needs_external_intervention": bool,
        }
    """
    system = llm.load_prompt("coordinator")

    user_msg = (
        "以下是三方輸入：\n\n"
        "## 學生 profile（已抽象化）\n"
        f"{json.dumps(student_profile, ensure_ascii=False, indent=2)}\n\n"
        "## 家長輸入\n"
        f"{parent_input.strip() or '（無輸入）'}\n\n"
        "## 老師輸入\n"
        f"{teacher_input.strip() or '（無輸入）'}\n\n"
        "請按系統提示輸出嚴格 JSON。記得：禁用語清單、specificity 規則、reframe、reverse psychology 優先。"
    )

    plan = llm.complete_json(
        system=system,
        messages=[{"role": "user", "content": user_msg}],
        max_tokens=2500,
        temperature=0.5,
    )

    # 補齊新 schema 欄位
    plan.setdefault("whats_really_happening", "")
    plan.setdefault("who_knows_what", {})
    plan["who_knows_what"].setdefault("parent_sees", "")
    plan["who_knows_what"].setdefault("teacher_sees", "")
    plan["who_knows_what"].setdefault("student_knows_alone", "")
    plan.setdefault("privacy_kept", [])
    plan.setdefault("this_week", {})
    for party in ("for_student", "for_parent", "for_teacher"):
        plan["this_week"].setdefault(party, {})
        plan["this_week"][party].setdefault("do", [])
        plan["this_week"][party].setdefault("dont", [])
    plan.setdefault("watch_for", [])
    plan.setdefault("needs_external_intervention", False)
    return plan
