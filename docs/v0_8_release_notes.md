# v0.8 Internal Pilot Harness Release Notes

**Version**: `0.8.0-internal-pilot-harness`  
**Date**: 2026-05-21

v0.8 moves the repo from synthetic calibration into a controlled internal pilot rehearsal. It still does not run real families, and it does not generate new synthetic conversations.

## Completed

- Added audience-safe case reports:
  - `internal_reviewer`
  - `parent_safe`
  - `teacher_safe`
- Added controlled pilot harness:
  - isolated one-student run folders under `data/pilot_runs/`
  - case summary
  - audience-safe reports
  - trajectory report
  - reviewer calibration attachment
  - append-only JSONL audit log
- Added reviewer-note CLI support so reviewers do not need to hand-write JSON.
- Added provider safety documentation and `.env.example` mode/provider warnings.
- Added source-type migration and dimension snapshot backfill scripts.
- Added pilot onboarding checklist and reviewer assignment example config.
- Added tests for audience variants, audit logging, and pilot harness behavior.

## Smoke Run

Generated a controlled internal harness run:

`data/pilot_runs/v0_8_smoke_michael/`

Leak scan over `data/audience_reports/` and the smoke run found no direct hits for checked raw seed / secret truth / do-not-share phrases.

## Still Not Pilot Ready

This is still **not** ready for real student deployment until:

- Alan assigns a primary and backup human reviewer.
- Level 3 crisis handoff is tabletop-tested.
- Real-data provider path is confirmed.
- Consent, opt-out, and deletion procedure are finalized.
- At least one full dry run is reviewed by a human without using raw secrets.

## Recommendation

Move next to v0.9 only after the human operation layer is explicit. The code can rehearse a pilot now; the organization still needs reviewer ownership and family-facing protocol.
