"""抽象化模組——隱私牆。

把學生與 AI 的對話 history 轉成不含原話的 profile JSON。
"""

from __future__ import annotations

import json
import re
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

PARTY_PROFILE_FIELDS: dict[str, Any] = {
    "party": "",
    "role_context": "",
    "expressed_concerns": [],
    "underlying_needs": [],
    "fears_or_constraints": [],
    "communication_style": "",
    "blind_spots": [],
    "what_they_can_offer": [],
    "safe_summary_for_coordinator": "",
    "what_not_to_share": [],
    "confidence_level": "low",
}

_SAGA_ENTITY_TERMS = {
    "Michael",
    "Rachel",
    "Alan",
    "GIIS",
    "Jieni",
    "杰尼",
    "沈又",
    "沈媽",
    "可兒",
    "大伯",
    "後爸",
    "Michael 媽",
    "Steam",
    "Discord",
    "UCLA",
    "NYU",
    "Stern",
    "LSE",
    "印刻",
}
_SENSITIVE_KEYS = {
    "turns",
    "secret_truth",
    "scenario_seed",
    "scenario_seed_id",
    "raw_conversation",
    "transcript",
}
_ABSTRACT_REPLACEMENT = "某個具體細節"
_INDIRECT_IDENTITY_PATTERNS = (
    r"唯一[^，。！？!?]{0,24}(?:學生|孩子|轉學生|繼子|女兒|兒子)",
    r"only [^,.!?]{0,40}(?:student|child|transfer student|stepson|daughter|son)",
    r"the student whose [^,.!?]{8,80}",
)


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

    profile, audit = privacy_rewrite_if_needed(profile, history)
    if isinstance(profile, dict):
        profile["_privacy_audit"] = redact_privacy_audit(audit)
    return profile


def normalize_party_profile(
    party: str,
    payload: dict[str, Any] | str | None,
    *,
    source_type: str = "synthetic",
) -> dict[str, Any]:
    """Normalize parent/teacher/other adult input into a party profile.

    This is intentionally deterministic and conservative. If the caller only
    has raw text, the profile captures that text as an input summary for the
    coordinator, but does not pretend to infer hidden psychology. Richer
    parent/teacher AI abstraction can fill the same schema later.
    """
    profile = dict(PARTY_PROFILE_FIELDS)
    profile["party"] = party
    profile["source_type"] = source_type
    if isinstance(payload, dict):
        for key, default in PARTY_PROFILE_FIELDS.items():
            value = payload.get(key, default)
            profile[key] = value if not isinstance(default, list) else list(value or [])
        profile["party"] = str(profile.get("party") or party)
        profile["source_type"] = payload.get("source_type", source_type)
    elif isinstance(payload, str) and payload.strip():
        text = payload.strip()
        profile["role_context"] = f"{party} input"
        profile["expressed_concerns"] = [text]
        profile["safe_summary_for_coordinator"] = text
        profile["confidence_level"] = "low"

    profile["confidence_level"] = (
        profile["confidence_level"]
        if profile["confidence_level"] in {"low", "medium", "high"}
        else "low"
    )
    return profile


def extract_party_profile(
    party: str,
    history: Iterable[dict[str, str]],
    *,
    source_type: str = "pilot",
) -> dict[str, Any]:
    """Create a privacy-safe party profile from live parent/teacher turns.

    This deterministic baseline deliberately avoids storing raw turns. It
    records broad categories and support constraints only, so parent/teacher
    self-disclosure gets the same privacy posture as student abstraction even
    before a richer LLM abstraction prompt exists.
    """
    user_turns = [
        str(turn.get("content", "")).strip()
        for turn in history
        if turn.get("role") == "user" and str(turn.get("content", "")).strip()
    ]
    profile = dict(PARTY_PROFILE_FIELDS)
    profile.update(
        {
            "party": party,
            "role_context": f"{party} live AI conversation",
            "source_type": source_type,
            "confidence_level": "low",
        }
    )
    if not user_turns:
        return profile

    joined = " ".join(user_turns).lower()
    concerns = _party_signal_categories(joined)
    profile["expressed_concerns"] = concerns or ["general support concern"]
    profile["underlying_needs"] = _party_needs_for(party, concerns)
    profile["fears_or_constraints"] = _party_constraints(joined)
    profile["communication_style"] = _party_communication_style(user_turns)
    profile["blind_spots"] = _party_blind_spots(party, concerns)
    profile["what_they_can_offer"] = _party_support_offers(party, concerns)
    profile["safe_summary_for_coordinator"] = _party_safe_summary(
        party, profile["expressed_concerns"], profile["underlying_needs"]
    )
    profile["what_not_to_share"] = []
    profile["confidence_level"] = "medium" if len(user_turns) >= 3 else "low"
    return profile


