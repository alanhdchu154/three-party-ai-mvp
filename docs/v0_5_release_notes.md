# v0.5 Synthetic Calibration Release

**Date:** 2026-05-21

## Current Version

`0.5.0-synthetic-calibration`

This is not a production or real-student pilot release. It is a synthetic benchmark and human-calibration release.

## What v0.5 Includes

- Privacy Wall v2 deterministic leakage checks.
- Cumulative Strain Triage v1.
- Demo / pilot / dev mode separation.
- Case Summary generation under `data/case_summaries/`.
- Trajectory Report generation under `data/trajectory_reports/`.
- Signal library and rule-based trajectory detection.
- Human reviewer notes under `data/reviewer_notes/`.
- Reviewer aggregation under `data/reviewer_summaries/reviewer_calibration_summary.md`.
- Calibrated trajectory reports that distinguish rule confidence from reviewer-adjusted confidence.

## Calibration Pass 1 Result

Representative cases reviewed:

- `case_summary:michael` — supported.
- `trajectory_report:michael:burnout_risk` — plausible true positive, medium confidence.
- `trajectory_report:michael:dependency_risk` — under-evidenced.
- `case_summary:rachel` — supported with privacy caveat.
- `trajectory_report:rachel:disclosure_collapse` — under-evidenced.
- `case_summary:shen_you` — privacy review needed.
- `trajectory_report:shen_you:hidden_disengagement` — plausible true positive, medium confidence.

## Go / No-Go

Go for:

- local synthetic demo,
- internal safety review,
- rule calibration,
- Umi / Alan benchmark discussion.

No-go for:

- real GIIS student data,
- parent-facing reports,
- teacher-facing reports,
- automated escalation without human review.

## Remaining Blockers Before Real Pilot

- Local/private provider path for real student data.
- Reviewer assignment and crisis SLA.
- Parent-safe / teacher-safe report variants.
- Source type migration for existing artifacts.
- Dimension snapshot backfill.
- Pilot onboarding and consent language.
- Manual privacy review of all user-facing surfaces.

## Next Recommended Step

Build v0.6 as a pilot-readiness pack:

- parent-safe / teacher-safe report variants,
- explicit reviewer assignment config,
- source-type and dimension snapshot migrations,
- pilot onboarding + consent checklist.

