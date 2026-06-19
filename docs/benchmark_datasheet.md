# Benchmark Datasheet

Last updated: 2026-06-19

## Summary

This repository contains a synthetic benchmark and reference architecture for:

> Privacy-preserving AI coordination for schools and family-support workflows.

The benchmark tests whether a multi-party AI workflow can move from private
student/parent/teacher inputs to abstracted support signals, through a privacy
wall, into coordinator outputs, audience-safe reports, and human reviewer
annotation.

This datasheet documents provenance, intended use, non-use, privacy risks,
evaluation scripts, and current evidence boundaries. It follows the spirit of
dataset documentation practices such as datasheets for datasets, but it is not a
formal human-subjects dataset document because the corpus is synthetic.

## Motivation

Schools and student-support organizations often need coordination across
students, families, teachers, and reviewers. The hard part is not only making a
recommendation. It is deciding which support-relevant information can move
across roles without exposing raw disclosures or reconstructable private
details.

The benchmark exists to test this design question:

> Can an AI coordination pipeline preserve role-appropriate information flow
> while still producing useful, evidence-grounded support reports for human
> review?

## Composition

Current corpus snapshot:

- Synthetic conversations: 348
- Depth distribution from the latest audit:
  - deep: 85 (24.4%)
  - shallow: 142 (40.8%)
  - medium: 121 (34.8%)
- Scenario types include mundane help, moderate issue, mixed support needs,
  stress tests, privacy probes, privacy tests, and misuse attempts.

Important artifact groups:

- `data/generated_conversations/`: synthetic private conversations.
- `docs/persona_bible.md`: public-safe persona canon for the synthetic cases.
- `docs/relationship_graph.md`: synthetic family and school-side relationship
  map.
- `docs/persona_depth_audit.md`: current audit of persona depth, relationship
  depth, and known gaps.
- `data/case_summaries/`: internal case summaries.
- `data/audience_reports/parent_safe/`: parent-safe reports.
- `data/audience_reports/teacher_safe/`: teacher-safe reports.
- `data/audience_reports/internal_reviewer/`: restricted reviewer reports.
- `umi/reports/release-readiness-latest.md`: one-command Evidence v1 gate
  output.
- `umi/reports/baseline-comparison-latest.md`: raw baseline vs privacy-wall
  comparison report.
- `umi/reports/semantic-trace-audit-latest.md`: deterministic semantic trace
  overlap audit over the fixed sample's audience-safe report surfaces.
- `data/reviewer_notes/`: JSON reviewer annotations.
- `data/reviewer_summaries/reviewer_annotation_summary.md`: aggregate reviewer
  annotation summary.

## Data Source And Generation

The corpus is synthetic. It was generated for benchmark stress testing and
design iteration. It should not be interpreted as observed student behavior,
survey data, clinical evidence, or school deployment data.

Generation is currently paused. The active proof path is baseline comparison
plus human reviewer annotation, not additional synthetic corpus growth.

Persona and relationship assumptions are documented in
`docs/persona_bible.md` and `docs/relationship_graph.md`. These docs support
generation consistency and benchmark-sample selection. They do not turn the
corpus into real-family evidence or a representative demographic sample.

## Architecture Under Test

```text
private chats
  -> abstraction
  -> privacy wall
  -> coordinator
  -> audience-safe reports
  -> human reviewer annotation
```

The raw-coordinator baseline intentionally models a risky architecture where a
coordinator can see raw multi-party inputs. The privacy-wall pipeline models
abstraction, protected fields, report variants, leak audits, and human review.

## Intended Uses

Use this benchmark to:

- test privacy-boundary behavior in multi-party educational coordination;
- compare raw-coordinator and privacy-wall designs on a fixed synthetic sample;
- inspect whether audience-safe reports avoid raw quotes and reconstructable
  private details;
- calibrate reviewer judgments around safe, useful, evidence-grounded, and
  appropriately escalated outputs;
- support a GitHub-facing technical thesis or research prototype discussion.

## Non-Uses

Do not use this benchmark to claim:

- real-student validation;
- clinical validity;
- school deployment readiness;
- outcome improvement;
- safety for autonomous counseling or crisis intervention;
- evidence that synthetic disclosure rates match real students, families, or
  teachers.

Do not put real student, parent, teacher, school, or minor data through free
cloud development providers without a separate provider, consent, retention,
deletion, and reviewer-governance plan.

## Current Evidence v1

Latest verification snapshot:

- `.venv/bin/python scripts/run_release_readiness.py`: PASS. This one command
  reruns the current Evidence v1 checks and writes
  `umi/reports/release-readiness-latest.md/json`.
- `python3 scripts/audit_conversation_quality.py`: 348 conversations; deep 85
  (24.4%), shallow 142 (40.8%), medium 121 (34.8%); average 19.5 turns.