def extract_party_profile_llm(
    party: str,
    history: Iterable[dict[str, str]],
    *,
    source_type: str = "pilot",
    protected_terms: Iterable[str] | None = None,
) -> dict[str, Any]:
    """Extract parent/teacher profile with an LLM, then audit and sanitize.

    If the model is unavailable or returns risky output, callers may fall back
    to `extract_party_profile`. This function itself sanitizes high-risk model
    output before returning a profile.
    """
    party = "teacher" if party == "teacher" else "parent"
    history = list(history)
    transcript = _format_party_history(party, history)
    if not transcript.strip():
        return normalize_party_profile(party, None, source_type=source_type)

    prompt_name = "teacher_abstraction" if party == "teacher" else "parent_abstraction"
    profile = llm.complete_json(
        system=llm.load_prompt(prompt_name),
        messages=[
            {
                "role": "user",
                "content": (
                    f"以下是一段 {party} 與 AI 的對話。請按系統提示輸出嚴格 JSON。\n\n"
                    f"{transcript}"
                ),
            }
        ],
        max_tokens=1400,
        temperature=0.2,
    )
    profile = normalize_party_profile(party, profile, source_type=source_type)

    audit = audit_privacy_leakage(
        profile,
        history,
        protected_terms=list(protected_terms or []) + profile.get("what_not_to_share", []),
    )
    if audit.get("needs_rewrite") or audit.get("entity_hits"):
        audit["needs_rewrite"] = True
        profile = sanitize_for_privacy(
            profile,
            protected_terms=list(protected_terms or []) + profile.get("what_not_to_share", []),
        )
        profile = normalize_party_profile(party, profile, source_type=source_type)
    profile["_privacy_audit"] = redact_privacy_audit(audit)
    return profile


def extract_party_profile_with_fallback(
    party: str,
    history: Iterable[dict[str, str]],
    *,
    source_type: str = "pilot",
    protected_terms: Iterable[str] | None = None,
    use_llm: bool = True,
) -> dict[str, Any]:
    """Extract a party profile with optional LLM upgrade and deterministic fallback."""
    history = list(history)
    if use_llm:
        try:
            return extract_party_profile_llm(
                party,
                history,
                source_type=source_type,
                protected_terms=protected_terms,
            )
        except Exception:  # noqa: BLE001 - fallback is intentional for local/offline mode.
            pass
    return extract_party_profile(party, history, source_type=source_type)


def _format_party_history(party: str, history: Iterable[dict[str, str]]) -> str:
    speaker = "老師" if party == "teacher" else "家長"
    lines = []
    for turn in history:
        role = turn.get("role", "")
        content = str(turn.get("content", "")).strip()
        if not content:
            continue
        if role == "user":
            lines.append(f"[{speaker}] {content}")
        elif role == "assistant":
            lines.append(f"[AI] {content}")
    return "\n".join(lines)


def _party_signal_categories(text: str) -> list[str]:
    signals: list[str] = []
    checks = [
        ("academic progress or workload concern", ("grade", "homework", "exam", "study", "學", "成績", "考", "作業")),
        ("communication or trust concern", ("talk", "listen", "secret", "hide", "溝通", "不說", "不讀", "關上", "秘密", "信任")),
        ("family pressure or conflict", ("parent", "family", "argue", "家", "父", "母", "吵", "壓力")),
        ("motivation or disengagement concern", ("motivation", "avoid", "quit", "absent", "動力", "逃", "放棄", "缺席")),
        ("wellbeing or emotional concern", ("sleep", "cry", "anxious", "sad", "睡", "哭", "焦慮", "難過")),
        ("coordination or logistics need", ("schedule", "meeting", "message", "安排", "會議", "時間", "通知")),
    ]
    for label, keywords in checks:
        if any(keyword in text for keyword in keywords):
            signals.append(label)
    return signals


