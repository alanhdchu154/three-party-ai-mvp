"""Coordinator 模組。

收三方輸入（學生 profile + 家長 dummy + 老師 dummy），產出協調方案
與分別給三方的訊息。
"""

from __future__ import annotations

import json
from typing import Any

from . import abstraction, llm


def synthesize(
    student_profile: dict[str, Any],
    parent_input: str | dict[str, Any],
    teacher_input: str | dict[str, Any],
    *,
    parent_profile: dict[str, Any] | None = None,
    teacher_profile: dict[str, Any] | None = None,
    protected_terms: list[str] | None = None,
) -> dict[str, Any]:
    """合成三方輸入，產出協調方案。

    Args:
        student_profile: abstraction.extract_profile 的輸出
        parent_input: 家長對情況的看法（legacy raw/dummy 字串或 profile dict）
        teacher_input: 老師對情況的看法（legacy raw/dummy 字串或 profile dict）
        parent_profile: 已抽象化家長 profile。若未提供，會由 parent_input 正規化。
        teacher_profile: 已抽象化老師 profile。若未提供，會由 teacher_input 正規化。

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
    parent_profile = parent_profile or abstraction.normalize_party_profile(
        "parent",
        parent_input,
        source_type=student_profile.get("source_type", "synthetic"),
    )
    teacher_profile = teacher_profile or abstraction.normalize_party_profile(
        "teacher",
        teacher_input,
        source_type=student_profile.get("source_type", "synthetic"),
    )
    parent_for_coordinator = abstraction.party_profile_view(
        parent_profile,
        audience="internal_reviewer",
    )
    teacher_for_coordinator = abstraction.party_profile_view(
        teacher_profile,
        audience="internal_reviewer",
    )

    user_msg = (
        "以下是三方輸入：\n\n"
        "## 學生 profile（已抽象化）\n"
        f"{json.dumps(student_profile, ensure_ascii=False, indent=2)}\n\n"
        "## 家長 profile（已抽象化）\n"
        f"{json.dumps(parent_for_coordinator, ensure_ascii=False, indent=2)}\n\n"
        "## 老師 profile（已抽象化）\n"
        f"{json.dumps(teacher_for_coordinator, ensure_ascii=False, indent=2)}\n\n"
        "請按系統提示輸出嚴格 JSON。記得：禁用語清單、specificity 規則、reframe、reverse psychology 優先。"
        "三方都可能有不能直接說的擔心；請保護三方各自的 what_not_to_share，但 objective 仍以學生安全與成長為中心。"
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
    plan, audit = abstraction.privacy_rewrite_if_needed(
        plan,
        protected_terms=(
            protected_terms
            or student_profile.get("do_not_share", [])
            + parent_profile.get("what_not_to_share", [])
            + teacher_profile.get("what_not_to_share", [])
        ),
        threshold=0.01,
    )
    if isinstance(plan, dict):
        plan["_privacy_audit"] = abstraction.redact_privacy_audit(audit)
    return plan
