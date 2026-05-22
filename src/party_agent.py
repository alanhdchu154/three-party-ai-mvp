"""Parent / teacher chat agent.

This module keeps adult-facing live chat symmetrical with the student chat
without changing the privacy contract: live raw turns stay in Streamlit session
memory, while saved party profiles are abstracted separately.
"""

from __future__ import annotations

from typing import Any, Iterable

from . import llm


def chat(
    party: str,
    message: str,
    history: Iterable[dict[str, str]] | None = None,
    *,
    party_profile: dict[str, Any] | None = None,
    student_profile: dict[str, Any] | None = None,
) -> str:
    """Return an adult-facing AI response for a parent or teacher."""
    normalized_party = "teacher" if party == "teacher" else "parent"
    system = llm.load_prompt(f"{normalized_party}_system")
    context = _render_context(
        normalized_party,
        party_profile=party_profile,
        student_profile=student_profile,
    )
    if context:
        system = f"{system}\n\n{context}"

    messages: list[dict[str, str]] = list(history or [])
    messages.append({"role": "user", "content": message})
    return llm.complete(
        system=system,
        messages=messages,
        max_tokens=400,
        temperature=0.7,
    )


def _render_context(
    party: str,
    *,
    party_profile: dict[str, Any] | None,
    student_profile: dict[str, Any] | None,
) -> str:
    lines = [
        "# Privacy-safe continuity context",
        "Use only broad, abstracted context. Do not reveal student secrets, raw quotes, scenario seeds, or another party's private constraints.",
        f"- Current party: {party}",
    ]
    if student_profile:
        emotional = _short(str(student_profile.get("emotional_state") or ""), 140)
        concerns = _items(student_profile.get("key_concerns"), limit=3)
        needs = _items(student_profile.get("needs_signals"), limit=3)
        if emotional:
            lines.append(f"- Broad student support context: {emotional}")
        if concerns:
            lines.append("- Broad student concerns: " + "; ".join(concerns))
        if needs:
            lines.append("- Broad student support needs: " + "; ".join(needs))
    if party_profile:
        concerns = _items(party_profile.get("expressed_concerns"), limit=3)
        needs = _items(party_profile.get("underlying_needs"), limit=3)
        style = _short(str(party_profile.get("communication_style") or ""), 120)
        if concerns:
            lines.append("- Your broad prior concerns: " + "; ".join(concerns))
        if needs:
            lines.append("- Your likely support needs: " + "; ".join(needs))
        if style:
            lines.append(f"- Communication style note: {style}")
    return "\n".join(lines)


def _items(value: Any, *, limit: int) -> list[str]:
    if not isinstance(value, list):
        return []
    return [_short(str(item).strip(), 90) for item in value[:limit] if str(item).strip()]


def _short(text: str, limit: int) -> str:
    return text if len(text) <= limit else text[: limit - 1].rstrip() + "..."