def _party_needs_for(party: str, concerns: list[str]) -> list[str]:
    needs = ["clear, privacy-safe guidance from the coordinator"]
    if "parent" in party:
        needs.append("support understanding the student without pressuring for secrets")
    if "teacher" in party:
        needs.append("classroom guidance that does not expose private disclosures")
    if any("communication" in concern for concern in concerns):
        needs.append("help repairing trust and reducing interrogation dynamics")
    if any("academic" in concern for concern in concerns):
        needs.append("concrete academic support plan with realistic workload")
    return needs


def _party_constraints(text: str) -> list[str]:
    constraints = []
    if any(word in text for word in ("worry", "afraid", "怕", "擔心", "焦慮")):
        constraints.append("may be acting from worry or fear")
    if any(word in text for word in ("time", "busy", "工作", "忙", "時間")):
        constraints.append("limited time or attention bandwidth")
    if any(word in text for word in ("complain", "投訴", "責怪", "blame")):
        constraints.append("concern about being blamed or judged")
    return constraints


def _party_communication_style(user_turns: list[str]) -> str:
    text = " ".join(user_turns)
    if text.count("?") + text.count("？") >= 2:
        return "question-heavy, seeking certainty"
    if len(text) / max(len(user_turns), 1) > 160:
        return "detailed and narrative"
    return "brief and practical"


def _party_blind_spots(party: str, concerns: list[str]) -> list[str]:
    blind_spots = []
    if "parent" in party:
        blind_spots.append("may confuse care with pressure if guidance is too direct")
    if "teacher" in party:
        blind_spots.append("may see classroom behavior without the full home context")
    if any("academic" in concern for concern in concerns):
        blind_spots.append("academic signals may be symptoms rather than root cause")
    return blind_spots


def _party_support_offers(party: str, concerns: list[str]) -> list[str]:
    offers = []
    if "parent" in party:
        offers.extend(["reduce pressure at home", "support routines and emotional safety"])
    elif "teacher" in party:
        offers.extend(["adjust classroom communication", "observe changes over time"])
    else:
        offers.append("provide contextual observations")
    if any("academic" in concern for concern in concerns):
        offers.append("help coordinate realistic academic next steps")
    return offers


def _party_safe_summary(party: str, concerns: list[str], needs: list[str]) -> str:
    concern_text = ", ".join(concerns[:3]) if concerns else "general support concerns"
    need_text = ", ".join(needs[:2]) if needs else "privacy-safe coordination"
    return f"{party} is raising {concern_text}; likely needs {need_text}."


def party_profile_view(profile: dict[str, Any], *, audience: str) -> dict[str, Any]:
    """Return the safe subset of a party profile for another audience.

    `what_not_to_share` is never exposed outside internal reviewer context.
    """
    allowed = {
        "party",
        "role_context",
        "expressed_concerns",
        "underlying_needs",
        "fears_or_constraints",
        "communication_style",
        "blind_spots",
        "what_they_can_offer",
        "safe_summary_for_coordinator",
        "confidence_level",
        "source_type",
    }
    if audience == "internal_reviewer":
        allowed = allowed | {"what_not_to_share"}
    return {key: value for key, value in profile.items() if key in allowed}


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


