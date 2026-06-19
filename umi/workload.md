# Umi Workload

Last updated: 2026-06-19

This file holds one active Codex / cc worker handoff at a time. The previous 2026-05-21
single-conversation handoff is stale and was removed from the active board.

## Active Task

GitHub publication readiness after Evidence v1 release gate.

Current worker should not generate new synthetic conversations. The first
baseline comparison and human reviewer annotation pass now exists. Use the
existing 348-case corpus, `scripts/run_baseline_comparison.py`, and
`data/reviewer_summaries/reviewer_annotation_summary.md` to keep GitHub / paper
claims bounded. README now includes an `Evidence v1` section, and
`docs/benchmark_datasheet.md` documents provenance, intended use, non-use,
risks, and maintenance rules. The baseline over-escalation heuristic has been
calibrated so conditional reviewer boilerplate is not treated as high-severity
escalation in shallow cases.

The one-command release-readiness gate now exists:

```bash
.venv/bin/python scripts/run_release_readiness.py
```

It reruns corpus audit, baseline comparison, reviewer summary generation,
audience-report leak audit, semantic trace audit, full pytest, public
claim-boundary scan, and git-visible secret scan. The latest report is
`umi/reports/release-readiness-latest.md`.

## Before Creating The Next Task

- Read `/Users/alanhdchu/umi-central/goals.md`.
- Read this repo's `WORKLOG.md`.
- Read this repo's durable roadmap at `docs/roadmap.md` when direction or
  pilot-readiness scope matters.
- Run `python3 scripts/audit_conversation_quality.py` before using corpus
  numbers.
- Current corpus evidence is 348 conversations from the 2026-06-19 audit:
  deep 85 (24.4%), shallow 142 (40.8%), medium 121 (34.8%). The project is
  framed as a synthetic benchmark / reference architecture and GitHub-first
  technical asset, not a real-student pilot claim.
- Reviewer annotation v1 exists: 37 notes / 22 reviewed artifacts, including a
  second local reviewer pass over 15 baseline/audience-report artifacts.
  New-style verdicts are 26 `safe`, 3 `privacy_concern`, and 2 `minor_issue`.
  Treat this as screening evidence, not deployment validation.
- Semantic trace audit exists: 22 pass / 0 fail across fixed-sample parent-safe
  and teacher-safe report surfaces.
- Current calibrated baseline metrics on the 11-case sample: raw baseline
  reconstructability risk 11/11; privacy-wall pipeline 0 reconstructability
  risk, 0 over-escalation flags, 0 under-escalation flags, and 0 unsupported
  recommendation flags.
- Prefer `cc-first` or `Split-work` for bounded script fixes, audit review,
  report regeneration, and test runs.

## Likely Next Handoff

If work resumes, create a focused task for:

- final public GitHub push/PR packaging if Alan wants Codex to commit/push;
- optionally adding an external independent reviewer pass before investor or
  school outreach;
- optionally expanding privacy evaluation beyond deterministic semantic trace
  overlap into stronger semantic privacy checks;
- rerunning `.venv/bin/python scripts/run_release_readiness.py`;
- preserving synthetic-data limitations and avoiding real-student validation
  claims.

Do not create a handoff for more synthetic generation until Alan explicitly
reopens generation.