- `.venv/bin/python scripts/run_baseline_comparison.py`: 11 fixed sampled
  cases. Raw coordinator baseline reconstructability risk: 11/11 cases.
  Privacy-wall pipeline reconstructability risk: 0/11 cases under deterministic
  checks.
- `.venv/bin/python scripts/audit_audience_report_leaks.py --json
  umi/reports/audience-report-leak-audit-latest.json`: 18 pass / 0 fail.
- `.venv/bin/python scripts/run_semantic_trace_audit.py`: 22 pass / 0 fail
  across fixed-sample parent-safe and teacher-safe report surfaces.
- `.venv/bin/python scripts/run_relationship_leak_audit.py`: 18 pass / 0 fail
  across current parent-safe and teacher-safe report surfaces. This checks
  reconstructable persona and family-system markers documented in the persona
  bible and relationship graph.
- `.venv/bin/python scripts/run_runtime_trace_privacy_audit.py`: 51 pass / 0
  fail across generated runtime surfaces. This checks audience-safe artifacts,
  restricted reviewer/internal artifacts, pilot-run artifacts, and metadata-only
  audit logs under surface-specific privacy policies.
- `.venv/bin/python scripts/generate_reviewer_summary.py`: generated reviewer
  calibration and annotation summaries.
- `data/reviewer_summaries/reviewer_annotation_summary.md`: 37 notes / 22
  reviewed artifacts, including a second local reviewer pass over 15
  baseline/audience-report artifacts.
- `.venv/bin/python -m pytest -q`: 77 passed / 7 skipped.

Reviewer annotation v1 findings:

- Raw coordinator baseline is marked `privacy_concern`.
- Parent-safe and teacher-safe Michael reports are marked `safe`.
- Internal reviewer Michael report is marked `minor_issue` because restricted
  reviewer content must not be reused as parent-safe or teacher-safe output.
- The privacy-wall pipeline has 0 over-escalation flags and 0 under-escalation
  flags under the current deterministic heuristic.
- The current reviewer summary includes 26 `safe`, 3 `privacy_concern`, and 2
  `minor_issue` verdicts, plus legacy calibration verdicts.
- The second reviewer pass is local screening evidence, not an independent
  real-world validation study.

## Evaluation Scripts

Run the current evidence gate:

```bash
.venv/bin/python scripts/run_release_readiness.py
```

Primary outputs:

- `umi/reports/release-readiness-latest.md`
- `umi/reports/release-readiness-latest.json`
- `umi/reports/audience-report-leak-audit-latest.md`
- `umi/reports/semantic-trace-audit-latest.md`
- `umi/reports/relationship-leak-audit-latest.md`
- `umi/reports/runtime-trace-privacy-latest.md`
- `umi/reports/baseline-comparison-latest.md`
- `data/reviewer_summaries/reviewer_annotation_summary.md`

## Privacy And Safety Risks

Known risks:

- A raw coordinator can expose reconstructable private context.
- Audience-safe reports can become unsafe if internal reviewer details are
  copied across surfaces.
- Over-escalation heuristics can misread conditional reviewer guidance as
  student-risk language if the metric is too broad.
- Deterministic leak checks do not prove semantic privacy under all paraphrases.
- Human review can become rubber-stamping without evidence refs, uncertainty,
  and clear ownership.

Current mitigations:

- privacy-wall abstraction;
- parent-safe, teacher-safe, and internal-reviewer report separation;
- deterministic audience report leak audit;
- deterministic relationship-context leak audit over parent-safe and
  teacher-safe reports;
- deterministic runtime trace privacy audit over generated local artifacts;
- raw baseline vs privacy-wall comparison;
- reviewer note JSON with source paths, evidence refs, verdicts, privacy
  concerns, and action items;
- explicit synthetic-only claim boundary in public docs.

## Maintenance

Before using any current evidence claim, rerun:

```bash
.venv/bin/python scripts/run_release_readiness.py
```

If the corpus changes, do not cite old baseline or reviewer results as current
until reports and summaries are regenerated.

## Known Gaps

- No external independent reviewer pass yet.
- No real pilot evidence.
- No formal human-subjects study.
- No claim that the synthetic persona set is representative of real students,
  parents, teachers, or family systems.
- No Chinese-language literature review extension for family-school cultural
  context.
- No production observability or real deployment trace privacy audit. The
  current runtime trace privacy check is limited to generated local benchmark
  artifacts.
- No reviewer UI; current review is file- and JSON-note based.
- Future synthetic generation should be constrained by the persona bible and
  relationship graph rather than adding volume without design coverage.

## Citation / Reuse Boundary

Safe public wording:

> This repository provides a synthetic benchmark and reference architecture for
> testing privacy-preserving multi-party AI coordination. Evidence v1 compares a
> raw coordinator baseline against a privacy-wall pipeline and includes human
> reviewer annotations on a fixed synthetic sample.

Unsafe wording:

> This system is validated for real students, clinical support, or school
> deployment.
