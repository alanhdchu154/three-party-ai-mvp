# Simulated External Panel Review

Date: 2026-06-19

## Boundary

This is an AI-assisted simulated external panel review. It is not external
independent validation, legal advice, clinical review, school procurement
review, deployment approval, real-student validation, or outcome evidence.

The purpose is to pressure-test what outside reviewers might notice before Alan
invites real privacy/governance, school-operations, research, or partner
reviewers.

## Review Surface

The simulated panel reviewed public and proof-facing repo artifacts including:

- `README.md`
- `docs/external_reviewer_packet.md`
- `docs/external_testing_instructions.md`
- `docs/external_reviewer_outreach.md`
- `docs/external_review_agent_dry_run_2026-06-19.md`
- `docs/benchmark_datasheet.md`
- `docs/reviewer_gate_checklist.md`
- `docs/paper_draft.md`
- `docs/evaluation_plan.md`
- `docs/synthetic_data_limitations.md`
- `umi/reports/release-readiness-latest.md`
- `umi/reports/baseline-comparison-latest.md`
- `data/reviewer_summaries/reviewer_annotation_summary.md`
- sample parent-safe, teacher-safe, and internal-reviewer reports.

## Simulated Panel Roles

- Privacy / AI governance reviewer.
- School counselor / student-support operations reviewer.
- HCI / learning analytics / benchmark methodology reviewer.
- Skeptical buyer / partner reviewer.
- Claude Code read-only synthesis pass.

## Overall Verdict

`PASS_WITH_LIMITS` for public GitHub sharing as a synthetic benchmark and
reference architecture.

`BLOCKED` for real school-support workflow claims, pilot-readiness claims,
clinical claims, investor proof claims, or academic-paper-ready benchmark
claims.

## Cross-Cutting Findings

### Blockers For Investor, School, Or Pilot Outreach

- No real external human reviewer has completed a review track yet.
- No named Level 2 / Level 3 escalation owner, backup reviewer, SLA, or handoff
  channel exists in the public proof package.
- Consent, opt-out, deletion, provider boundary, and crisis handoff remain
  future governance requirements.
- The repo must not use passing synthetic checks as proof of real minor-data
  readiness.

### Blockers For Academic Review

- The current 11-case baseline is a fixed screening sample, not a held-out
  benchmark evaluation split.
- The raw baseline is intentionally unsafe, so the comparison is a useful
  negative control but not a full ablation study.
- The current baseline sample is concentrated in a small number of personas.
- Independent human annotation, codebook, calibration examples, disagreement
  handling, and agreement reporting are not complete.
- The paper draft needs to stay aligned with Evidence v1 metrics and must label
  current results as preliminary deterministic screening.

### Major Privacy / Governance Issues

- Teacher-safe reports may leak category-level signals through dimension labels
  such as family dynamics, identity, financial pressure, or academic load.
- Deterministic audits are credible regression checks, but they do not prove
  semantic privacy under paraphrase, motivated-recipient inference, or
  cross-artifact triangulation.
- Internal reviewer reports are useful but copy/paste dangerous. Any
  internal-to-audience reuse must pass through a rewrite/sanitization layer.
- `pilot` terminology can create ambiguity unless it remains clearly labeled as
  synthetic local harness planning, not real deployment readiness.

### Major School-Operations Issues

- Parent-safe reports are often safe by being generic, but may be too vague for
  real support operations.
- Reports need clearer owner, next action, time window, escalation threshold,
  and "what not to ask the student" language before any school workflow claim.
- Confidence labels in audience-safe reports can be misread as real
  student-support confidence. Future wording should distinguish synthetic
  artifact confidence from operational confidence.

### Methodology Issues

- Current evidence is strong enough for GitHub/workshop discussion, but not for
  an academic-ready benchmark claim.
- The next research upgrade is stratified sampling, ablation baselines, and
  independent reviewer agreement, not more synthetic volume.
- Cultural-context claims should stay careful until bilingual / China-context
  literature support is added.

## What Is Credible Now

- The public claim boundary is disciplined and repeated across README,
  datasheet, reviewer packet, testing instructions, and release reports.
- The architecture is understandable: private chats -> abstraction -> privacy
  wall -> coordinator -> audience-safe reports -> reviewer annotation.
- The deterministic audit stack is reproducible and layered.
- The external reviewer packet, testing instructions, and outreach kit are
  usable by real reviewers.
- The repo is ready for first-round real external review.

## Adopted Fixes From This Simulated Review

- Reviewer summaries now disclose that `Umi` is an AI-assisted internal reviewer
  label and `ReviewerB` is a local second-reviewer screening label.
- The benchmark datasheet now records the reviewer identity boundary.
- The paper draft now reflects 89 passed / 7 skipped tests, 37 notes / 22
  artifacts, and the reviewer identity boundary.
- Paper wording now says the privacy-wall pipeline passed deterministic
  screening checks, not that privacy is proven.

## Recommended Next Actions

1. Invite one real privacy / AI governance reviewer and one real school-support
   operations reviewer using `docs/external_reviewer_outreach.md`.
2. Run a motivated-recipient reconstructability exercise and record findings.
3. Replace teacher-facing dimension labels with less revealing operational
   language, or test whether they leak category-level private concerns.
4. Define a hypothetical named reviewer role, backup role, Level 2 / Level 3
   SLA, and escalation handoff path before school-facing outreach.
5. Before academic review, create a named benchmark snapshot and label current
   11-case results as fixed-sample screening evidence.
6. Add ablation baselines and a stratified sample before stronger methodology
   claims.

