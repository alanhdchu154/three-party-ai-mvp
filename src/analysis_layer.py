"""Analysis Layer v0.1.

Builds evidence-disciplined case summaries from existing Saga A artifacts.
This module does not generate conversations, call LLMs, or make clinical
diagnoses. Reports are synthetic-only unless explicitly marked otherwise.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from . import abstraction, dimension_store, source_types

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
CASE_SUMMARY_DIR = DATA_DIR / "case_summaries"

EvidenceRef = dict[str, Any]
CaseSummary = dict[str, Any]


@dataclass
class AnalysisCorpus:
    sagas_text: str = ""
    conversations: dict[str, list[dict[str, Any]]] = field(default_factory=dict)
    analysis_reports: dict[str, dict[str, Any]] = field(default_factory=dict)
    dimension_scores: dict[str, dict[str, Any]] = field(default_factory=dict)
    profiles: dict[str, dict[str, Any]] = field(default_factory=dict)
    party_profiles: dict[str, dict[str, dict[str, Any]]] = field(default_factory=dict)
    triage_outputs: dict[str, dict[str, Any]] = field(default_factory=dict)


def load_corpus(data_dir: Path = DATA_DIR) -> AnalysisCorpus:
    """Read existing local artifacts without creating new data."""
    corpus = AnalysisCorpus()
    sagas = data_dir / "sagas.md"
    if sagas.exists():
        corpus.sagas_text = sagas.read_text(encoding="utf-8")

    for path in sorted((data_dir / "generated_conversations").glob("*.json")):
        payload = _read_json(path)
        if not payload or path.name == "index.json":
            continue
        student_id = _student_id_from_payload(payload)
        payload["_source_path"] = _rel(path)
        payload["source_type"] = source_types.normalize_source_type(
            payload.get("source_type") or "llm_generated"
        )
        corpus.conversations.setdefault(student_id, []).append(payload)

    for path in sorted((data_dir / "analysis_reports").glob("*.json")):
        payload = _read_json(path)
        if not payload:
            continue
        student_id = str(payload.get("student") or path.stem.removesuffix("_analysis"))
        payload["_source_path"] = _rel(path)
        payload["source_type"] = source_types.normalize_source_type(
            payload.get("source_type") or "synthetic"
        )
        corpus.analysis_reports[student_id] = payload

    for path in sorted((data_dir / "dimension_scores").glob("*.json")):
        payload = _read_json(path)
        if not payload:
            continue
        student_id = path.stem
        payload["_source_path"] = _rel(path)
        payload["source_type"] = source_types.normalize_source_type(
            payload.get("source_type") or "synthetic"
        )
        corpus.dimension_scores[student_id] = payload

    for path in sorted((data_dir / "student_profiles").glob("*.json")):
        payload = _read_json(path)
        if not payload:
            continue
        student_id = str(payload.get("student_id") or path.stem)
        payload["_source_path"] = _rel(path)
        payload["source_type"] = source_types.normalize_source_type(payload.get("source_type"))
        corpus.profiles[student_id] = payload

    party_root = data_dir / "party_profiles"
    if party_root.exists():
        for path in sorted(party_root.glob("*/*.json")):
            payload = _read_json(path)
            if not payload:
                continue
            student_id = str(payload.get("student_id") or path.parent.name)
            party = str(payload.get("party") or path.stem)
            payload["_source_path"] = _rel(path)
            payload["source_type"] = source_types.normalize_source_type(payload.get("source_type"))
            corpus.party_profiles.setdefault(student_id, {})[party] = payload

    triage_dir = data_dir / "triage_outputs"
    if triage_dir.exists():
        for path in sorted(triage_dir.glob("*.json")):
            payload = _read_json(path)
            if not payload:
                continue
            student_id = str(payload.get("student_id") or path.stem)
            payload["_source_path"] = _rel(path)
            payload["source_type"] = source_types.normalize_source_type(payload.get("source_type"))
            corpus.triage_outputs[student_id] = payload

    return corpus


def build_case_summaries(corpus: AnalysisCorpus | None = None) -> list[CaseSummary]:
    corpus = corpus or load_corpus()
    student_ids = sorted(
        set(corpus.conversations)
        | set(corpus.analysis_reports)
        | set(corpus.dimension_scores)
        | set(corpus.profiles)
        | set(corpus.triage_outputs)
    )
    return [build_case_summary(student_id, corpus) for student_id in student_ids]


def build_case_summary(student_id: str, corpus: AnalysisCorpus) -> CaseSummary:
    conversations = corpus.conversations.get(student_id, [])
    report = corpus.analysis_reports.get(student_id, {})
    dimensions = corpus.dimension_scores.get(student_id, {})
    profile = corpus.profiles.get(student_id) or report.get("student_profile", {})
    party_profiles = _party_profiles_for(student_id, corpus, report)
    triage_output = corpus.triage_outputs.get(student_id, {})
    analysis = report.get("analysis", {})
    protected_terms = _protected_terms(report, profile, conversations, party_profiles)

    evidence: list[EvidenceRef] = []
    observed_signals = _observed_signals(student_id, dimensions, conversations, evidence, protected_terms)
    inferred_needs = _inferred_needs(student_id, profile, analysis, dimensions, evidence, protected_terms)
    risk_dimensions = _risk_dimensions(student_id, dimensions, evidence, protected_terms)
    recommended_actions = _recommended_actions(student_id, analysis, triage_output, dimensions, evidence, protected_terms)
    coordination_snapshot = _coordination_snapshot(
        student_id,
        profile,
        party_profiles,
        analysis,
        dimensions,
        evidence,
        protected_terms,
    )
    contradictions = detect_contradictions(
        student_id=student_id,
        report=report,
        dimensions=dimensions,
        triage_output=triage_output,
        evidence=evidence,
    )

    summary: CaseSummary = {
        "student_id": student_id,
        "character_id": report.get("persona_id") or _first_value(conversations, "persona_id") or student_id,
        "source_type": _summary_source_type(report, conversations, dimensions, profile),
        "observed_signals": observed_signals,
        "inferred_needs": inferred_needs,
        "risk_dimensions": risk_dimensions,
        "privacy_constraints": _privacy_constraints(report, profile, evidence),
        "party_profiles": _party_profile_summaries(party_profiles, protected_terms),
        "coordination_snapshot": coordination_snapshot,
        "recommended_actions": recommended_actions,
        "confidence_level": _confidence_level(evidence, contradictions),
        "evidence_refs": evidence,
        "missing_information": _missing_information(report, dimensions, triage_output),
        "next_watch_signals": _next_watch_signals(student_id, analysis, evidence, protected_terms),
        "contradictions": contradictions,
        "synthetic_only_warning": _is_synthetic_only(report, conversations, dimensions, profile, triage_output),
    }
    return summary


def detect_contradictions(
    *,
    student_id: str,
    report: dict[str, Any],
    dimensions: dict[str, Any],
    triage_output: dict[str, Any],
    evidence: list[EvidenceRef] | None = None,
) -> list[dict[str, Any]]:
    evidence = evidence if evidence is not None else []
    analysis = report.get("analysis", {})
    profile = report.get("student_profile", {})
    out: list[dict[str, Any]] = []

    profile_text = _blob(profile)
    parent_teacher_text = f"{report.get('parent_input', '')}\n{report.get('teacher_input', '')}"
    if _contains_any(profile_text, ("身份", "家族", "family", "identity")) and _contains_any(
        parent_teacher_text, ("學業", "作業", "成績", "academic")
    ):
        out.append(_contradiction(
            "perspective_gap",
            "Student-side profile centers identity/family strain while parent/teacher input frames the issue as academics or behavior.",
            "medium",
            _add_evidence(evidence, student_id, "coordinator_report", report.get("_source_path", ""), "profile/parent-teacher perspective gap", "medium", report.get("source_type")),
        ))

    highest_level = _highest_dimension_level(dimensions)
    needs_external = bool(analysis.get("needs_external_intervention"))
    if highest_level >= 3 and not needs_external:
        out.append(_contradiction(
            "dimension_vs_coordinator",
            "Dimension score has Level 3 concern but coordinator report does not request external intervention.",
            "high",
            _add_evidence(evidence, student_id, "dimension_score", dimensions.get("_source_path", ""), "Level 3 dimension conflict", "high", dimensions.get("source_type")),
        ))
    if highest_level <= 1 and needs_external:
        out.append(_contradiction(
            "possible_over_escalation",
            "Coordinator requests external intervention but dimension scores do not show Level 2/3 strain.",
            "medium",
            _add_evidence(evidence, student_id, "coordinator_report", report.get("_source_path", ""), "external intervention with low dimensions", "medium", report.get("source_type")),
        ))

    triage_type = triage_output.get("escalation_type")
    if highest_level >= 3 and triage_type in {"none", None, ""}:
        out.append(_contradiction(
            "triage_too_low",
            "Dimension score suggests urgent review but triage output is missing or non-escalating.",
            "high",
            _add_evidence(evidence, student_id, "triage", triage_output.get("_source_path", ""), "triage missing despite high score", "medium", triage_output.get("source_type")),
        ))
    if recommended_without_evidence(analysis, dimensions, triage_output):
        out.append(_contradiction(
            "recommendation_under_evidenced",
            "At least one recommendation appears stronger than the available evidence supports.",
            "medium",
            _add_evidence(evidence, student_id, "coordinator_report", report.get("_source_path", ""), "recommendation evidence check", "medium", report.get("source_type")),
        ))

    return out


def recommended_without_evidence(
    analysis: dict[str, Any],
    dimensions: dict[str, Any],
    triage_output: dict[str, Any],
) -> bool:
    if triage_output.get("escalation_type") in {"crisis_intervention", "professional_counseling"}:
        return _highest_dimension_level(dimensions) < 2 and not analysis.get("needs_external_intervention")
    return False


def generate_case_reports(
    summaries: list[CaseSummary] | None = None,
    *,
    output_dir: Path = CASE_SUMMARY_DIR,
) -> list[Path]:
    summaries = summaries or build_case_summaries()
    output_dir.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []
    for summary in summaries:
        path = output_dir / f"{summary['student_id']}.md"
        path.write_text(render_case_report(summary), encoding="utf-8")
        paths.append(path)
    return paths


def render_case_report(summary: CaseSummary) -> str:
    warning = (
        "> Warning: This case summary is based on synthetic Saga A data only. "
        "Do not treat it as real-world validation.\n\n"
        if summary.get("synthetic_only_warning")
        else ""
    )
    lines = [
        f"# Case Summary — {summary['student_id']}",
        "",
        warning.rstrip(),
        f"- Character ID: `{summary['character_id']}`",
        f"- Source type: `{summary['source_type']}`",
        f"- Confidence: `{summary['confidence_level']}`",
        "",
        "## What is happening",
        _bullets(summary["observed_signals"]),
        "",
        "## What we know",
        _evidence_bullets(summary["evidence_refs"]),
        "",
        "## What we infer",
        _bullets(summary["inferred_needs"]),
        "",
        "## Three-Party Coordination Snapshot",
        _render_coordination_snapshot(summary.get("coordination_snapshot", {})),
        "",
        "## What we must not reveal",
        _bullets(summary["privacy_constraints"]),
        "",
        "## What action is justified",
        _bullets(summary["recommended_actions"]),
        "",
        "## What action is not justified yet",
        _bullets(_not_justified(summary)),
        "",
        "## What to watch next week",
        _bullets(summary["next_watch_signals"]),
        "",
        "## Contradictions / Review Flags",
        _bullets([item["description"] for item in summary.get("contradictions", [])] or ["No major contradiction detected by deterministic checks."]),
        "",
        "## Missing Information",
        _bullets(summary["missing_information"]),
        "",
    ]
    return "\n".join(line for line in lines if line is not None) + "\n"


def _observed_signals(
    student_id: str,
    dimensions: dict[str, Any],
    conversations: list[dict[str, Any]],
    evidence: list[EvidenceRef],
    protected_terms: list[str],
) -> list[str]:
    signals: list[str] = []
    for dim_key, dim in (dimensions.get("dimensions") or {}).items():
        level = _safe_int(dim.get("level"), 0)
        if level <= 0:
            continue
        n_signals = len(dim.get("signals_observed") or [])
        signals.append(
            f"{dim_key} Level {level}: {n_signals} supporting signal(s) recorded in dimension score; high-specificity details withheld."
        )
        _add_evidence(evidence, student_id, "dimension_score", dimensions.get("_source_path", ""), f"{dim_key} Level {level}", "high", dimensions.get("source_type"))
    if not signals and conversations:
        signals.append(f"{len(conversations)} existing conversation artifacts available for this character.")
        _add_evidence(evidence, student_id, "raw_conversation", conversations[0].get("_source_path", ""), "conversation artifact exists", "low", conversations[0].get("source_type"))
    return signals[:8] or ["No observed signal available in existing artifacts."]


def _inferred_needs(
    student_id: str,
    profile: dict[str, Any],
    analysis: dict[str, Any],
    dimensions: dict[str, Any],
    evidence: list[EvidenceRef],
    protected_terms: list[str],
) -> list[str]:
    needs = [_sanitize_text(str(item), protected_terms) for item in profile.get("needs_signals", [])]
    if analysis.get("whats_really_happening"):
        needs.append("Coordinator report indicates an underlying support need; high-specificity event details are withheld in the case summary.")
        _add_evidence(evidence, student_id, "coordinator_report", "", "coordinator synthesis", "medium", "synthetic")
    highest = dimensions.get("highest_concern_dimension")
    if highest:
        needs.append(f"Primary support need appears connected to `{highest}`; treat this as synthetic benchmark inference, not diagnosis.")
    return needs[:6] or ["Needs are not inferable from current artifacts."]


def _risk_dimensions(
    student_id: str,
    dimensions: dict[str, Any],
    evidence: list[EvidenceRef],
    protected_terms: list[str],
) -> list[dict[str, Any]]:
    risks: list[dict[str, Any]] = []
    for key, value in (dimensions.get("dimensions") or {}).items():
        level = _safe_int(value.get("level"), 0)
        if level <= 0:
            continue
        risks.append({
            "dimension": key,
            "level": level,
            "evidence_count": len(value.get("signals_observed") or []),
            "reasoning": "Detailed reasoning withheld from pilot-facing summary; inspect authorized source artifact if needed.",
        })
    if risks:
        _add_evidence(evidence, student_id, "dimension_score", dimensions.get("_source_path", ""), "risk dimensions", "high", dimensions.get("source_type"))
    return risks


def _privacy_constraints(report: dict[str, Any], profile: dict[str, Any], evidence: list[EvidenceRef]) -> list[str]:
    constraints = []
    kept_count = len((report.get("analysis") or {}).get("privacy_kept") or [])
    do_not_share_count = len(profile.get("do_not_share") or [])
    if kept_count:
        constraints.append(f"Coordinator marked {kept_count} private detail categories that must not be shown verbatim.")
    if do_not_share_count:
        constraints.append(f"Student profile has {do_not_share_count} do-not-share items; summarize only themes.")
    constraints.append("Do not reveal raw turns, scenario seeds, secret truths, or highly specific family events.")
    _add_evidence(evidence, str(report.get("student", "unknown")), "coordinator_report", report.get("_source_path", ""), "privacy constraints", "high", report.get("source_type"))
    return constraints


def _recommended_actions(
    student_id: str,
    analysis: dict[str, Any],
    triage_output: dict[str, Any],
    dimensions: dict[str, Any],
    evidence: list[EvidenceRef],
    protected_terms: list[str],
) -> list[str]:
    actions: list[str] = []
    this_week = analysis.get("this_week") or {}
    for party, payload in this_week.items():
        for action in (payload or {}).get("do", [])[:2]:
            actions.append(f"{party}: {_sanitize_text(str(action), protected_terms)}")
    if triage_output:
        actions.append(f"Triage recommends `{triage_output.get('escalation_type', 'none')}` with `{triage_output.get('urgency', 'low')}` urgency.")
        _add_evidence(evidence, student_id, "triage", triage_output.get("_source_path", ""), "triage recommendation", "medium", triage_output.get("source_type"))
    elif _highest_dimension_level(dimensions) >= 2:
        actions.append("Human review is justified because at least one dimension is Level 2 or higher.")
    return actions[:8] or ["No action is justified beyond continued monitoring from current evidence."]


def _next_watch_signals(
    student_id: str,
    analysis: dict[str, Any],
    evidence: list[EvidenceRef],
    protected_terms: list[str],
) -> list[str]:
    watch = [_sanitize_text(str(item), protected_terms) for item in analysis.get("watch_for", [])]
    if watch:
        _add_evidence(evidence, student_id, "coordinator_report", "", "watch signals", "medium", "synthetic")
    return watch[:6] or ["Watch for worsening trajectory, new Level 2 persistence, or emotional safety escalation."]


def _party_profiles_for(
    student_id: str,
    corpus: AnalysisCorpus,
    report: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    existing = corpus.party_profiles.get(student_id, {})
    out: dict[str, dict[str, Any]] = {}
    for party in ("parent", "teacher"):
        if existing.get(party):
            out[party] = abstraction.normalize_party_profile(
                party,
                existing[party],
                source_type=existing[party].get("source_type", report.get("source_type", "synthetic")),
            )
            continue
        raw_key = "parent_input" if party == "parent" else "teacher_input"
        raw = str(report.get(raw_key) or "").strip()
        if raw:
            out[party] = abstraction.extract_party_profile(
                party,
                [{"role": "user", "content": raw}],
                source_type=report.get("source_type", "synthetic"),
            )
    return out


def _party_profile_summaries(
    party_profiles: dict[str, dict[str, Any]],
    protected_terms: list[str],
) -> dict[str, dict[str, Any]]:
    summaries: dict[str, dict[str, Any]] = {}
    for party, profile in party_profiles.items():
        view = abstraction.party_profile_view(profile, audience="internal_reviewer")
        summaries[party] = {
            "party": party,
            "expressed_concerns": _sanitize_list(view.get("expressed_concerns"), protected_terms),
            "underlying_needs": _sanitize_list(view.get("underlying_needs"), protected_terms),
            "fears_or_constraints": _sanitize_list(view.get("fears_or_constraints"), protected_terms),
            "blind_spots": _sanitize_list(view.get("blind_spots"), protected_terms),
            "what_they_can_offer": _sanitize_list(view.get("what_they_can_offer"), protected_terms),
            "safe_summary_for_coordinator": _sanitize_text(
                str(view.get("safe_summary_for_coordinator") or ""),
                protected_terms,
            ),
            "what_not_to_share_count": len(view.get("what_not_to_share") or []),
            "confidence_level": view.get("confidence_level", "low"),
        }
    return summaries


def _coordination_snapshot(
    student_id: str,
    profile: dict[str, Any],
    party_profiles: dict[str, dict[str, Any]],
    analysis: dict[str, Any],
    dimensions: dict[str, Any],
    evidence: list[EvidenceRef],
    protected_terms: list[str],
) -> dict[str, Any]:
    parent = party_profiles.get("parent", {})
    teacher = party_profiles.get("teacher", {})
    student_needs = _sanitize_list(profile.get("needs_signals"), protected_terms)
    student_concerns = _sanitize_list(profile.get("key_concerns"), protected_terms)
    highest = str(dimensions.get("highest_concern_dimension") or "").strip()

    snapshot = {
        "student": {
            "observed_signals": student_concerns[:4],
            "inferred_needs": student_needs[:4],
            "privacy_constraints_count": len(profile.get("do_not_share") or []),
        },
        "parent": _party_profile_summaries({"parent": parent}, protected_terms).get("parent", {}),
        "teacher": _party_profile_summaries({"teacher": teacher}, protected_terms).get("teacher", {}),
        "alignment": [],
        "mismatches": [],
        "coordination_risks": [],
        "safe_bridges": [],
    }

    if highest:
        snapshot["alignment"].append(
            f"All recommendations should be checked against the active concern area `{highest}`."
        )
    if parent and teacher:
        snapshot["alignment"].append("Parent and teacher perspectives are both available for coordinator synthesis.")
    if parent and student_concerns:
        snapshot["mismatches"].append(
            "Parent concerns may frame the issue differently from the student's inferred needs; use low-pressure translation."
        )
    if teacher and student_concerns:
        snapshot["mismatches"].append(
            "Teacher observations may show school-facing behavior without the full private context."
        )
    if parent.get("blind_spots"):
        snapshot["coordination_risks"].append("Parent guidance could become pressure if it asks for hidden details.")
    if teacher.get("blind_spots"):
        snapshot["coordination_risks"].append("Teacher guidance could over-focus on visible behavior without context.")
    if (analysis.get("privacy_kept") or []) or profile.get("do_not_share"):
        snapshot["coordination_risks"].append("Cross-party messages must not reveal protected private details.")

    if parent.get("what_they_can_offer"):
        snapshot["safe_bridges"].append("Parent can provide broad support without requesting private details.")
    if teacher.get("what_they_can_offer"):
        snapshot["safe_bridges"].append("Teacher can provide classroom support without exposing private context.")
    if not snapshot["safe_bridges"]:
        snapshot["safe_bridges"].append("Use human reviewer guidance before making stronger recommendations.")

    _add_evidence(
        evidence,
        student_id,
        "abstracted_profile",
        "data/party_profiles or analysis report inputs",
        "three-party coordination snapshot",
        "medium",
        dimensions.get("source_type") or "synthetic",
    )
    return snapshot


def _missing_information(report: dict[str, Any], dimensions: dict[str, Any], triage_output: dict[str, Any]) -> list[str]:
    missing = []
    if not report:
        missing.append("No coordinator analysis report found.")
    if not dimensions:
        missing.append("No dimension score file found.")
    if not triage_output:
        missing.append("No saved triage output found; analysis uses dimension/report evidence only.")
    missing.append("No real pilot evidence; all current Saga A artifacts should be treated as synthetic benchmark data.")
    return missing


def _confidence_level(evidence: list[EvidenceRef], contradictions: list[dict[str, Any]]) -> str:
    high = sum(1 for item in evidence if item.get("confidence") == "high")
    kinds = {item.get("source_kind") for item in evidence}
    if any(item.get("severity") == "high" for item in contradictions):
        return "medium"
    if high >= 2 and len(kinds) >= 2:
        return "high"
    if evidence:
        return "medium"
    return "low"


def _summary_source_type(*payloads: Any) -> str:
    values: list[str] = []
    for payload in payloads:
        if isinstance(payload, list):
            values.extend(str(item.get("source_type", "")) for item in payload if isinstance(item, dict))
        elif isinstance(payload, dict):
            values.append(str(payload.get("source_type", "")))
    if any(source_types.is_pilot_source(value) for value in values):
        return "pilot_real_anonymized"
    if any(source_types.normalize_source_type(value) == "llm_generated" for value in values):
        return "llm_generated"
    if any(source_types.normalize_source_type(value) == "handcrafted_gold" for value in values):
        return "handcrafted_gold"
    return "synthetic"


def _is_synthetic_only(*payloads: Any) -> bool:
    values: list[str] = []
    for payload in payloads:
        if isinstance(payload, list):
            values.extend(str(item.get("source_type", "")) for item in payload if isinstance(item, dict))
        elif isinstance(payload, dict):
            values.append(str(payload.get("source_type", "")))
    return not any(source_types.is_pilot_source(value) for value in values)


def _sanitize_text(text: str, protected_terms: list[str]) -> str:
    return abstraction.sanitize_for_privacy(text, protected_terms=protected_terms)


def _sanitize_list(value: Any, protected_terms: list[str]) -> list[str]:
    if not isinstance(value, list):
        return []
    return [
        _sanitize_text(str(item), protected_terms)
        for item in value
        if str(item).strip()
    ]


def _protected_terms(
    report: dict[str, Any],
    profile: dict[str, Any],
    conversations: list[dict[str, Any]],
    party_profiles: dict[str, dict[str, Any]] | None = None,
) -> list[str]:
    terms: list[str] = []
    analysis = report.get("analysis") or {}
    terms.extend(analysis.get("privacy_kept") or [])
    terms.extend(profile.get("do_not_share") or [])
    for party_profile in (party_profiles or {}).values():
        terms.extend(party_profile.get("what_not_to_share") or [])
    for conv in conversations:
        terms.extend([conv.get("scenario_seed", ""), conv.get("scenario_seed_id", "")])
    return [term for term in terms if term]


def _add_evidence(
    evidence: list[EvidenceRef],
    student_id: str,
    source_kind: str,
    source_path: str,
    claim: str,
    confidence: str,
    source_type: str | None,
) -> EvidenceRef:
    ref = {
        "id": f"ev_{len(evidence) + 1:03d}",
        "student_id": student_id,
        "source": source_path or "existing artifact",
        "source_kind": source_kind,
        "claim": claim,
        "confidence": confidence if confidence in {"low", "medium", "high"} else "low",
        "synthetic_only": not source_types.is_pilot_source(source_type),
    }
    evidence.append(ref)
    return ref


def _contradiction(kind: str, description: str, severity: str, evidence_ref: EvidenceRef) -> dict[str, Any]:
    return {
        "kind": kind,
        "description": description,
        "severity": severity,
        "evidence_ref": evidence_ref["id"],
    }


def _not_justified(summary: CaseSummary) -> list[str]:
    items = [
        "Do not make a clinical diagnosis from synthetic benchmark evidence.",
        "Do not take irreversible school/family action without human review.",
        "Do not reveal protected private details to parents, teachers, tutors, or other students.",
    ]
    if summary.get("synthetic_only_warning"):
        items.append("Do not treat this as real pilot validation.")
    return items


def _evidence_bullets(evidence: list[EvidenceRef]) -> str:
    if not evidence:
        return "- No evidence refs available."
    lines = []
    for item in evidence:
        synth = "synthetic-only" if item.get("synthetic_only") else "pilot/anonymized"
        lines.append(
            f"- `{item['id']}` {item['source_kind']} · {item['confidence']} · {synth} · {item['claim']} · `{item['source']}`"
        )
    return "\n".join(lines)


def _render_coordination_snapshot(snapshot: dict[str, Any]) -> str:
    if not snapshot:
        return "- No three-party snapshot available."
    lines = []
    student = snapshot.get("student") or {}
    lines.append("### Student")
    lines.append(_bullets([
        f"Observed signals: {', '.join(student.get('observed_signals') or ['not available'])}",
        f"Inferred needs: {', '.join(student.get('inferred_needs') or ['not available'])}",
        f"Privacy constraints count: {student.get('privacy_constraints_count', 0)}",
    ]))
    for party in ("parent", "teacher"):
        data = snapshot.get(party) or {}
        lines.append(f"### {party.title()}")
        if not data:
            lines.append("- No party profile available.")
            continue
        lines.append(_bullets([
            f"Expressed concerns: {', '.join(data.get('expressed_concerns') or ['not available'])}",
            f"Likely needs: {', '.join(data.get('underlying_needs') or ['not available'])}",
            f"Constraints/blind spots: {', '.join((data.get('fears_or_constraints') or []) + (data.get('blind_spots') or []) or ['not available'])}",
            f"What they can offer: {', '.join(data.get('what_they_can_offer') or ['not available'])}",
            f"Private constraints count: {data.get('what_not_to_share_count', 0)}",
        ]))
    lines.extend([
        "### Coordination Problem",
        _bullets(snapshot.get("alignment") or ["No clear alignment detected."]),
        "### Mismatches / Risks",
        _bullets((snapshot.get("mismatches") or []) + (snapshot.get("coordination_risks") or []) or ["No major mismatch detected."]),
        "### Safe Bridges",
        _bullets(snapshot.get("safe_bridges") or ["Use reviewer guidance before stronger action."]),
    ])
    return "\n".join(lines)


def _bullets(items: Any) -> str:
    if not items:
        return "- None."
    if isinstance(items, str):
        items = [items]
    lines = []
    for item in items:
        if isinstance(item, dict):
            lines.append(f"- {json.dumps(item, ensure_ascii=False)}")
        else:
            lines.append(f"- {item}")
    return "\n".join(lines)


def _read_json(path: Path) -> dict[str, Any] | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def _rel(path: Path) -> str:
    try:
        return str(path.relative_to(PROJECT_ROOT))
    except ValueError:
        return str(path)


def _student_id_from_payload(payload: dict[str, Any]) -> str:
    persona = str(payload.get("persona_id") or payload.get("student_persona_id") or payload.get("id") or "unknown")
    if persona.startswith("saga_a_"):
        return persona.removeprefix("saga_a_")
    return persona


def _first_value(items: list[dict[str, Any]], key: str) -> Any:
    for item in items:
        if item.get(key):
            return item[key]
    return None


def _safe_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _highest_dimension_level(dimensions: dict[str, Any]) -> int:
    return max((_safe_int(item.get("level")) for item in (dimensions.get("dimensions") or {}).values()), default=0)


def _contains_any(text: str, needles: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(needle.lower() in lowered for needle in needles)


def _blob(payload: Any) -> str:
    return json.dumps(payload, ensure_ascii=False)