def audit_privacy_leakage(
    payload: Any,
    history: Iterable[dict[str, str]] | None = None,
    protected_terms: Iterable[str] | None = None,
    *,
    min_len: int = 8,
) -> dict[str, Any]:
    """Run Privacy Wall v2 checks on a profile/coordinator payload.

    This is a conservative, deterministic audit. It catches verbatim snippets,
    named entities, numbers/proper nouns, and highly reconstructable event
    descriptions. It does not replace human review for pilot launch.
    """
    text = _payload_to_text(payload)
    history = list(history or [])
    terms = _collect_protected_terms(history, protected_terms)

    raw_quotes = validate_no_raw_quotes(payload if isinstance(payload, dict) else {"payload": payload}, history, min_len=min_len)
    entity_hits = sorted({term for term in terms if term and term in text})
    numeric_hits = sorted(set(re.findall(r"\b\d+(?:[.,]\d+)?\b", text)))
    event_hits = _detect_event_level_hits(text, history, terms, min_len=min_len)
    indirect_identity_hits = _detect_indirect_identity_hits(text)
    paraphrase_hits = _detect_paraphrase_hits(text, history, min_len=min_len)

    score = reconstructability_score(
        raw_quotes=raw_quotes,
        entity_hits=entity_hits,
        event_hits=event_hits,
        numeric_hits=numeric_hits,
        indirect_identity_hits=indirect_identity_hits,
        paraphrase_hits=paraphrase_hits,
    )
    return {
        "raw_quote_hits": raw_quotes,
        "entity_hits": entity_hits,
        "event_hits": event_hits,
        "numeric_hits": numeric_hits,
        "indirect_identity_hits": indirect_identity_hits,
        "paraphrase_hits": paraphrase_hits,
        "reconstructability_score": score,
        "risk_level": _risk_level(score),
        "needs_rewrite": score >= 0.35,
    }


def reconstructability_score(
    *,
    raw_quotes: list[str] | None = None,
    entity_hits: list[str] | None = None,
    event_hits: list[str] | None = None,
    numeric_hits: list[str] | None = None,
    indirect_identity_hits: list[str] | None = None,
    paraphrase_hits: list[str] | None = None,
) -> float:
    """Score how easy it is to reconstruct the private source from an output."""
    raw_quotes = raw_quotes or []
    entity_hits = entity_hits or []
    event_hits = event_hits or []
    numeric_hits = numeric_hits or []
    indirect_identity_hits = indirect_identity_hits or []
    paraphrase_hits = paraphrase_hits or []
    score = 0.0
    score += min(len(raw_quotes), 3) * 0.30
    score += min(len(event_hits), 3) * 0.22
    score += min(len(paraphrase_hits), 3) * 0.35
    score += min(len(indirect_identity_hits), 3) * 0.16
    score += min(len(entity_hits), 6) * 0.07
    score += min(len(numeric_hits), 4) * 0.04
    return round(min(score, 1.0), 2)


def sanitize_for_privacy(
    payload: Any,
    history: Iterable[dict[str, str]] | None = None,
    protected_terms: Iterable[str] | None = None,
) -> Any:
    """Rewrite a payload into a safer abstract form for demo/pilot surfaces."""
    terms = _collect_protected_terms(list(history or []), protected_terms)
    return _sanitize_value(payload, terms)


def privacy_rewrite_if_needed(
    payload: Any,
    history: Iterable[dict[str, str]] | None = None,
    protected_terms: Iterable[str] | None = None,
    *,
    threshold: float = 0.35,
) -> tuple[Any, dict[str, Any]]:
    """Return a sanitized payload when the deterministic audit is too risky."""
    audit = audit_privacy_leakage(payload, history, protected_terms)
    if audit["reconstructability_score"] >= threshold:
        audit = {**audit, "needs_rewrite": True}
        return sanitize_for_privacy(payload, history, protected_terms), audit
    return payload, audit


def redact_privacy_audit(audit: dict[str, Any]) -> dict[str, Any]:
    """Keep audit metadata without leaking the sensitive hit strings."""
    redacted: dict[str, Any] = {
        "reconstructability_score": audit.get("reconstructability_score", 0),
        "risk_level": audit.get("risk_level", "none"),
        "needs_rewrite": audit.get("needs_rewrite", False),
    }
    for key in (
        "raw_quote_hits",
        "entity_hits",
        "event_hits",
        "numeric_hits",
        "indirect_identity_hits",
        "paraphrase_hits",
    ):
        redacted[f"{key}_count"] = len(audit.get(key) or [])
    return redacted


def _split_sentences(text: str) -> list[str]:
    """粗略的中英文句子切分。"""
    parts = re.split(r"[。！？!?\.\n]+", text)
    return [p.strip() for p in parts if p.strip()]


def _payload_to_text(payload: Any) -> str:
    if isinstance(payload, str):
        return payload
    return json.dumps(payload, ensure_ascii=False, sort_keys=True)


