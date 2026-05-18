"""學生對話 agent。

責任：拿學生 system prompt + 對話 history，呼叫 Claude 回傳一段回應。
本模組刻意保持薄——所有 prompt 內容都在 prompts/student_system.txt。
"""

from __future__ import annotations

from typing import Iterable

from . import llm


def chat(message: str, history: Iterable[dict[str, str]] | None = None) -> str:
    """學生丟一句話，回 AI 的回應。

    Args:
        message: 學生這一輪的訊息。
        history: 之前的對話，[{"role": "user"/"assistant", "content": "..."}]。
                 user = 學生；assistant = AI。

    Returns:
        AI 的回應字串。
    """
    system = llm.load_prompt("student_system")
    messages: list[dict[str, str]] = list(history or [])
    messages.append({"role": "user", "content": message})

    return llm.complete(
        system=system,
        messages=messages,
        max_tokens=400,    # 系統 prompt 已限制 3 句，給點 buffer
        temperature=0.8,    # 對話要有自然感，不要太機械
    )
