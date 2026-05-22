# Umi Task Workflow

Umi coordinates course-pipeline tasks by keeping Codex as the main planning and engineering agent while using Claude Code as a focused content worker.

## Intended Flow

1. Alan discusses goals with Codex.
2. Codex writes or updates `workload.md`.
3. Umi runs the workload through worker CLIs.
4. Claude Code generates content drafts.
5. Codex reviews accuracy, objectives, tone, pacing, and integration risk.
6. Umi saves a markdown report under `umi/reports/`.
7. Alan approves before any final lesson files are changed.

## Status Values

- `DRAFT`: still being shaped by Alan and Codex.
- `READY_FOR_CLAUDE`: ready for Claude Code content drafting.
- `CLAUDE_RUNNING`: Claude Code run is in progress.
- `CLAUDE_DONE`: Claude Code has produced draft output.
- `READY_FOR_CODEX_REVIEW`: ready for Codex review.
- `CODEX_REVIEW_DONE`: Codex has reviewed the draft.
- `APPROVED_FOR_INTEGRATION`: Alan approved changes to final lesson files.
- `ARCHIVED`: task is complete or no longer active.

## Safety Defaults

- Workers are read-only by default.
- `--write` is required before worker prompts may ask for file modifications.
- `--upload` is required before worker prompts may ask for uploads, YouTube, publishing, or external delivery.
- Umi itself may write reports under `umi/reports/`.
- Do not delete files through Umi.
- Do not call paid APIs through Umi.

## Typical Commands

```bash
python umi/orchestrator.py run workload.md
python umi/orchestrator.py run workload.md --write
python umi/orchestrator.py run workload.md --upload
```

You can also pass a one-line task directly:

```bash
python umi/orchestrator.py "inspect week 3 module"
```

Direct task mode is useful for quick inspection. For course content production, prefer `workload.md`.
