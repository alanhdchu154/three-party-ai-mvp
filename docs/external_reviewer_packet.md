# External Reviewer Packet

Last updated: 2026-06-25

## Purpose

This packet is for outside reviewers who want to evaluate the repo as a public
synthetic benchmark and reference architecture:

> Privacy-preserving AI coordination layer for schools and family-support
> workflows.

The useful review question is narrow: does this project model a credible
privacy boundary for multi-party student-support coordination, and are the
current claims properly limited to synthetic-benchmark evidence?

This packet is not an institutional approval request, human-subjects study,
clinical review, or deployment sign-off.

Reviewers do not need to run the app, log in, upload data, or inspect private
systems. The safest first-round review is artifact-first: read the public docs
and reports, then leave file-linked feedback.

## Who Should Review

Useful reviewer lenses include:

- school operations, student support, counseling operations, or family-support
  workflows;
- LMS, SIS, EdTech, or student-success product teams;
- AI governance, privacy, security, or responsible-AI reviewers;
- HCI, learning analytics, education research, or child-safety researchers;
- people who have reviewed minor-data, family-data, or school-data workflows.

## What This Repo Is Testing

The architecture under review is:

```text
private chats
  -> abstraction
  -> privacy wall
  -> coordinator
  -> audience-safe reports
  -> human reviewer annotation
```

The central design claim is that a coordinator should not need raw private
student, parent, or teacher disclosures. It should coordinate over abstracted
support signals and produce reports that are safe for the intended audience.

## What To Read

For concrete task-by-task testing instructions, start with
`docs/external_testing_instructions.md`.

### 5-Minute Orientation

- `README.md`
- `umi/reports/release-readiness-latest.md`
- the `Claim Boundary` section in this packet

Use this path to decide whether the project is worth a deeper privacy,
operations, or research review.

### Quick 20-Minute Review

- `README.md`
- `docs/startup_thesis.md`
- `docs/benchmark_datasheet.md`
- `umi/reports/release-readiness-latest.md`

Use this path to check whether the public story, claim boundary, and evidence
summary make sense.

### Privacy-Focused 45-Minute Review

- `docs/human_reviewer_annotation_protocol.md`
- `docs/external_testing_instructions.md`
- `docs/persona_bible.md`
- `docs/relationship_graph.md`
- `umi/reports/baseline-comparison-latest.md`
- `umi/reports/semantic-trace-audit-latest.md`
- `umi/reports/relationship-leak-audit-latest.md`
- `umi/reports/runtime-trace-privacy-latest.md`
- `umi/reports/audience-report-leak-audit-latest.md`
- `data/reviewer_summaries/reviewer_annotation_summary.md`

Use this path to check whether parent-safe and teacher-safe outputs reveal too
much, become too vague to act on, or encourage unsafe follow-up behavior.

### School-Ops 30-Minute Review

- `docs/external_testing_instructions.md`
- `docs/reviewer_gate_checklist.md`
- parent-safe reports under `data/audience_reports/parent_safe/`
- teacher-safe reports under `data/audience_reports/teacher_safe/`
- `data/reviewer_summaries/reviewer_annotation_summary.md`

Use this path to check whether a parent, teacher, counselor/reviewer, or school
administrator can take a low-risk next step without probing for hidden private
details.

### Research / Paper 60-Minute Review

- `docs/literature_review.md`
- `docs/paper_draft.md`
- `docs/evaluation_plan.md`
- `docs/benchmark_spec.md`
- `docs/synthetic_data_limitations.md`
- `docs/persona_bible.md`
- `docs/relationship_graph.md`
- `docs/persona_depth_audit.md`

Use this path to check whether the benchmark framing, evaluation plan, persona
layer, and limitations are coherent enough for a public technical paper draft.

## What To Evaluate

Good review feedback usually answers one or more of these questions:

- Does the README or thesis overclaim beyond synthetic benchmark evidence?
- Does the privacy-wall architecture separate raw disclosure from coordination
  in a way that is understandable and auditable?
- Do audience-safe reports avoid raw quotes, reconstructable private details,
  and cross-party leakage?
- Are reports still useful enough for a human reviewer to act on?
- Does the baseline comparison fairly contrast raw coordination risk against
  privacy-wall coordination?
- Are deterministic audits useful as regression gates, or are important privacy
  failures still untested?
- Are reviewer verdicts and annotation protocols clear enough for a second
  independent reviewer?
- What evidence would be required before this could responsibly move toward a
  real pilot?

Reconstructability should be tested broadly: not only exact quote leakage, but
also close paraphrases, unique family-system markers, role-specific context,
copy/paste failure, and cross-artifact triangulation that could reveal
protected synthetic disclosures.

## Reviewer Verdicts

When reviewing a concrete artifact, use the project verdict vocabulary:

- `safe`
- `minor_issue`
- `privacy_concern`
- `over_escalated`
- `under_escalated`
- `under_evidenced`
- `not_actionable`

For issue-level feedback, include severity in plain language:

- `blocker`: should block public outreach or pilot discussion;
- `major`: should be fixed before broad GitHub sharing;
- `minor`: improves clarity or reviewability;
- `question`: needs judgment, but may not require an immediate change.

## Claim Boundary

It is appropriate to say this repo has:

- a synthetic benchmark;
- a reference architecture;
- deterministic privacy and release-readiness gates;
- baseline comparison evidence;
- local human-review annotation evidence;
- public documentation of benchmark limits and non-uses.

It is not appropriate to infer:

- real-student validation;
- clinical validity;
- deployment readiness for minors;
- school, family, retention, learning, or mental-health outcome improvement;
- proof that synthetic disclosure patterns match real school communities;
- external independent validation, until outside reviewers have actually
  completed and recorded review.

## Confidentiality Boundary

Do not upload real student, parent, teacher, school, clinical, or family data
into this repository.

Do not paste private transcripts, identifiable incidents, student records,
school records, API keys, screenshots of private systems, or confidential
review notes into GitHub issues.

Public feedback should refer to file paths, report IDs, case IDs, evidence IDs,
and abstract risk descriptions.

## How To Leave Feedback

Open a GitHub issue using the `External Review` template. Include:

- reviewer lens;
- review track;
- artifacts reviewed;
- short summary;
- highest-severity findings first;
- claim-boundary concerns;
- privacy or safety concerns;
- recommended next step.

If feedback depends on private professional context, summarize only the
generalizable lesson in public and keep confidential details out of the issue.

External reviewers should use GitHub issues for public feedback. The local
`scripts/add_reviewer_note.py` workflow is for internal annotation passes and
should not be required for outside review.
