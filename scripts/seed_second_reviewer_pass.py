"""Seed a bounded second reviewer pass for the public Evidence v1 sample.

This creates local reviewer notes for the fixed baseline sample and three
audience-report variants when they do not already have a `ReviewerB` note.
It does not call an LLM and does not turn synthetic evidence into real-world
validation.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts import run_baseline_comparison
from src import reviewer_workflow

ROOT = Path(__file__).resolve().parent.parent
BASELINE_JSON = ROOT / "umi" / "reports" / "baseline-comparison-latest.json"
REVIEWER = "ReviewerB"


def existing_reviewed_keys() -> set[tuple[str, str, str]]:
    keys: set[tuple[str, str, str]] = set()
    for note in reviewer_workflow.load_review_notes():
        keys.add((note["artifact_type"], note["artifact_id"], note["reviewer"]))
    return keys


def build_notes() -> list[dict[str, Any]]:
    baseline = json.loads(BASELINE_JSON.read_text(encoding="utf-8"))
    notes: list[dict[str, Any]] = [
        reviewer_workflow.build_review_note(
            artifact_type="baseline_comparison",
            artifact_id="raw_coordinator_baseline",
            reviewer=REVIEWER,
            verdict="privacy_concern",
            confidence="high",
            source_path="umi/reports/baseline-comparison-latest.json",
            evidence_ref_ids=["baseline:raw_coordinator", "metric:reconstructability_risk_cases"],
            comments=(
                "Second-pass review agrees that direct raw-input coordination is an unsafe "
                "baseline for audience-facing workflows."
            ),
            privacy_concerns=[
                "Raw baseline preserves private turns and scenario metadata in a reconstructable form."
            ],
            action_items=[
                "Keep raw-input coordinator results as a negative baseline only."
            ],
        )
    ]

    for case in baseline.get("cases", []):
        privacy_wall = case.get("privacy_wall_pipeline", {})
        has_flags = any(
            privacy_wall.get(key)
            for key in (
                "reconstructability_risk",
                "over_escalation_flag",
                "under_escalation_flag",
                "recommendation_without_evidence_flag",
                "missing_audience_report",
            )
        )
        notes.append(
            reviewer_workflow.build_review_note(
                artifact_type="baseline_comparison",
                artifact_id=case["case_id"],
                reviewer=REVIEWER,
                verdict="minor_issue" if has_flags else "safe",
                confidence="medium",
                source_path="umi/reports/baseline-comparison-latest.json",
                evidence_ref_ids=[
                    f"baseline_case:{case['case_id']}",
                    f"depth:{case['depth']}",
                    "metric:privacy_wall_pipeline",
                ],
                comments=(
                    "Second-pass check reviewed the privacy-wall metrics and report paths for "
                    "this fixed sample case. The judgment is synthetic-screening evidence only."
                ),
                privacy_concerns=[] if not has_flags else ["Privacy-wall case has deterministic flags."],
                action_items=[
                    "Keep this case in future public-readiness gates."
                ],
            )
        )

    notes.extend(_audience_report_notes())
    return notes


def _audience_report_notes() -> list[dict[str, Any]]:
    return [
        reviewer_workflow.build_review_note(
            artifact_type="audience_report",
            artifact_id="parent_safe:michael",
            reviewer=REVIEWER,
            verdict="safe",
            confidence="medium",
            source_path="data/audience_reports/parent_safe/michael.md",
            evidence_ref_ids=["report:parent_safe:michael", "surface:parent_safe"],
            comments=(
                "Second-pass review finds the parent-safe report appropriately abstract for "
                "the current synthetic benchmark surface."
            ),
            action_items=["Keep parent-safe and internal-reviewer surfaces separated."],
        ),
        reviewer_workflow.build_review_note(
            artifact_type="audience_report",
            artifact_id="teacher_safe:michael",
            reviewer=REVIEWER,
            verdict="safe",
            confidence="medium",
            source_path="data/audience_reports/teacher_safe/michael.md",
            evidence_ref_ids=["report:teacher_safe:michael", "surface:teacher_safe"],
            comments=(
                "Second-pass review finds the teacher-safe report useful without exposing "
                "raw private turns."
            ),
            action_items=["Keep teacher-safe reports focused on classroom support actions."],
        ),
        reviewer_workflow.build_review_note(
            artifact_type="audience_report",
            artifact_id="internal_reviewer:michael",
            reviewer=REVIEWER,
            verdict="minor_issue",
            confidence="medium",
            source_path="data/audience_reports/internal_reviewer/michael.md",
            evidence_ref_ids=["report:internal_reviewer:michael", "surface:internal_reviewer"],
            comments=(
                "Second-pass review agrees this restricted report is useful for reviewers "
                "but should not be reused as parent-safe or teacher-safe output."
            ),
            privacy_concerns=[
                "Internal reviewer content contains detail that belongs behind the restricted review boundary."
            ],
            action_items=["Preserve restricted internal-reviewer labeling in public docs and examples."],
        ),
    ]


def main() -> int:
    existing = existing_reviewed_keys()
    created: list[Path] = []
    skipped = 0
    for note in build_notes():
        key = (note["artifact_type"], note["artifact_id"], note["reviewer"])
        if key in existing:
            skipped += 1
            continue
        created.append(reviewer_workflow.save_review_note(note))
        existing.add(key)

    print(f"Second reviewer pass: {len(created)} created / {skipped} skipped")
    for path in created:
        print(f"- {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
