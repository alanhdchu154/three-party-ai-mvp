"""學生對話 agent。

責任：拿學生 system prompt + 對話 history，呼叫 Claude 回傳一段回應。
本模組刻意保持薄——所有 prompt 內容都在 prompts/student_system.txt。
"""

from __future__ import annotations

from typing import Any, Iterable

from . import llm


def chat(
    message: str,
    history: Iterable[dict[str, str]] | None = None,
    *,
    context_profile: dict[str, Any] | None = None,
) -> str:
    """學生丟一句話，回 AI 的回應。

    Args:
        message: 學生這一輪的訊息。
        history: 之前的對話，[{"role": "user"/"assistant", "content": "..."}]。
                 user = 學生；assistant = AI。
        context_profile: 已抽象化 profile，用於 continuity。不要放 raw turns。

    Returns:
        AI 的回應字串。
    """
    system = llm.load_prompt("student_system")
    if context_profile:
        system = f"{system}\n\n{_render_context_profile(context_profile)}"
    messages: list[dict[str, str]] = list(history or [])
    messages.append({"role": "user", "content": message})

    return llm.complete(
        system=system,
        messages=messages,
        max_tokens=400,    # 系統 prompt 已限制 3 句，給點 buffer
        temperature=0.8,    # 對話要有自然感，不要太機械
    )


def _render_context_profile(profile: dict[str, Any]) -> str:
    """Render a compact, abstracted continuity context for the student AI.

    This deliberately excludes do_not_share and raw-source fields. The student
    AI may use the context to avoid acting like a blank chatbot, but should not
    recite it as surveillance knowledge.
    """
    student_id = profile.get("student_id") or profile.get("character_id") or "unknown"
    source = profile.get("source_type", "unknown")
    concerns = _items(profile.get("key_concerns"), limit=4)
    needs = _items(profile.get("needs_signals"), limit=4)
    notes = str(profile.get("communication_notes") or "").strip()
    emotional_state = _short(str(profile.get("emotional_state") or "").strip(), 180)

    lines = [
        "# Continuity context",
        "You are continuing a session with an abstracted profile. This is not a raw transcript.",
        f"- Current session/student id: {student_id}",
        f"- Source type: {source}",
    ]
    if emotional_state:
        lines.append(f"- Broad emotional/support context: {emotional_state}")
    if concerns:
        lines.append("- Broad concerns: " + "; ".join(concerns))
    if needs:
        lines.append("- Possible support needs: " + "; ".join(needs))
    if notes:
        lines.append(f"- Communication notes: {_short(notes, 160)}")
    lines.extend([
        "",
        "Use this only for continuity. Do not reveal hidden details, do not quote or reconstruct private events, and do not sound like you are surveilling the student.",
        "If the student asks who they are in this UI, explain the current session label calmly and briefly.",
    ])
    return "\n".join(lines)


def _items(value: Any, *, limit: int) -> list[str]:
    if not isinstance(value, list):
        return []
    return [_short(str(item).strip(), 90) for item in value[:limit] if str(item).strip()]


def _short(text: str, limit: int) -> str:
    return text if len(text) <= limit else text[: limit - 1].rstrip() + "…"
