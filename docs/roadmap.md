# Three-Party AI Roadmap

Last updated: 2026-05-31

This roadmap keeps only the current product direction and open work. Completed
historical version ladders were removed from the active roadmap.

## North Star

Build a privacy-preserving truth-capture and support-coordination layer for
online education.

Short term: validate in the GIIS context that students, parents, and teachers
can each tell AI more honest information, and that a coordinator can translate
patterns into safe support actions without exposing raw secrets.

## Current Product Position

- GIIS is the first controlled proof point.
- Jieni can be an optional support destination when the case fits academic
  coaching, study planning, learning gaps, exam pressure, or 1-on-1 mentoring.
- The product is not a clinical tool, not automatic crisis intervention, and not
  a parent surveillance product.

## Active Work

### 1. Current Corpus Health

- Scheduled generation can change counts hourly.
- Always run `python3 scripts/audit_conversation_quality.py` before reporting
  corpus numbers.
- Keep deep/shallow/medium balance from drifting back into all-deep psychology
  theater.

### 2. Downstream Report Freshness

- Ensure case summaries, audience reports, analysis reports, and dimension
  scores are regenerated only from the current intended corpus.
- Do not claim pilot readiness from stale reports.

### 3. Pilot Readiness Boundary

- Before any real student/family pilot, confirm provider/data boundary,
  reviewer ownership, consent/onboarding, deletion procedure, and Level 2/3
  human escalation flow.
- Parent-safe and teacher-safe outputs must never leak raw student secrets or
  another party's private constraints.

### 4. Reviewer UI / Annotation Flow

- Still useful future work: show coordination snapshots and reviewer notes in a
  practical review surface instead of relying only on generated files.

## Deferred

- Broad SaaS positioning
- Unsupervised minor-data handling
- Automatic counseling or crisis response
- Claims based only on synthetic corpus behavior
- Adding more generated data when downstream reports are stale

## Working Rule

When asked for current status:

1. Read `WORKLOG.md`.
2. Run `python3 scripts/audit_conversation_quality.py`.
3. Check whether downstream reports are newer than the corpus snapshot.
4. Report current evidence separately from historical notes.
