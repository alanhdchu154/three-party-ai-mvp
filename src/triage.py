"""Triage 模組——判斷是否升級到人類介入。

升級類別：
- academic_1on1：學科 1 對 1（→ 杰尼）
- professional_counseling：心理諮商
- crisis_intervention：緊急介入
- none：不需要升級
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from . import dimension_store
from . import llm

ESCALATION_TYPES = {
    "none",
    "academic_1on1",
    "professional_counseling",
    "crisis_intervention",
}
URGENCY_LEVELS = {"low", "medium", "high", "critical"}
_URGENCY_RANK = {"low": 0, "medium": 1, "high": 2, "critical": 3}
_SAFETY_FLAGS = {
    "self_harm_ideation",
    "suicidal_ideation",
    "abuse_signal",
    "severe_bullying",
}
_ACADEMIC_FLAGS = {"academic_collapse"}
_PROFESSIONAL_NEEDS = {"professional_counseling"}
_CRISIS_NEEDS = {"crisis_intervention"}
_ACADEMIC_NEEDS = {"academic_support", "1on1_tutoring"}
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_DIMENSION_DIR = _PROJECT_ROOT / "data" / "dimension_scores"
_DIMENSION_KEYS = {
    "emotional_safety",
    "academic_load",
    "family_dynamics",
    "social_development",
    "identity",
    "financial_pressure",
    "future_planning",
}


def should_escalate(
    profile: dict[str, Any],
    recent_signals: str | None = None,
    *,
    dimension_scores: dict[str, Any] | None = None,
    previous_dimension_scores: list[dict[str, Any]] | None = None,
    student_id: str | None = None,
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

    resolved_student_id = student_id or profile.get("student_id")
    dimension_scores = dimension_scores or _load_dimension_scores(resolved_student_id)
    if previous_dimension_scores is None and resolved_student_id:
        previous_dimension_scores = dimension_store.load_snapshots(resolved_student_id, limit=3)
        if dimension_scores and previous_dimension_scores:
            previous_dimension_scores = [
                item for item in previous_dimension_scores
                if item.get("scored_at") != dimension_scores.get("scored_at")
            ]
    guardrail = _deterministic_guardrail(
        profile,
        dimension_scores=dimension_scores,
        previous_dimension_scores=previous_dimension_scores,
    )

    try:
        result = llm.complete_json(
            system=system,
            messages=[{"role": "user", "content": user_msg}],
            max_tokens=600,
            temperature=0.2,
        )
    except Exception:
        if guardrail:
            return guardrail
        raise

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
    if guardrail:
        result = _apply_guardrail(result, guardrail)
    return result


def _deterministic_guardrail(
    profile: dict[str, Any],
    *,
    dimension_scores: dict[str, Any] | None = None,
    previous_dimension_scores: list[dict[str, Any]] | None = None,
) -> dict[str, Any] | None:
    """Minimum escalation derived from structured safety and strain signals."""
    risk_flags = set(profile.get("risk_flags") or [])
    needs = set(profile.get("needs_signals") or [])
    strain_guardrail = _dimension_guardrail(
        dimension_scores,
        previous_dimension_scores=previous_dimension_scores,
    )

    if needs & _CRISIS_NEEDS:
        return {
            "escalate": True,
            "escalation_type": "crisis_intervention",
            "urgency": "critical",
            "reason": "結構化 profile 已標出危機介入需求。",
            "recommended_action": "立刻交由指定成人依 crisis protocol 接手，不由 AI 單獨處理。",
            "guardrail_applied": True,
        }

    if risk_flags & _SAFETY_FLAGS or needs & _PROFESSIONAL_NEEDS:
        return {
            "escalate": True,
            "escalation_type": "professional_counseling",
            "urgency": "high" if risk_flags & _SAFETY_FLAGS else "medium",
            "reason": "結構化 profile 已標出安全或心理健康風險，不能只停留在 AI 對話層。",
            "recommended_action": "安排成人人工複核，確認是否需要校內輔導或外部專業資源。",
            "guardrail_applied": True,
        }

    if strain_guardrail:
        return strain_guardrail

    if risk_flags & _ACADEMIC_FLAGS or needs & _ACADEMIC_NEEDS:
        return {
            "escalate": True,
            "escalation_type": "academic_1on1",
            "urgency": "medium",
            "reason": "結構化 profile 已標出需要個別化學業支持的訊號。",
            "recommended_action": "安排杰尼或 GIIS 端 1-on-1 學業支持評估。",
            "guardrail_applied": True,
        }

    return None


def _dimension_guardrail(
    scores: dict[str, Any] | None,
    *,
    previous_dimension_scores: list[dict[str, Any]] | None = None,
) -> dict[str, Any] | None:
    if not scores:
        return None

    levels = _dimension_levels(scores)
    if not levels:
        return None

    if levels.get("emotional_safety", 0) >= 3:
        return {
            "escalate": True,
            "escalation_type": "crisis_intervention",
            "urgency": "critical",
            "reason": "七維度評分顯示情緒安全 Level 3，必須立刻升級。",
            "recommended_action": "交由指定成人啟動 crisis protocol，AI 退到輔助角色。",
            "guardrail_applied": True,
            "triage_level": "urgent_escalation",
        }

    if any(level >= 3 for level in levels.values()):
        return {
            "escalate": True,
            "escalation_type": "professional_counseling",
            "urgency": "high",
            "reason": "七維度評分出現 Level 3 紅燈，需人工複核。",
            "recommended_action": "安排人類 reviewer 判斷是否需要校內輔導、外部專業或杰尼 1-on-1。",
            "guardrail_applied": True,
            "triage_level": "human_review",
        }

    persistent_level_2 = _persistent_level_2_dimensions(
        scores,
        previous_dimension_scores=previous_dimension_scores or [],
    )
    if persistent_level_2:
        return {
            "escalate": True,
            "escalation_type": "academic_1on1",
            "urgency": "medium",
            "reason": f"七維度評分顯示 {', '.join(persistent_level_2)} 持續 Level 2，需要人工複核或 1-on-1 支持。",
            "recommended_action": "安排 GIIS/杰尼 端人類 reviewer，看是否進入 1-on-1 支持流程。",
            "guardrail_applied": True,
            "triage_level": "human_review_or_1on1",
        }

    if _worsening_trajectory(scores, previous_dimension_scores or []):
        return {
            "escalate": True,
            "escalation_type": "academic_1on1",
            "urgency": "medium",
            "reason": "七維度評分呈現惡化軌跡，升高一級處理。",
            "recommended_action": "安排短期人工 check-in，確認是否需要杰尼 1-on-1 或校內支持。",
            "guardrail_applied": True,
            "triage_level": "worsening_monitor",
        }

    level_1_count = sum(1 for level in levels.values() if level >= 1)
    if level_1_count >= 3:
        return {
            "escalate": False,
            "escalation_type": "none",
            "urgency": "medium",
            "reason": "七維度評分有三個以上 Level 1，代表 distributed strain，需提高觀察頻率。",
            "recommended_action": "暫不升級，但安排一週內 light check-in 並重新評分。",
            "guardrail_applied": True,
            "triage_level": "monitor_or_light_intervention",
        }

    return None


def _apply_guardrail(result: dict[str, Any], guardrail: dict[str, Any]) -> dict[str, Any]:
    """Ensure LLM output is at least as cautious as the deterministic guardrail."""
    if not guardrail.get("escalate"):
        if result.get("escalate"):
            return result
        return {**result, **guardrail}

    if not result.get("escalate"):
        return {**result, **guardrail}

    if result.get("escalation_type") == "none":
        result["escalation_type"] = guardrail["escalation_type"]
    elif guardrail["escalation_type"] == "crisis_intervention":
        result["escalation_type"] = "crisis_intervention"
    elif result["escalation_type"] == "academic_1on1" and guardrail["escalation_type"] == "professional_counseling":
        result["escalation_type"] = "professional_counseling"

    if _URGENCY_RANK.get(result.get("urgency", "low"), 0) < _URGENCY_RANK[guardrail["urgency"]]:
        result["urgency"] = guardrail["urgency"]

    result["escalate"] = True
    result["guardrail_applied"] = True
    if not result.get("reason"):
        result["reason"] = guardrail["reason"]
    if not result.get("recommended_action"):
        result["recommended_action"] = guardrail["recommended_action"]
    return result


def _load_dimension_scores(student_id: str | None) -> dict[str, Any] | None:
    return dimension_store.load_latest(student_id)


def _dimension_levels(scores: dict[str, Any]) -> dict[str, int]:
    dimensions = scores.get("dimensions") or {}
    levels: dict[str, int] = {}
    for key in _DIMENSION_KEYS:
        value = dimensions.get(key, {})
        try:
            levels[key] = int(value.get("level", 0))
        except (TypeError, ValueError):
            levels[key] = 0
    return levels


def _persistent_level_2_dimensions(
    scores: dict[str, Any],
    *,
    previous_dimension_scores: list[dict[str, Any]],
) -> list[str]:
    current = _dimension_levels(scores)
    persistent: list[str] = []
    for previous in previous_dimension_scores:
        previous_levels = _dimension_levels(previous)
        for dim, level in current.items():
            if level >= 2 and previous_levels.get(dim, 0) >= 2:
                persistent.append(dim)

    trend = str(scores.get("trend_notes") or "")
    if not persistent and any(level >= 2 for level in current.values()):
        if any(marker in trend for marker in ("維持", "連續", "持平", "仍")):
            persistent = [dim for dim, level in current.items() if level >= 2]
    return sorted(set(persistent))


def _worsening_trajectory(
    scores: dict[str, Any],
    previous_dimension_scores: list[dict[str, Any]],
) -> bool:
    current_total = _safe_int(scores.get("cumulative_strain"))
    previous_totals = [_safe_int(item.get("cumulative_strain")) for item in previous_dimension_scores]
    previous_totals = [item for item in previous_totals if item is not None]
    if current_total is not None and previous_totals and current_total > max(previous_totals):
        return True

    trend = str(scores.get("trend_notes") or "")
    return any(marker in trend for marker in ("上升", "升級", "惡化", "worsen", "加深"))


def _safe_int(value: Any) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None