def _collect_protected_terms(
    history: Iterable[dict[str, str]], protected_terms: Iterable[str] | None
) -> set[str]:
    terms = {t.strip() for t in (protected_terms or []) if t and len(t.strip()) >= 2}
    terms.update(_SAGA_ENTITY_TERMS)
    for turn in history:
        if turn.get("role") != "user":
            continue
        text = turn.get("content", "")
        terms.update(_extract_sensitive_terms(text))
    return {t for t in terms if len(t) >= 2}


def _extract_sensitive_terms(text: str) -> set[str]:
    terms: set[str] = set()
    terms.update(re.findall(r"[A-Z][A-Za-z0-9_-]{2,}", text))
    terms.update(re.findall(r"\b\d+(?:[.,]\d+)?\s*(?:美|美元|分|年|週|天|小時|頁|%|元)?", text))
    for pattern in (r"「([^」]{2,30})」", r"『([^』]{2,30})』", r"《([^》]{2,30})》"):
        terms.update(re.findall(pattern, text))
    return {t.strip() for t in terms if t.strip()}


def _detect_event_level_hits(
    text: str,
    history: Iterable[dict[str, str]],
    terms: set[str],
    *,
    min_len: int,
) -> list[str]:
    hits: list[str] = []
    for turn in history:
        if turn.get("role") != "user":
            continue
        for chunk in _split_sentences(turn.get("content", "")):
            if len(chunk) < min_len:
                continue
            chunk_terms = [term for term in terms if term in chunk and term in text]
            if chunk in text or len(chunk_terms) >= 2:
                hits.append(chunk)
    return hits


def _detect_indirect_identity_hits(text: str) -> list[str]:
    hits: list[str] = []
    for pattern in _INDIRECT_IDENTITY_PATTERNS:
        hits.extend(match.group(0) for match in re.finditer(pattern, text, flags=re.IGNORECASE))
    return sorted(set(hits))


def _detect_paraphrase_hits(
    text: str,
    history: Iterable[dict[str, str]],
    *,
    min_len: int,
) -> list[str]:
    """Catch high-overlap paraphrases that avoid exact raw quotes."""
    hits: list[str] = []
    output_grams = _char_grams(text)
    if not output_grams:
        return hits
    for turn in history:
        if turn.get("role") != "user":
            continue
        for chunk in _split_sentences(turn.get("content", "")):
            if len(chunk) < min_len or chunk in text:
                continue
            chunk_grams = _char_grams(chunk)
            if len(chunk_grams) < 8:
                continue
            overlap = len(chunk_grams & output_grams)
            if overlap >= 4 and overlap / len(chunk_grams) >= 0.25:
                hits.append(chunk)
    return hits


def _char_grams(text: str, n: int = 2) -> set[str]:
    normalized = re.sub(r"[\s，。！？!?、,.；;：「」『』()（）\[\]{}]", "", text)
    if len(normalized) < n:
        return set()
    return {normalized[i : i + n] for i in range(len(normalized) - n + 1)}


def _risk_level(score: float) -> str:
    if score >= 0.7:
        return "high"
    if score >= 0.35:
        return "medium"
    if score > 0:
        return "low"
    return "none"


def _sanitize_value(value: Any, terms: set[str]) -> Any:
    if isinstance(value, dict):
        cleaned: dict[str, Any] = {}
        for key, item in value.items():
            if key in _SENSITIVE_KEYS:
                continue
            cleaned[key] = _sanitize_value(item, terms)
        return cleaned
    if isinstance(value, list):
        return [_sanitize_value(item, terms) for item in value]
    if isinstance(value, str):
        return _sanitize_text(value, terms)
    return value


def _sanitize_text(text: str, terms: set[str]) -> str:
    cleaned = text
    for term in sorted(terms, key=len, reverse=True):
        if len(term) < 2:
            continue
        cleaned = cleaned.replace(term, _ABSTRACT_REPLACEMENT)
    cleaned = re.sub(r"\b\d+(?:[.,]\d+)?\s*(?:美|美元|分|年|週|天|小時|頁|%|元)?", _ABSTRACT_REPLACEMENT, cleaned)
    cleaned = re.sub(r"[A-Z][A-Za-z0-9_-]{2,}", _ABSTRACT_REPLACEMENT, cleaned)
    return cleaned
