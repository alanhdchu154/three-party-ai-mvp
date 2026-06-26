# Umi Workload

Last updated: 2026-06-25

This file holds one active Codex / cc worker handoff at a time.

## Active Task

Keep Evidence v1 publishable without expanding synthetic data or overstating
validation.

## Repo

`/Users/alanhdchu/three-party-ai-mvp`

## Objective

Current bounded lane:

1. use the refreshed public GitHub package for artifact-first external review;
2. invite one privacy/governance reviewer and one school/student-support
   operations reviewer;
3. review/push the ahead evidence-refresh branch when Alan wants the public repo
   updated;
4. update claim-boundary docs after real reviewer feedback.

## Current Evidence

- Synthetic generation is paused.
- 2026-06-25 evidence refresh: `audit_conversation_quality.py` reports 348
  conversations with depth counts 85 deep / 142 shallow / 121 medium.
- Evidence v1 already includes baseline comparison, local reviewer annotation,
  privacy/leak/trace audits, external reviewer packet, testing instructions, and
  internal dry-run review.
- `scripts/run_release_readiness.py` returned PASS after the public docs polish.
- `.venv/bin/python -m pytest -q` returned 89 passed / 7 skipped.
- A local intro video draft was generated at
  `public_video/three_party_intro_2026-06-25/three_party_intro_synthetic_benchmark.mp4`
  with `script.md` and `subtitles.srt`. It uses synthetic benchmark metrics
  only and does not include raw conversations or real student/family/school
  data.
- No external independent validation has been completed.
- Claude Code review was attempted with `--model sonnet`, but the CLI returned
  `Not logged in`; this pass was completed by Codex/Umi with deterministic
  release-readiness verification instead.

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
reviewer for external feedback, and review the local intro video draft before
any upload or external sharing. Do not create more synthetic conversations for
this outreach round.
