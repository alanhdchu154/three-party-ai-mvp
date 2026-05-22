"""Controlled internal pilot harness.

This harness does not run real conversations or call LLMs. It packages one
existing synthetic/local student case into an isolated run folder and records
auditable metadata for each step.
"""

from __future__ import annotations

import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any

from . import analysis_layer, audit_log, report_variants, reviewer_workflow, trajectory_model

PILOT_RUNS_DIR = analysis_layer.DATA_DIR / "pilot_runs"


def run_controlled_harness(
    student_id: str,
    *,
    run_id: str | None = None,
    output_dir: Path = PILOT_RUNS_DIR,
) -> Path:
    run_id = run_id or f"{student_id}_{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}"
    run_dir = output_dir / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    audit_path = run_dir / "audit_log.jsonl"

    corpus = analysis_layer.load_corpus()
    summary = analysis_layer.build_case_summary(student_id, corpus)
    trajectories = trajectory_model.apply_reviewer_calibration(
        {student_id: trajectory_model.detect_trajectories(student_id, corpus)}
    )[student_id]
    review_summary = reviewer_workflow.summarize_reviews()

    audit_log.append_event(audit_path, event_type="harness_started", payload={"student_id": student_id, "run_id": run_id})

    _write_json(run_dir / "case_summary.json", summary)
    audit_log.append_event(audit_path, event_type="case_summary_written", payload={"path": "case_summary.json"})

    for audience in sorted(report_variants.AUDIENCES):
        path = run_dir / f"{audience}.md"
        path.write_text(report_variants.render_case_variant(summary, audience), encoding="utf-8")
        audit_log.append_event(audit_path, event_type="audience_report_written", payload={"audience": audience, "path": path.name})

    trajectory_path = run_dir / "trajectory_report.md"
    trajectory_path.write_text(trajectory_model.render_trajectory_report(student_id, trajectories), encoding="utf-8")
    audit_log.append_event(audit_path, event_type="trajectory_report_written", payload={"path": trajectory_path.name})

    _write_json(run_dir / "reviewer_calibration.json", review_summary)
    audit_log.append_event(audit_path, event_type="reviewer_calibration_attached", payload={"review_notes": review_summary.get("n_notes", 0)})

    manifest = {
        "run_id": run_id,
        "student_id": student_id,
        "created_at": datetime.utcnow().isoformat() + "Z",
        "source_type": summary.get("source_type", "unknown"),
        "synthetic_only_warning": summary.get("synthetic_only_warning", True),
        "files": sorted(
            {path.name for path in run_dir.iterdir() if path.is_file()}
            | {"manifest.json"}
        ),
    }
    _write_json(run_dir / "manifest.json", manifest)
    audit_log.append_event(audit_path, event_type="harness_completed", payload={"manifest": "manifest.json"})
    return run_dir


def archive_run(run_dir: Path, archive_dir: Path | None = None) -> Path:
    archive_dir = archive_dir or run_dir.parent / "archived"
    archive_dir.mkdir(parents=True, exist_ok=True)
    target = archive_dir / run_dir.name
    if target.exists():
        raise FileExistsError(target)
    shutil.move(str(run_dir), str(target))
    return target


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
