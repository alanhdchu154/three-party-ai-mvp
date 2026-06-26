# WORKLOG - Three-Party AI Current Evidence

Last updated: 2026-06-25

This file is for current coordination only. Detailed pre-slimming worklog state
is archived at `docs/archive/WORKLOG_DETAIL_2026-06-24-pre-slim.md`.

## Usage

1. Run `python3 scripts/audit_conversation_quality.py` before reporting current
   corpus numbers.
2. Run `.venv/bin/python scripts/run_release_readiness.py` before release,
   public GitHub, pilot-readiness, or paper-ready claims.
3. Do not restart synthetic generation unless Alan explicitly reopens that lane.
4. Treat internal Claude/reviewer-agent dry runs as pre-review QA, not external
   independent validation.

## Current State

- The project is a synthetic benchmark / reference architecture, not a
  real-student validation claim.
- Synthetic generation is paused.
- Existing Evidence v1 artifacts include baseline comparison, local reviewer
  annotation, privacy/trace/leak audits, external reviewer packet, external
  testing instructions, GitHub issue template, and simulated/internal dry-run
  review.
- 2026-06-25 public GitHub readiness polish is complete: README now has a
  5-minute reviewer path and "How To Help" section; reviewer packet/outreach
  now make artifact-first review explicit; startup thesis Evidence v1 numbers
  are current; datasheet/testing/checklist dates are refreshed; and the external
  review issue template includes a school/student-support workflow path.
- 2026-06-25 local intro video draft was generated from synthetic benchmark
  data only at `public_video/three_party_intro_2026-06-25/`. Output MP4:
  `three_party_intro_synthetic_benchmark.mp4`; sidecars: `script.md`,
  `subtitles.srt`, and render README. It uses Evidence v1 metrics and repeats
  the synthetic-only / no deployment-readiness boundary.
- The current Evidence v1 gate was rerun after the doc polish and returned
  PASS. Current corpus audit remains 348 conversations with depth counts 85
  deep / 142 shallow / 121 medium; pytest remains 89 passed / 7 skipped.
- The ahead branch contains evidence-refresh work that should be reviewed/pushed
  only when useful.

## Open Follow-Ups

| # | Item | Owner | Status |
|---|---|---|---|
| 1 | Invite one privacy/governance reviewer and one school/student-support operations reviewer for artifact-first external feedback. | Alan / Codex | ready |
| 2 | Review the local intro video draft before any public upload or external sharing. | Alan / Codex | ready |
| 3 | Rerun full release-readiness before any further public GitHub, pilot-readiness, or paper-ready claim change. | Codex or cc | active rule; last PASS 2026-06-25 |
| 4 | Keep synthetic corpus generation paused unless Alan explicitly reopens generation. | Codex / Umi | active rule |
| 5 | Revoke any previously exposed Gemini / Groq / GitHub PAT secrets if not already done outside this repo. | Alan | open |
| 6 | Clean generated/cache artifacts only after confirming they are not needed for audit/repro. | Codex | deferred |

## Current Reporting Rule

Any answer about current corpus state must include:

- audit command run
- generated corpus count
- depth distribution
- whether downstream reports were refreshed after that snapshot
- whether the statement is current evidence or historical context

## Claim Boundary

Allowed: public synthetic-benchmark / reference-architecture discussion with
clear limitations.

Blocked without stronger evidence: real-student validity, clinical validity,
deployment readiness, outcome improvement, or claims of external independent
validation.
