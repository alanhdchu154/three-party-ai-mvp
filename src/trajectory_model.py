"""Trajectory & Coordination Models v0.1.

Rule-based, human-readable trajectory detection. This is not ML, diagnosis,
or prediction certainty. Outputs describe possible risk patterns only.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from . import abstraction, analysis_layer, reviewer_workflow, signal_library, source_types

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
TRAJECTORY_REPORT_DIR = DATA_DIR / "trajectory_reports"

Trajectory = dict[str, Any]
SignalHit = dict[str, Any]


TRAJECTORY_RULES: dict[str, dict[str, Any]] = {
    "burnout_risk": {
        "trajectory_name": "Burnout Risk",
        "signals": {"perfectionism_pressure", "emotional_flattening", "future_planning_collapse", "autonomy_loss"},
        "dimension_triggers": {"academic_load", "future_planning", "identity"},
        "likely_outcomes_if_unchanged": [
            "Continued outward functioning with lower engagement.",
            "Possible hidden disengagement if adults respond only with performance pressure.",
        ],
        "recommended_interventions": [
            "Reduce performance interrogation; focus on low-pressure reflection.",
            "Offer one small student-owned choice instead of a broad life-plan question.",
        ],
    },
    "trust_erosion": {
        "trajectory_name": "Trust Erosion",
        "signals": {"parent_monitoring_increase", "masking_language", "social_withdrawal"},
        "dimension_triggers": {"family_dynamics", "social_development"},
        "likely_outcomes_if_unchanged": [
            "Student may share less with adults and rely more on indirect communication.",
            "Parent/teacher attempts to help may be experienced as surveillance.",
        ],
        "recommended_interventions": [
            "Protect privacy boundaries explicitly.",
            "Coach adults to create space without demanding disclosure.",
        ],
    },
    "disclosure_collapse": {
        "trajectory_name": "Disclosure Collapse",
        "signals": {"disclosure_drop", "masking_language", "social_withdrawal", "emotional_flattening"},
        "dimension_triggers": {"emotional_safety", "family_dynamics", "social_development"},
        "likely_outcomes_if_unchanged": [
            "AI may stop receiving the student's most useful truths.",
            "System confidence should decrease until new evidence appears.",
        ],
        "recommended_interventions": [
            "Avoid sudden cross-party exposure of private themes.",
            "Use shorter, choice-based check-ins rather than broad probing.",
        ],
    },
    "hidden_disengagement": {
        "trajectory_name": "Hidden Disengagement",
        "signals": {"strategic_compliance", "future_planning_collapse", "emotional_flattening", "autonomy_loss"},
        "dimension_triggers": {"academic_load", "future_planning", "identity"},
        "likely_outcomes_if_unchanged": [
            "Student may keep meeting visible expectations while internally opting out.",
            "Adults may miss the issue because grades or behavior remain stable.",
        ],
        "recommended_interventions": [
            "Look for agency signals, not only performance metrics.",
            "Offer low-stakes action experiments that belong to the student.",
        ],
    },
    "parent_escalation": {
        "trajectory_name": "Parent Escalation",
        "signals": {"parent_monitoring_increase", "strategic_compliance", "disclosure_drop"},
        "dimension_triggers": {"family_dynamics", "academic_load"},
        "likely_outcomes_if_unchanged": [
            "Parent concern may convert into more monitoring, reducing student trust.",
            "The coordination loop may become parent-driven rather than student-centered.",
        ],
        "recommended_interventions": [
            "Give parent concrete low-pressure behaviors instead of more questions.",
            "Do not share protected student details to calm parent anxiety.",
        ],
    },
    "dependency_risk": {
        "trajectory_name": "Dependency Risk",
        "signals": {"autonomy_loss", "disclosure_drop", "future_planning_collapse"},
        "dimension_triggers": {"identity", "future_planning", "emotional_safety"},
        "likely_outcomes_if_unchanged": [
            "Student may over-rely on AI or adult interpretation instead of building agency.",
            "The system may become a substitute for student-owned decisions.",
        ],
        "recommended_interventions": [
            "Return decisions to the student in small reversible steps.",
            "Use AI as scaffolding, not as the final authority.",
        ],
    },
}


def build_trajectory_models(corpus: analysis_layer.AnalysisCorpus | None = None) -> dict[str, list[Trajectory]]:
    corpus = corpus or analysis_layer.load_corpus()
    student_ids = sorted(
        set(corpus.conversations)
        | set(corpus.analysis_reports)
        | set(corpus.dimension_scores)
        | set(corpus.profiles)
        | set(corpus.triage_outputs)
    )
    return {student_id: detect_trajectories(student_id, corpus) for student_id in student_ids}


def detect_trajectories(student_id: str, corpus: analysis_layer.AnalysisCorpus) -> list[Trajectory]:
    context = _case_context(student_id, corpus)
    signal_hits = detect_signals(student_id, context)
    trajectories: list[Trajectory] = []
    for trajectory_id, rule in TRAJECTORY_RULES.items():
        trajectory = _trajectory_from_rule(trajectory_id, rule, student_id, context, signal_hits)
        if trajectory is not None:
            trajectories.append(trajectory)
    if not trajectories:
        trajectories.append(_insufficient_evidence_trajectory(student_id, context, signal_hits))
    trajectories.sort(key=lambda item: _confidence_rank(item["confidence"]), reverse=True)
    return trajectories


def detect_signals(student_id: str, context: dict[str, Any]) -> list[SignalHit]:
    text = context["text"].lower()
    dimensions = context["dimensions"].get("dimensions") or {}
    hits: list[SignalHit] = []

    def add(signal_id: str, reason: str, source_kind: str, source_path: str, confidence: str = "medium") -> None:
        if any(hit["signal_id"] == signal_id and hit["reason"] == reason for hit in hits):
            return
        hits.append({
            "signal_id": signal_id,
            "reason": reason,
            "source_kind": source_kind,
            "source": source_path or "existing artifact",
            "confidence": confidence,
            "synthetic_only": context["synthetic_only"],
        })

    if _has_any(text, ("表演", "炫技", "hypothetical", "沒事", "abstract", "foucault")):
        add("masking_language", "Language suggests indirect or performative self-presentation.", "coordinator_report", context["report_path"])
    if _has_any(text, ("舉手次數明顯變少", "spark 不見", "share less", "shorter", "沉默")):
        add("disclosure_drop", "Longitudinal artifact suggests reduced openness or visible participation.", "coordinator_report", context["report_path"])
    if _has_any(text, ("照做", "維持", "compliance", "不抱怨", "作業質量沒掉")):
        add("strategic_compliance", "Visible functioning may be masking private disengagement.", "coordinator_report", context["report_path"])
    if _has_any(text, ("不知道自己想做什麼", "外部評價", "agency", "自己想做什麼")):
        add("autonomy_loss", "Artifacts suggest difficulty naming self-owned goals.", "coordinator_report", context["report_path"])
    if _has_any(text, ("追問", "監控", "問他", "擔心", "checking", "surveillance")):
        add("parent_monitoring_increase", "Parent-facing context may increase questioning or monitoring.", "coordinator_report", context["report_path"])
    if _dimension_level(dimensions, "future_planning") >= 1 or _has_any(text, ("future", "未來", "想做什麼")):
        add("future_planning_collapse", "Future-planning uncertainty appears in dimensions or summary.", "dimension_score", context["dimension_path"])
    if _has_any(text, ("spark 不見", "反芻", "空白", "flattening", "functional")):
        add("emotional_flattening", "Student may remain functional while affect or spark decreases.", "dimension_score", context["dimension_path"])
    if _dimension_level(dimensions, "social_development") >= 1 or _has_any(text, ("迴避", "沉默", "withdraw", "疏遠")):
        add("social_withdrawal", "Social or family withdrawal should be watched as a possible pattern.", "dimension_score", context["dimension_path"])
    if _dimension_level(dimensions, "academic_load") >= 1 or _has_any(text, ("成績", "作業", "perfection", "achievement", "學業")):
        add("perfectionism_pressure", "Achievement pressure appears in dimension or coordination artifacts.", "dimension_score", context["dimension_path"])

    return hits


def generate_trajectory_reports(
    models: dict[str, list[Trajectory]] | None = None,
    *,
    output_dir: Path = TRAJECTORY_REPORT_DIR,
) -> list[Path]:
    models = models or build_trajectory_models()
    models = apply_reviewer_calibration(models)
    output_dir.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []
    for student_id, trajectories in models.items():
        path = output_dir / f"{student_id}.md"
        path.write_text(render_trajectory_report(student_id, trajectories), encoding="utf-8")
        paths.append(path)
    return paths


def apply_reviewer_calibration(
    models: dict[str, list[Trajectory]],
    *,
    review_summary: dict[str, Any] | None = None,
) -> dict[str, list[Trajectory]]:
    """Attach human calibration status to trajectory outputs."""
    review_summary = review_summary or reviewer_workflow.summarize_reviews()
    calibrated: dict[str, list[Trajectory]] = {}
    for student_id, trajectories in models.items():
        calibrated_items: list[Trajectory] = []
        for trajectory in trajectories:
            artifact_id = f"{student_id}:{trajectory['trajectory_id']}"
            calibration = reviewer_workflow.artifact_calibration(
                review_summary,
                artifact_type="trajectory_report",
                artifact_id=artifact_id,
            )
            item = dict(trajectory)
            if calibration:
                item["reviewer_calibration"] = {
                    "status": calibration["calibration_status"],
                    "verdict_counts": calibration["verdict_counts"],
                    "confidence_counts": calibration["confidence_counts"],
                    "reviewers": calibration["reviewers"],
                    "action_items": calibration["action_items"],
                }
                item["calibrated_confidence"] = _calibrated_confidence(
                    item["confidence"],
                    calibration,
                )
            else:
                item["reviewer_calibration"] = {
                    "status": "not_reviewed",
                    "verdict_counts": {},
                    "confidence_counts": {},
                    "reviewers": [],
                    "action_items": [],
                }
                item["calibrated_confidence"] = _downgrade_synthetic_confidence(item["confidence"], item.get("synthetic_only", True))
            calibrated_items.append(item)
        calibrated[student_id] = calibrated_items
    return calibrated


def render_trajectory_report(student_id: str, trajectories: list[Trajectory]) -> str:
    lines = [
        f"# Trajectory Report — {student_id}",
        "",
        "> These are possible risk patterns from synthetic/local artifacts, not diagnoses or certain predictions.",
        "",
    ]
    for trajectory in trajectories:
        lines.extend([
            f"## {trajectory['trajectory_name']} (`{trajectory['trajectory_id']}`)",
            f"- Confidence: `{trajectory['confidence']}`",
            f"- Calibrated confidence: `{trajectory.get('calibrated_confidence', trajectory['confidence'])}`",
            f"- Reviewer status: `{trajectory.get('reviewer_calibration', {}).get('status', 'not_reviewed')}`",
            "",
            "### Current trajectory",
            _bullets(trajectory["observed_patterns"]),
            "",
            "### Why the system thinks so",
            _evidence_bullets(trajectory["evidence_refs"]),
            "",
            "### Likely outcomes if unchanged",
            _bullets(trajectory["likely_outcomes_if_unchanged"]),
            "",
            "### Actions that may stabilize",
            _bullets(trajectory["recommended_interventions"]),
            "",
            "### Actions that may destabilize",
            _bullets(trajectory["destabilizing_factors"]),
            "",
            "### What evidence is missing",
            _bullets(trajectory["missing_evidence"]),
            "",
            "### Reviewer calibration",
            _reviewer_calibration_block(trajectory.get("reviewer_calibration", {})),
            "",
        ])
    return "\n".join(lines)


def _trajectory_from_rule(
    trajectory_id: str,
    rule: dict[str, Any],
    student_id: str,
    context: dict[str, Any],
    signal_hits: list[SignalHit],
) -> Trajectory | None:
    hit_ids = {hit["signal_id"] for hit in signal_hits}
    matched_signals = sorted(hit_ids & set(rule["signals"]))
    dimensions = context["dimensions"].get("dimensions") or {}
    matched_dimensions = [
        key for key in rule["dimension_triggers"]
        if _dimension_level(dimensions, key) >= 1
    ]
    if len(matched_signals) + len(matched_dimensions) < 2:
        return None

    confidence = _trajectory_confidence(matched_signals, matched_dimensions, context)
    evidence_refs = _trajectory_evidence_refs(student_id, matched_signals, matched_dimensions, context, signal_hits)
    trajectory = {
        "trajectory_id": trajectory_id,
        "trajectory_name": rule["trajectory_name"],
        "observed_patterns": [
            f"Possible `{signal_id}` pattern: {signal_library.get_signal(signal_id)['description']}"
            for signal_id in matched_signals
        ] + [
            f"Dimension `{dim}` is active in current score."
            for dim in matched_dimensions
        ],
        "contributing_signals": matched_signals,
        "stabilizing_factors": _stabilizing_factors(context),
        "destabilizing_factors": _destabilizing_factors(trajectory_id),
        "likely_outcomes_if_unchanged": rule["likely_outcomes_if_unchanged"],
        "recommended_interventions": rule["recommended_interventions"],
        "confidence": confidence,
        "evidence_refs": evidence_refs,
        "missing_evidence": _missing_evidence(context, confidence),
        "synthetic_only": context["synthetic_only"],
    }
    return trajectory


def _insufficient_evidence_trajectory(
    student_id: str,
    context: dict[str, Any],
    signal_hits: list[SignalHit],
) -> Trajectory:
    return {
        "trajectory_id": "insufficient_evidence",
        "trajectory_name": "Insufficient Evidence",
        "observed_patterns": ["No stable trajectory should be inferred yet."],
        "contributing_signals": [hit["signal_id"] for hit in signal_hits],
        "stabilizing_factors": _stabilizing_factors(context),
        "destabilizing_factors": ["Over-interpreting sparse or synthetic-only evidence."],
        "likely_outcomes_if_unchanged": ["System confidence should remain low until more longitudinal evidence exists."],
        "recommended_interventions": ["Continue observation without escalating beyond available evidence."],
        "confidence": "low",
        "evidence_refs": [],
        "missing_evidence": _missing_evidence(context, "low"),
        "synthetic_only": context["synthetic_only"],
    }


def _case_context(student_id: str, corpus: analysis_layer.AnalysisCorpus) -> dict[str, Any]:
    conversations = corpus.conversations.get(student_id, [])
    report = corpus.analysis_reports.get(student_id, {})
    dimensions = corpus.dimension_scores.get(student_id, {})
    profile = corpus.profiles.get(student_id) or report.get("student_profile", {})
    analysis = report.get("analysis", {})
    protected_terms = []
    protected_terms.extend(profile.get("do_not_share") or [])
    protected_terms.extend(analysis.get("privacy_kept") or [])
    protected_terms.extend(conv.get("scenario_seed", "") for conv in conversations)
    source_values = [report, dimensions, profile, *conversations]
    text = "\n".join(
        json.dumps(item, ensure_ascii=False)
        for item in (report, dimensions, profile)
        if item
    )
    return {
        "student_id": student_id,
        "conversations": conversations,
        "report": report,
        "dimensions": dimensions,
        "profile": profile,
        "analysis": analysis,
        "text": text,
        "protected_terms": [term for term in protected_terms if term],
        "report_path": report.get("_source_path", ""),
        "dimension_path": dimensions.get("_source_path", ""),
        "synthetic_only": not any(
            source_types.is_pilot_source(item.get("source_type"))
            for item in source_values
            if isinstance(item, dict)
        ),
    }


def _trajectory_confidence(
    matched_signals: list[str],
    matched_dimensions: list[str],
    context: dict[str, Any],
) -> str:
    evidence_count = len(matched_signals) + len(matched_dimensions)
    has_report = bool(context["report"])
    has_dimensions = bool(context["dimensions"])
    has_longitudinal = len(context["conversations"]) >= 3
    if evidence_count >= 4 and has_report and has_dimensions and has_longitudinal:
        return "high"
    if evidence_count >= 2 and (has_report or has_dimensions):
        return "medium"
    return "low"


def _trajectory_evidence_refs(
    student_id: str,
    matched_signals: list[str],
    matched_dimensions: list[str],
    context: dict[str, Any],
    signal_hits: list[SignalHit],
) -> list[dict[str, Any]]:
    refs: list[dict[str, Any]] = []
    for signal_id in matched_signals:
        hit = next((item for item in signal_hits if item["signal_id"] == signal_id), {})
        refs.append({
            "id": f"traj_ev_{len(refs) + 1:03d}",
            "student_id": student_id,
            "source": hit.get("source", "existing artifact"),
            "source_kind": hit.get("source_kind", "coordinator_report"),
            "claim": f"Possible signal `{signal_id}` detected.",
            "confidence": hit.get("confidence", "medium"),
            "synthetic_only": context["synthetic_only"],
        })
    for dim in matched_dimensions:
        refs.append({
            "id": f"traj_ev_{len(refs) + 1:03d}",
            "student_id": student_id,
            "source": context["dimension_path"] or "existing artifact",
            "source_kind": "dimension_score",
            "claim": f"Dimension `{dim}` is Level {_dimension_level(context['dimensions'].get('dimensions') or {}, dim)}.",
            "confidence": "high" if context["dimensions"] else "low",
            "synthetic_only": context["synthetic_only"],
        })
    return refs


def _stabilizing_factors(context: dict[str, Any]) -> list[str]:
    factors = []
    if context["analysis"].get("this_week"):
        factors.append("Coordinator has concrete reversible actions available.")
    if context["dimensions"] and _dimension_level(context["dimensions"].get("dimensions") or {}, "emotional_safety") < 3:
        factors.append("Current emotional safety score is below Level 3.")
    if len(context["conversations"]) >= 3:
        factors.append("Multiple existing artifacts allow comparison across time, though still synthetic.")
    return factors or ["No clear stabilizing factor detected from current artifacts."]


def _destabilizing_factors(trajectory_id: str) -> list[str]:
    common = [
        "Treating the possible trajectory as certainty.",
        "Sharing protected details across parties to force alignment.",
    ]
    specific = {
        "burnout_risk": ["Increasing performance pressure without restoring agency."],
        "trust_erosion": ["Parent or teacher questioning that feels like surveillance."],
        "disclosure_collapse": ["Pushing for more disclosure after trust has weakened."],
        "hidden_disengagement": ["Mistaking visible compliance for true buy-in."],
        "parent_escalation": ["Using private student themes to calm parent anxiety."],
        "dependency_risk": ["Letting AI make decisions the student should practice making."],
    }
    return common + specific.get(trajectory_id, [])


def _missing_evidence(context: dict[str, Any], confidence: str) -> list[str]:
    missing = []
    if not context["dimensions"]:
        missing.append("No dimension score artifact.")
    if not context["report"]:
        missing.append("No coordinator report artifact.")
    if len(context["conversations"]) < 3:
        missing.append("Fewer than three conversation artifacts; downgrade trajectory confidence.")
    if context["synthetic_only"]:
        missing.append("No real pilot evidence; synthetic-only trajectory should not be treated as validation.")
    if confidence == "low":
        missing.append("Need repeated time-stamped observations before inferring a stable trajectory.")
    return missing or ["No major missing evidence detected by deterministic checks."]


def _dimension_level(dimensions: dict[str, Any], key: str) -> int:
    try:
        return int((dimensions.get(key) or {}).get("level", 0))
    except (TypeError, ValueError):
        return 0


def _has_any(text: str, needles: tuple[str, ...]) -> bool:
    return any(needle.lower() in text for needle in needles)


def _confidence_rank(confidence: str) -> int:
    return {"low": 0, "medium": 1, "high": 2}.get(confidence, 0)


def _calibrated_confidence(rule_confidence: str, calibration: dict[str, Any]) -> str:
    verdicts = calibration.get("verdict_counts", {})
    if verdicts.get("false_positive") or verdicts.get("under_evidenced") or verdicts.get("needs_more_evidence"):
        return "low"
    if verdicts.get("privacy_concern"):
        return "low"
    confidence_counts = calibration.get("confidence_counts", {})
    if confidence_counts:
        return max(confidence_counts, key=lambda key: _confidence_rank(key))
    return _downgrade_synthetic_confidence(rule_confidence, True)


def _downgrade_synthetic_confidence(confidence: str, synthetic_only: bool) -> str:
    if not synthetic_only:
        return confidence
    if confidence == "high":
        return "medium"
    return confidence


def _reviewer_calibration_block(calibration: dict[str, Any]) -> str:
    if not calibration or calibration.get("status") == "not_reviewed":
        return "- Not reviewed yet."
    lines = [
        f"- Status: `{calibration.get('status')}`",
        f"- Verdicts: `{calibration.get('verdict_counts', {})}`",
        f"- Reviewers: `{', '.join(calibration.get('reviewers', []))}`",
    ]
    action_items = calibration.get("action_items") or []
    if action_items:
        lines.append("- Action items:")
        lines.extend(f"  - {item}" for item in action_items)
    return "\n".join(lines)


def _evidence_bullets(evidence_refs: list[dict[str, Any]]) -> str:
    if not evidence_refs:
        return "- No evidence refs available."
    lines = []
    for ref in evidence_refs:
        synth = "synthetic-only" if ref.get("synthetic_only") else "pilot/anonymized"
        lines.append(
            f"- `{ref['id']}` {ref['source_kind']} · {ref['confidence']} · {synth} · {ref['claim']} · `{ref['source']}`"
        )
    return "\n".join(lines)


def _bullets(items: Any) -> str:
    if not items:
        return "- None."
    if isinstance(items, str):
        items = [items]
    return "\n".join(f"- {item}" for item in items)
