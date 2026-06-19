# Three-Party AI Roadmap

Last updated: 2026-06-19

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

Short term: package the repo as a credible GitHub-first technical asset and
define a publishable benchmark/system paper around synthetic
student-parent-teacher conversations, privacy-wall abstraction, coordinator
synthesis, triage guardrails, party-aware reporting, baseline comparison, and
reviewer evaluation.

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
- 2026-06-18 literature pass added:
  - `docs/literature_review.md`
- 2026-06-19 benchmark datasheet added:
  - `docs/benchmark_datasheet.md`
- Next step: use the raw-coordinator baseline comparison and human reviewer
  annotation v1 to tighten the paper/README claims before treating the draft as
  public or submission-ready.

### 0.5 GitHub Thesis + Proof Layer

- Public-facing thesis:
  `Privacy-preserving AI coordination layer for schools and family-support workflows`.
- GitHub positioning docs now exist:
  - `docs/startup_thesis.md`
  - `docs/literature_review.md`
  - `docs/benchmark_datasheet.md`
  - `docs/baseline_comparison_plan.md`
  - `docs/human_reviewer_annotation_protocol.md`
- First deterministic baseline scaffold now exists:
  - `scripts/run_baseline_comparison.py`
  - `umi/reports/baseline-comparison-latest.json`
  - `umi/reports/baseline-comparison-latest.md`
- One-command Evidence v1 release gate now exists:
  - `scripts/run_release_readiness.py`
  - `umi/reports/release-readiness-latest.json`
  - `umi/reports/release-readiness-latest.md`
- Semantic trace audit now exists:
  - `scripts/run_semantic_trace_audit.py`
  - `umi/reports/semantic-trace-audit-latest.json`
  - `umi/reports/semantic-trace-audit-latest.md`
- Human reviewer annotation v1 now exists:
  - `data/reviewer_summaries/reviewer_annotation_summary.md`
  - `data/reviewer_notes/baseline_comparison__*.json`
  - `data/reviewer_notes/audience_report__*.json`
- Second local reviewer pass now exists over the fixed 11-case baseline sample
  plus 3 audience-report variants. This is screening evidence only, not an
  external independent validation study.
- The baseline + reviewer annotation pass is screening evidence only. It can
  support a public synthetic-benchmark claim, but not real-student validation,
  clinical validity, deployment readiness, or outcome improvement.
- 2026-06-19 calibration fix: shallow conditional reviewer guidance is no
  longer counted as high-severity over-escalation in the deterministic baseline
  heuristic. Current privacy-wall baseline metrics are 0 reconstructability-risk
  cases, 0 over-escalation flags, 0 under-escalation flags, and 0
  recommendation-without-evidence flags on the 11-case sample.

### 1. Current Corpus Health

- Scheduled generation is paused as of 2026-06-18. Do not restart synthetic
  corpus growth unless Alan explicitly reopens generation.
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
- Semantic trace audit now exists:
  `.venv/bin/python scripts/run_semantic_trace_audit.py`. Current result is 22
  pass / 0 fail across fixed-sample parent-safe and teacher-safe report
  surfaces.
- Reviewer gate checklist now exists at `docs/reviewer_gate_checklist.md`.

### 4. Reviewer UI / Annotation Flow

- Still useful future work: show coordination snapshots and reviewer notes in a
  practical review surface instead of relying only on generated files.
- Next technical packaging items after GitHub publication: optional external
  reviewer, stronger semantic privacy evaluation, and a practical reviewer UI.

## Deferred

- Broad SaaS positioning
- GIIS/Jieni-specific product pilot framing
- Unsupervised minor-data handling
- Automatic counseling or crisis response
- Claims based only on synthetic corpus behavior
- Adding more generated data when downstream reports are stale
- Adding more generated data while baseline comparison and human review are the
  active proof bottleneck
- Expanding scheduled generation volume before the 2026-06-05 privacy /
  automation-risk safeguards are implemented or explicitly accepted

## Working Rule

When asked for current status:

1. Read `WORKLOG.md`.
2. Run `python3 scripts/audit_conversation_quality.py`.
3. Check whether downstream reports are newer than the corpus snapshot.
4. Report current evidence separately from historical notes.
