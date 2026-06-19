# External Review Agent Dry Run

Date: 2026-06-19

## Boundary

This is an internal AI-assisted dry run of the external review instructions.
It is not external independent validation, real-student validation, clinical
review, deployment readiness, or outcome evidence.

The goal was to stress-test whether outside reviewers would know what to test
before the repo is shared for broader GitHub or collaborator feedback.

## Reviewers Simulated

- Claude Code read-only review: external testing instruction critique.
- Privacy / AI governance reviewer agent.
- School / student-support operations reviewer agent.
- Research / HCI / learning analytics reviewer agent.

No synthetic data generation was performed.

## Main Findings

### 1. External Instructions Needed More Adversarial Privacy Tests

The first reviewer packet was directionally safe, but too open-ended.
Reviewers need explicit instructions to test:

- raw quote leakage;
- close paraphrase leakage;
- motivated-recipient reconstructability;
- cross-artifact triangulation;
- relationship-context leakage;
- copy/paste failure from restricted reviewer artifacts;
- parent/teacher interrogation risk.

Action taken:

- Added `docs/external_testing_instructions.md`.
- Added privacy and reconstructability exercises to the external test tracks.
- Added `docs/persona_bible.md` and `docs/relationship_graph.md` to the
  privacy-focused review path in `docs/external_reviewer_packet.md`.

### 2. School Operations Review Needed Its Own Rubric

A school-support reviewer should not only ask whether the output is private.
They should ask whether an adult can act without probing for hidden private
details.

Reviewers should test:

- owner: parent, teacher, counselor/reviewer, or administrator;
- next action;
- 24-72 hour low-risk actionability;
- escalation threshold;
- what not to ask the student;
- whether the report is safe but too generic;
- whether teacher-facing dimension labels reveal more than the audience needs.

Action taken:

- Added a School-Ops 30-minute review path to
  `docs/external_reviewer_packet.md`.
- Added usefulness/actionability criteria to
  `docs/external_testing_instructions.md`.

### 3. Research Review Needed Sampling And Annotation Caveats

The current 11-case baseline comparison is useful screening evidence, but not
a full research comparison. External reviewers should evaluate whether future
proof needs:

- stratified fixed sampling across persona, depth, scenario type,
  relationship-system risk, benign daily cases, privacy probes, and misuse
  cases;
- ablation comparisons beyond raw coordinator vs privacy wall;
- independent reviewer criteria;
- reviewer calibration examples;
- disagreement handling and agreement reporting.

Action taken:

- Added baseline fairness and methodology checks to
  `docs/external_testing_instructions.md`.
- Kept the current claim boundary synthetic-only.

### 4. GitHub Issue Template Needed Stronger Structured Fields

The issue template needed to make the highest-value feedback dimensions harder
to skip.

Action taken:

- Added test-track checkboxes.
- Added overall verdict dropdown using project verdict vocabulary.
- Added script/review-mode checkboxes.
- Made claim-boundary and privacy/safety concerns required.
- Added a required confidentiality confirmation.

### 5. Pilot-Gate Checklist Was Stale

`docs/reviewer_gate_checklist.md` still referenced the older 300-conversation
state and could confuse external review with pilot readiness.

Action taken:

- Updated it to the 2026-06-19 Evidence v1 state.
- Clarified that it is a stricter pilot-readiness checklist, while
  `docs/external_reviewer_packet.md` and
  `docs/external_testing_instructions.md` are the public synthetic-review
  path.

## Remaining Useful Work

- Update `docs/paper_draft.md` before asking academic reviewers to treat it as
  current.
- Add a future stratified baseline sample if moving from GitHub package to
  research-paper submission.
- Add two real external reviewers before investor, school, or pilot outreach.
- Keep production-grade runtime trace/privacy governance as a future pilot
  requirement.

