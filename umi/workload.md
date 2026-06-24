# Umi Workload

Last updated: 2026-06-24

This file holds one active Codex / cc worker handoff at a time.

## Active Task

Keep Evidence v1 publishable without expanding synthetic data or overstating
validation.

## Repo

`/Users/alanhdchu/three-party-ai-mvp`

## Objective

If work resumes, choose one bounded lane:

1. rerun release-readiness for a public/GitHub claim;
2. prepare external reviewer outreach;
3. review/push the ahead evidence-refresh branch;
4. update claim-boundary docs after real reviewer feedback.

## Current Evidence

- Synthetic generation is paused.
- Existing corpus evidence must be refreshed with
  `python3 scripts/audit_conversation_quality.py` before current counts are
  reported.
- Evidence v1 already includes baseline comparison, local reviewer annotation,
  privacy/leak/trace audits, external reviewer packet, testing instructions, and
  internal dry-run review.
- No external independent validation has been completed.

## Constraints

- Do not create more synthetic conversations unless Alan explicitly asks.
- Do not claim real-student validation, clinical validity, deployment
  readiness, or outcome improvement.
- Do not expose or commit secrets, real student/family data, private school
  records, or reviewer personal data.
- Treat `Umi`, `ReviewerB`, Claude Code, and reviewer agents as internal
  AI-assisted/local screening labels unless real external reviewers are
  documented.

## Suggested Verification

Before public or release claims:

```bash
python3 scripts/audit_conversation_quality.py
.venv/bin/python scripts/run_release_readiness.py
```

Then inspect the latest report and git diff before committing or pushing.

## Likely Next Handoff

Ask one privacy/governance reviewer and one school/student-support operations
reviewer for external feedback, or rerun the release-readiness gate if Alan
wants to publish/update the GitHub-facing package.
