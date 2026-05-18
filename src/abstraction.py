"""抽象化模組——隱私牆。

把學生與 AI 的對話 history 轉成不含原話的 profile JSON。
"""

from __future__ import annotations

import json
from typing import Any, Iterable

from . import llm

# Profile 必須有的欄位（用於 validation 與預設值）
PROFILE_FIELDS: dict[str, Any] = {
    "emotional_state": "",
    "key_concerns": [],
    "risk_flags": [],
    "needs_signals": [],
    "communication_notes": "",
    "what_to_share_with_parent": "",
    "what_to_share_with_teacher": "",
    "do_not_share": [],
}


def _format_history(history: Iterable[dict[str, str]]) -> str:
    """把 history 排版成給 LLM 看的 transcript。"""
    lines = []
    for turn in history:
        role = turn.get("role", "")
        content = turn.get("content", "")
        if role == "user":
            lines.append(f"[學生] {content}")
        elif role == "assistant":
            lines.append(f"[AI] {content}")
    return "\n".join(lines)


def extract_profile(history: Iterable[dict[str, str]]) -> dict[str, Any]:
    """從對話 history 產出抽象化 profile。

    Returns:
        符合 prompts/abstraction.txt 規格的 dict。缺欄位會用預設值補。
    """
    transcript = _format_history(history)
    if not transcript.strip():
        # 空對話直接回預設
        return dict(PROFILE_FIELDS)

    system = llm.load_prompt("abstraction")
    user_msg = (
        "以下是一段學生與 AI 的對話。請按系統提示輸出嚴格 JSON：\n\n"
        f"{transcript}"
    )

    profile = llm.complete_json(
        system=system,
        messages=[{"role": "user", "content": user_msg}],
        max_tokens=1500,
        temperature=0.2,
    )

    # 補齊缺漏欄位，避免下游崩潰
    for key, default in PROFILE_FIELDS.items():
        profile.setdefault(key, default if not isinstance(default, list) else list(default))

    return profile


def validate_no_raw_quotes(
    profile: dict[str, Any], history: Iterable[dict[str, str]], min_len: int = 8
) -> list[str]:
    """檢查 profile 是否意外洩漏學生原話。

    做法：取學生講過的句子（>= min_len 個字），看看是否有任何一句被原樣塞進 profile 字串裡。

    Returns:
        被洩漏的句子清單（空 list 代表通過）。
    """
    leaked: list[str] = []
    profile_blob = json.dumps(profile, ensure_ascii=False)

    for turn in history:
        if turn.get("role") != "user":
            continue
        text = turn.get("content", "").strip()
        if not text:
            continue
        # 切成短句，逐句檢查（避免太長的句子永遠不會被原話 copy）
        for chunk in _split_sentences(text):
            if len(chunk) >= min_len and chunk in profile_blob:
                leaked.append(chunk)
    return leaked


def _split_sentences(text: str) -> list[str]:
    """粗略的中英文句子切分。"""
    import re

    parts = re.split(r"[。！？!?\.\n]+", text)
    return [p.strip() for p in parts if p.strip()]
