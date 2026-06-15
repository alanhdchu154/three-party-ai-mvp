# Three-Party AI Roadmap

Last updated: 2026-06-14

This roadmap keeps only the current product direction and open work. Completed
historical version ladders were removed from the active roadmap.

## Version Vocabulary

- Repo product version: `0.8.0-internal-pilot-harness`.
- Central Umi routing goal: `v0.1` for cross-project coordination.
- Do not treat Central Umi's `v0.1` label as a product downgrade; it describes
  the coordination layer, not the repo feature maturity.

## North Star

Build a research prototype and synthetic benchmark for privacy-preserving,
human-led, multi-party student support coordination.

Short term: define a publishable benchmark/system paper around synthetic
student-parent-teacher conversations, privacy-wall abstraction, coordinator
synthesis, triage guardrails, party-aware reporting, and reviewer evaluation.

## Current Research Position

- Active framing: research prototype + synthetic benchmark.
- GIIS/Jieni are no longer the active product framing. They remain historical
  context or possible future deployment settings, not current claims.
- The project does not claim that synthetic conversations represent real student
  behavior.
- The project is not a clinical tool, not automatic crisis intervention, and not
  a parent surveillance product.

## Active Work

### 0. Research Artifact Pack

- Initial research docs now exist:
  - `docs/research_positioning.md`
  - `docs/benchmark_spec.md`
  - `docs/evaluation_plan.md`
  - `docs/synthetic_data_limitations.md`
  - `docs/paper_outline.md`
- 2026-06-14 paper pass added:
  - `docs/benchmark_snapshot_2026-06-14.md`
  - `docs/evaluation_results_2026-06-14.md`
  - `docs/paper_draft.md`
- Next step: add a raw-coordinator baseline comparison and human reviewer
  annotations before treating the draft as submission-ready.

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
- 2026-06-05 Umi review added concrete pre-pilot safeguards in
  `docs/generation_logic.md`: reviewer acceptance gate, parent/teacher-safe
  leak audit, crisis handoff runbook, generation pause condition, and
  consent/deletion boundary.
- Parent/teacher-safe report leak audit now exists:
  `python3 scripts/audit_audience_report_leaks.py`. Current result is 18 pass /
  0 fail, saved at `umi/reports/audience-report-leak-audit-latest.md`.
- Reviewer gate checklist now exists at `docs/reviewer_gate_checklist.md`.

### 4. Reviewer UI / Annotation Flow

- Still useful future work: show coordination snapshots and reviewer notes in a
  practical review surface instead of relying only on generated files.
- Next non-human pilot-readiness item: wire the leak audit and reviewer gate
  into a broader release-readiness command if this project resumes.

## Deferred

- Broad SaaS positioning
- GIIS/Jieni-specific product pilot framing
- Unsupervised minor-data handling
- Automatic counseling or crisis response
- Claims based only on synthetic corpus behavior
- Adding more generated data when downstream reports are stale
- Expanding scheduled generation volume before the 2026-06-05 privacy /
  automation-risk safeguards are implemented or explicitly accepted

## Working Rule

When asked for current status:

1. Read `WORKLOG.md`.
2. Run `python3 scripts/audit_conversation_quality.py`.
3. Check whether downstream reports are newer than the corpus snapshot.
4. Report current evidence separately from historical notes.
