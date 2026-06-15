# Umi Workload

Last updated: 2026-06-11

This file holds one active Codex / cc worker handoff at a time. The previous 2026-05-21
single-conversation handoff is stale and was removed from the active board.

## Active Task

None.

## Before Creating The Next Task

- Read `/Users/alanhdchu/umi-central/goals.md`.
- Read this repo's `WORKLOG.md`.
- Read this repo's durable roadmap at `docs/roadmap.md` when direction or
  pilot-readiness scope matters.
- Run `python3 scripts/audit_conversation_quality.py` before using corpus
  numbers.
- Current corpus evidence is 344 conversations from the 2026-06-11 22:49 CDT
  audit. The project is now framed as a research prototype / synthetic benchmark
  rather than a GIIS/Jieni pilot. The downstream reports were last fully
  refreshed for the 300-case 2026-06-04 snapshot, so report freshness is stale
  until an intended benchmark snapshot is frozen and reports/tables are
  regenerated from that snapshot.
- Prefer `cc-first` or `Split-work` for bounded script fixes, audit review,
  report regeneration, and test runs.

## Likely Next Handoff

If work resumes, create a focused task for:

- freezing an intended benchmark snapshot,
- regenerating downstream reports and evaluation tables from that snapshot,
- rerunning `.venv/bin/python -m pytest -q`,
- using `docs/paper_outline.md` plus `docs/research_positioning.md` to draft
  the first paper version,
- preserving synthetic-data limitations and avoiding real-student validation
  claims.

Do not create a handoff for more synthetic generation until the benchmark
snapshot and report/table regeneration path are explicit.
