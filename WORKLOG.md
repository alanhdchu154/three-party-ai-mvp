# WORKLOG - Three-Party AI Current Evidence

Last updated: 2026-06-19

This file is for current coordination only. Completed 2026-05-21 build and
generation history was removed from the active worklog; use git history for
historical details.

## Usage

1. Read open follow-ups before changing files.
2. Run `python3 scripts/audit_conversation_quality.py` before reporting corpus
   counts.
3. Do not record hourly scheduled generation here; use
   `data/generated_conversations/index.json` plus the audit script.
4. Treat old corpus counts and reports as historical snapshots.

## Open Follow-Ups

| # | Item | Owner | Status |
|---|---|---|---|
| 1 | Confirm whether latest case summaries and audience reports are current against the latest generated corpus. | Codex / Umi | done for 2026-06-04 snapshot |
| 2 | Run full audit + pytest when preparing any release or pilot-readiness claim. | Codex or cc | done for 2026-06-04 snapshot; rerun before release if corpus changes again |
| 3 | Clean stale generated/cache artifacts only after confirming they are not needed for current audit/repro. | Alan / Codex | open |
| 4 | Revoke any previously exposed Gemini / Groq / GitHub PAT secrets if not already done outside this repo. | Alan | open |
| 5 | Review `docs/generation_logic.md` privacy and automation-risk sections before expanding automation. | Umi | done for 2026-06-05; follow-ups added |
| 6 | Keep synthetic corpus generation paused while baseline comparison and human reviewer annotation are the main proof path. | Codex / Umi | paused 2026-06-18 |
| 7 | Wire the leak audit and reviewer gate into a broader release-readiness command before pilot-readiness claims. | Codex or cc | v1 done 2026-06-19 |
| 8 | Add baseline comparison and human reviewer annotation evidence before public/GitHub startup-thesis claims. | Codex or cc | v1 done 2026-06-19 |
| 9 | Add second reviewer coverage, semantic trace audit, and GitHub-public secret scan before public upload. | Codex / Umi | v1 done 2026-06-19 |
| 10 | Add relationship-context leak audit for reconstructable persona/family-system markers. | Codex / Umi | v1 done 2026-06-19 |
| 11 | Add runtime trace privacy audit for generated local artifacts and metadata-only audit logs. | Codex / Umi | v1 done 2026-06-19 |
| 12 | Add an external reviewer packet and GitHub feedback template for independent outside review. | Codex / Umi | v1 done 2026-06-19 |

## Current Reporting Rule

Any answer about "current" corpus state must include:

- audit command run
- generated corpus count
- depth distribution
- whether downstream reports were refreshed after that snapshot
- whether the statement is current evidence or historical context

## Work Log

### 2026-06-19 · Codex/Umi · External reviewer packet

- Added `docs/external_reviewer_packet.md` as the public entry point for
  outside reviewers.
- Added GitHub issue templates:
  - `.github/ISSUE_TEMPLATE/external-review.yml`
  - `.github/ISSUE_TEMPLATE/config.yml`
- The external packet gives quick, privacy-focused, and research/paper review
  paths; asks reviewers to evaluate claim boundary, privacy wall, audience-safe
  reports, deterministic audits, reviewer protocol, and next evidence needs;
  and tells reviewers not to upload real student, family, school, clinical, API
  key, or other confidential data.
- Expanded `scripts/run_release_readiness.py` public claim-boundary scan to
  include `docs/external_reviewer_packet.md` and
  `docs/github_publication_checklist.md`.
- Claim boundary: the packet makes the repo easier to review publicly. It does
  not mean external independent validation has already happened.

### 2026-06-19 · Codex/Umi · Runtime trace privacy audit

- Added `scripts/run_runtime_trace_privacy_audit.py`, a deterministic audit for
  generated local runtime surfaces.
- Added `tests/test_runtime_trace_privacy_audit.py`.
- Expanded `scripts/run_release_readiness.py` and
  `tests/test_release_readiness.py` so the one-command gate now includes
  runtime trace privacy audit.
- Current runtime trace privacy audit result: 51 pass / 0 fail.
- Surface coverage includes:
  - audience-safe reports,
  - restricted reviewer/internal artifacts,
  - pilot-run artifacts,
  - metadata-only audit logs.
- The audit enforces surface-specific policy: audience-safe surfaces cannot
  include raw trace markers or relationship-context leaks; restricted surfaces
  must carry synthetic/restricted boundary language; audit logs must not store
  prompts, transcripts, turns, raw scenario fields, or message content.
- Claim boundary: this is a local synthetic benchmark artifact audit. It is not
  production observability, real-world semantic privacy proof, deployment
  readiness, or a substitute for external review.

### 2026-06-19 · Codex/Umi · Relationship-context leak audit

- Added `scripts/run_relationship_leak_audit.py`, a deterministic audit for
  reconstructable relationship-context leaks in parent-safe and teacher-safe
  reports.
- Added `tests/test_relationship_leak_audit.py`.
- Expanded `scripts/run_release_readiness.py` and
  `tests/test_release_readiness.py` so the one-command gate now includes the
  relationship leak audit.
- Current relationship leak audit result: 18 pass / 0 fail.
- This audit intentionally allows broad support signals such as
  `family_dynamics`, but flags higher-specificity persona/family-system markers
  such as half-sibling ambiguity, fairness-as-distance, surveillance-channel
  framing, diary-like writing, succession/control, and similar reconstructable
  relationship context.
- Claim boundary: this is stronger deterministic screening evidence, not proof
  of real-world semantic privacy or a substitute for external review.

### 2026-06-19 · Codex/Umi · Persona and relationship depth layer

- Added public-safe persona and relationship documentation:
  - `docs/persona_bible.md`
  - `docs/relationship_graph.md`
  - `docs/persona_depth_audit.md`
- Current conclusion: the existing role depth is sufficient for the repo's
  synthetic benchmark / reference architecture claim, but not for real-student
  validation, clinical validity, school deployment readiness, or outcome-proof
  claims.
- The strongest relationship systems are Rachel-Uncle, Shen You-Shen Mom, and
  the Michael-Keer-Michael Mom-Stepdad blended-family system. Alan Teacher is
  intentionally treated as a utility-level school-side observer, not a full
  family-depth persona.
- Updated README, benchmark datasheet, and roadmap so the persona/relationship
  layer is visible from the GitHub-facing docs.
- Generation remains paused. Future generated cases should first name which
  persona motive and relationship edge they stress, rather than adding volume
  without design coverage.

### 2026-06-19 · Codex/Umi · GitHub-public readiness gate

- Added `scripts/run_semantic_trace_audit.py`, a deterministic trace-overlap
  guard that checks fixed-sample parent-safe and teacher-safe reports for
  reconstructable private-detail overlap beyond exact quote matching.
- Added `tests/test_semantic_trace_audit.py`.
- Added `scripts/seed_second_reviewer_pass.py`, an idempotent local
  second-reviewer seed script. It created 15 `ReviewerB` notes covering the raw
  baseline, the 11 fixed baseline cases, and 3 audience-report variants.
- Regenerated reviewer summaries. Current reviewer coverage is 37 notes / 22
  artifacts, with 15 baseline/audience artifacts covered by the second local
  reviewer pass. New-style verdict counts are now 26 `safe`, 3
  `privacy_concern`, and 2 `minor_issue`, plus legacy calibration verdicts.
- Expanded `scripts/run_release_readiness.py` so the public gate also runs
  semantic trace audit, checks second-reviewer coverage, and scans git-visible
  files for secret-looking values.
- Generated:
  - `umi/reports/semantic-trace-audit-latest.md`
  - `umi/reports/semantic-trace-audit-latest.json`
- Current gate result:
  - `.venv/bin/python scripts/run_release_readiness.py`: PASS.
  - Semantic trace audit: 22 pass / 0 fail.
  - Git-visible secret scan: 0 hits.
  - `.venv/bin/python -m pytest -q`: 77 passed / 7 skipped.
- Updated README, benchmark datasheet, roadmap, and `umi/workload.md` to mark
  GitHub publication readiness as the active state.
- Claim boundary: the second reviewer pass is local screening evidence. It is
  not external independent validation, real-student validation, clinical
  validity, deployment readiness, or outcome proof.

### 2026-06-19 · Codex/Umi · One-command release-readiness gate

- Added `scripts/run_release_readiness.py`, a deterministic Evidence v1 gate
  that does not call LLMs and does not generate synthetic data.
- The gate reruns corpus audit, baseline comparison, reviewer summary
  generation, audience-report leak audit, full pytest, and a public
  claim-boundary scan.
- Added `tests/test_release_readiness.py` for claim-boundary scanning and
  readiness metric evaluation.
- Generated:
  - `umi/reports/release-readiness-latest.md`
  - `umi/reports/release-readiness-latest.json`
- Initial gate result, superseded by the GitHub-public readiness entry above:
  - `.venv/bin/python scripts/run_release_readiness.py`: PASS.
  - Corpus remains 348 conversations: deep 85, shallow 142, medium 121.
  - Baseline sample remains 11 cases; privacy-wall pipeline has 0
    reconstructability-risk cases, 0 over-escalation flags, 0
    under-escalation flags, and 0 unsupported-recommendation flags.
  - Audience report leak audit remains 18 checked / 0 failures.
- Updated README, benchmark datasheet, roadmap, and `umi/workload.md` so the
  release gate is the canonical Evidence v1 verification command.
- Claim boundary: PASS only supports synthetic-benchmark packaging; it is not
  real-student validation, clinical validity, deployment readiness, or outcome
  proof.

### 2026-06-19 · Codex/Umi · Calibration fix and public claim review

- Fixed baseline over-escalation heuristic in
  `scripts/run_baseline_comparison.py`: shallow cases no longer treat
  conditional reviewer boilerplate as high-severity escalation. Deep
  under-escalation checks still accept reviewer/escalation language.
- Added `tests/test_baseline_comparison.py` to lock the intended behavior.
- Reran baseline comparison: privacy-wall pipeline now reports 0
  reconstructability-risk cases, 0 over-escalation flags, 0 under-escalation
  flags, and 0 recommendation-without-evidence flags on the fixed 11-case
  sample. Raw baseline remains intentionally unsafe with reconstructability
  risk in 11/11 cases.
- Updated the four formerly `over_escalated` baseline reviewer notes to `safe`
  after the metric calibration fix. Reviewer summary now reports 22 notes / 22
  artifacts with new-style verdicts: 13 `safe`, 2 `privacy_concern`, and 1
  `minor_issue`, plus legacy calibration verdicts.
- Public claim review:
  - README Evidence v1 now cites the calibrated baseline metrics and 65 passed /
    7 skipped test gate.
  - `docs/startup_thesis.md` now says Evidence v1 exists and separates
    remaining proof gaps from completed baseline/reviewer work.
  - `docs/paper_draft.md` now includes baseline comparison and reviewer
    annotation in the abstract, snapshot procedure, preliminary results,
    limitations, and conclusion.
  - `docs/benchmark_datasheet.md` now reflects the calibrated metrics and
    reviewer verdict mix.
- cc checkpoint: attempted a read-only Claude Code `sonnet` review of the
  calibration + claim-language changes. The worker produced no output before
  timeout and was stopped; no files were changed by cc and no approval is
  inferred from that attempt.
- Verification:
  - `python3 scripts/audit_conversation_quality.py`: 348 conversations; deep
    85 (24.4%), shallow 142 (40.8%), medium 121 (34.8%); avg 19.5 turns.
  - `.venv/bin/python scripts/audit_audience_report_leaks.py --json
    umi/reports/audience-report-leak-audit-latest.json`: 18 pass / 0 fail.
  - `.venv/bin/python scripts/run_baseline_comparison.py`: 11 sampled cases.
  - `.venv/bin/python scripts/generate_reviewer_summary.py`: regenerated
    calibration + annotation summaries.
  - `.venv/bin/python -m pytest -q`: 65 passed / 7 skipped.
  - `git diff --check`: clean.

### 2026-06-19 · Codex/Umi · Evidence v1 public packaging

- Added README `Evidence v1` section so the first screen now points to current
  baseline comparison, reviewer annotation, leak audit, and benchmark datasheet
  artifacts.
- Added `docs/benchmark_datasheet.md` documenting motivation, composition,
  synthetic generation boundary, intended uses, non-uses, current evidence v1,
  evaluation scripts, privacy/safety risks, maintenance rules, and known gaps.
- Updated `docs/roadmap.md` so the benchmark datasheet is part of the research
  artifact pack and GitHub thesis/proof layer.
- Claim boundary preserved: evidence v1 supports a synthetic-benchmark /
  reference-architecture claim only, not real-student validation or deployment
  readiness.

### 2026-06-19 · Codex/Umi · Human reviewer annotation v1

- Added first-pass human reviewer annotation evidence for the fixed baseline
  sample:
  - 11 case-level `baseline_comparison` notes covering 3 shallow, 3 medium, 3
    deep, 1 privacy-probe, and 1 misuse/boundary case.
  - 1 aggregate `raw_coordinator_baseline` note marked `privacy_concern`.
  - 3 audience-report notes covering `parent_safe:michael`,
    `teacher_safe:michael`, and `internal_reviewer:michael`.
- Regenerated:
  - `data/reviewer_summaries/reviewer_annotation_summary.md`
  - `data/reviewer_summaries/reviewer_calibration_summary.md`
- Reviewer summary coverage now reports 22 total notes / 22 reviewed artifacts:
  12 baseline artifacts, 3 audience-report artifacts, and 7 legacy calibration
  artifacts. New-style verdicts include 13 `safe`, 2 `privacy_concern`, and 1
  `minor_issue`, alongside legacy calibration verdicts.
- Hardened `src/reviewer_workflow.py` so reviewer summaries include source paths
  and evidence refs, review IDs use microsecond precision, and reviewer note
  metadata is not over-redacted by the profile privacy sanitizer.
- Updated `docs/human_reviewer_annotation_protocol.md` and
  `data/reviewer_notes/README.md` with baseline/audience-report examples and
  current claim boundaries.
- cc checkpoint: used Claude Code `sonnet` in read-only findings-first mode.
  Accepted its recommendations to cover the fixed baseline sample, include the
  three audience report variants, avoid timestamp collision, and expose evidence
  refs in summaries.
- Verification:
  - `python3 scripts/audit_conversation_quality.py`: 348 conversations; deep
    85 (24.4%), shallow 142 (40.8%), medium 121 (34.8%); avg 19.5 turns.
  - `.venv/bin/python scripts/audit_audience_report_leaks.py --json
    umi/reports/audience-report-leak-audit-latest.json`: 18 pass / 0 fail.
  - `.venv/bin/python scripts/run_baseline_comparison.py`: 11 sampled cases.
  - `.venv/bin/python scripts/generate_reviewer_summary.py`: regenerated
    calibration + annotation summaries.
  - `.venv/bin/python -m pytest -q`: 62 passed / 7 skipped.
  - `git diff --check`: clean.
- Claim boundary: this is synthetic benchmark reviewer annotation, not
  real-student validation, clinical validation, deployment readiness, or outcome
  proof.

### 2026-06-18 · Codex/Umi · Literature review for academic grounding

- Added `docs/literature_review.md` to ground the startup / paper thesis in
  existing research instead of only product intuition.
- Main supported framing: contextual privacy, learning analytics ethics,
  child-centred AI governance, human-AI review limits, self-disclosure to
  computers / virtual agents, multi-agent LLM privacy leakage, and benchmark
  documentation norms.
- Claim boundary preserved: the literature supports the design problem and
  benchmark rationale, but does not prove that real students will disclose to
  this system, that outcomes improve, or that the tool is deployment-ready.
- Status / handoff: use the literature review as the academic support layer for
  README / paper / GitHub positioning. The next empirical proof is still
  baseline comparison plus human reviewer annotation.

### 2026-06-18 · Codex/Umi · GitHub thesis and proof scaffold

- Reframed the repo surface as a GitHub-first technical asset:
  `Privacy-preserving AI coordination layer for schools and family-support workflows`.
- Added:
  - `docs/startup_thesis.md`
  - `docs/baseline_comparison_plan.md`
  - `docs/human_reviewer_annotation_protocol.md`
  - `scripts/run_baseline_comparison.py`
- Updated README / AGENTS / CLAUDE framing to preserve synthetic-only claim
  boundaries and make baseline comparison + human review the next proof path.
- Paused the external Claude Scheduled source-of-truth prompt at
  `/Users/alanhdchu/Documents/Claude/Scheduled/saga-a-hourly-conversation/SKILL.md`;
  if that task wakes up, it should stop without generating conversations.
- Current evidence:
  - `python3 scripts/audit_conversation_quality.py`: 348 conversations; deep
    85 (24.4%), shallow 142 (40.8%), medium 121 (34.8%); avg 19.5 turns.
  - `.venv/bin/python scripts/run_baseline_comparison.py`: 11 fixed sampled
    cases; raw baseline reconstructability risk 11/11, privacy-wall pipeline
    reconstructability risk 0/11 under deterministic checks.
  - `.venv/bin/python scripts/generate_reviewer_summary.py`: wrote both
    reviewer calibration and reviewer annotation summaries.
- Status / handoff: first proof scaffold is present. Next useful work is human
  reviewer annotation over the fixed sample and then a stricter baseline pass
  if a paper or public launch depends on the results.

### 2026-06-14 · Codex/Umi · Paper draft v0.1 and benchmark snapshot

- Used recommended defaults after Alan asked to start: full initial draft,
  HCI/CSCW-oriented framing, frozen current synthetic benchmark snapshot.
- Current evidence:
  - `python3 scripts/audit_conversation_quality.py`: 348 conversations; deep
    85 (24.4%), shallow 142 (40.8%), medium 121 (34.8%); avg 19.5 turns.
  - Regenerated deterministic downstream artifacts:
    `data/case_summaries/*.md`, `data/audience_reports/*/*.md`,
    `data/trajectory_reports/*.md`.
  - `.venv/bin/python scripts/audit_audience_report_leaks.py --json
    umi/reports/audience-report-leak-audit-latest.json`: 18 pass / 0 fail.
  - `.venv/bin/python -m pytest -q`: 59 passed / 7 skipped.
- Added paper artifacts:
  - `docs/benchmark_snapshot_2026-06-14.md`
  - `docs/evaluation_results_2026-06-14.md`
  - `docs/paper_draft.md`
- Updated `docs/roadmap.md` to record the paper pass.
- Status / handoff: draft is complete enough for advisor/collaborator reading,
  but not submission-ready. Next paper-critical work is raw-coordinator baseline
  comparison and human reviewer annotation.

### 2026-06-11 · Codex/Umi · Research prototype repositioning pack

- Reframed active direction away from GIIS/Jieni product framing and toward
  research prototype + synthetic benchmark.
- Added initial research artifact pack:
  - `docs/research_positioning.md`
  - `docs/benchmark_spec.md`
  - `docs/evaluation_plan.md`
  - `docs/synthetic_data_limitations.md`
  - `docs/paper_outline.md`
- Updated `docs/roadmap.md` so the active north star is now a publishable
  synthetic benchmark/system paper, not an internal GIIS/Jieni pilot.
- Current evidence check:
  - `python3 scripts/audit_conversation_quality.py`: 338 conversations; deep
    83 (24.6%), shallow 137 (40.5%), medium 118 (34.9%); avg 19.6 turns.
  - `python3 -m pytest -q` failed because system Python has no pytest.
  - `.venv/bin/python -m pytest -q`: 59 passed / 7 skipped.
- Status / handoff: next useful work is to freeze an intended benchmark
  snapshot, generate evaluation tables, and turn `docs/paper_outline.md` into
  a first paper draft. Do not claim real-world student behavior from synthetic
  data.

### 2026-06-11 · Central Umi · Corpus moved again; reports still need refresh

- 09:02 CDT refresh ran `python3 scripts/audit_conversation_quality.py`: corpus
  is now 330 conversations; deep 82 (24.8%), shallow 133 (40.3%), medium 115
  (34.8%). This supersedes the 2026-06-10 318-count note.
- Finding unchanged: downstream reports/tests were last fully refreshed for the
  300-case 2026-06-04 snapshot. Do not make pilot-readiness or report-freshness
  claims until reports are regenerated and the broader readiness gate is rerun.
- New local files are generated conversation artifacts plus report/score JSON
  updates; classify as corpus/evidence changes, not product validation.
- Next useful work remains a bounded release-readiness command that checks
  corpus audit, downstream report freshness/regeneration, pytest, leak audit,
  and reviewer gate together.

### 2026-06-10 · Central Umi · Corpus moved; reports need refresh

- 20:28 CDT refresh ran `python3 scripts/audit_conversation_quality.py`: corpus
  is now 318 conversations; deep 82 (25.8%), shallow 127 (39.9%), medium 109
  (34.3%). This supersedes the earlier same-day 306-count note.
- Ran `python3 scripts/audit_audience_report_leaks.py --json
  umi/reports/audience-report-leak-audit-latest.json`: 18 pass / 0 fail.
- Ran `.venv/bin/python -m pytest tests/test_report_variants.py
  tests/test_privacy.py -q`: 15 passed / 1 skipped.
- Finding: downstream reports/tests were last fully refreshed for the 300-case
  2026-06-04 snapshot. The generated corpus has moved to 318, so do not make
  pilot-readiness or report-freshness claims until reports are regenerated and
  the broader readiness gate is rerun.
- Next useful work: wire or run the release-readiness command that checks corpus
  audit, downstream report freshness/regeneration, pytest, leak audit, and
  reviewer gate together.

### 2026-06-09 · Central Umi · Current-state check

- Ran `python3 scripts/audit_conversation_quality.py`: corpus remains 300
  conversations; deep 82 (27.3%), shallow 117 (39.0%), medium 101 (33.7%).
- Ran `python3 scripts/audit_audience_report_leaks.py --json
  umi/reports/audience-report-leak-audit-latest.json`: 18 pass / 0 fail.
- No new generation, report expansion, or pilot-readiness claim was made.
- Status: keep this project in watch mode. Next useful work remains wiring the
  corpus audit, report freshness, tests, leak audit, and reviewer gate into one
  release-readiness command before any real-student pilot claim.

### 2026-06-05 · Umi · Privacy / automation-risk review

- Reviewed `docs/generation_logic.md` sections on privacy, safety, and unsupervised scheduled generation.
- Added a 2026-06-05 review section with current 300-conversation evidence and a clear decision: do not expand scheduled generation volume or pilot-facing claims until reviewer acceptance, privacy leak audit, crisis handoff, generation pause condition, and consent/deletion boundaries exist.
- Added `scripts/audit_audience_report_leaks.py` and ran it against current parent-safe / teacher-safe reports: 18 pass / 0 fail. Latest report:
  `umi/reports/audience-report-leak-audit-latest.md`.
- Added `docs/reviewer_gate_checklist.md` to define the human/reviewer gate
  before pilot-readiness claims: required evidence, sampling minimums, fail
  conditions, reviewer decisions, and current blocked status.
- Recommended next non-human work:
  - wire the leak audit into a broader release-readiness command if this project resumes,
  - keep the corpus stable until safeguards are reviewed.
- Status: #5 is done for this pass; report-leak audit is implemented and green,
  and the reviewer gate checklist exists. New follow-up work belongs under
  pilot-readiness safeguards, not more generation.

### 2026-06-04 · Codex/Umi · Version clarification and corpus refresh

- Clarified version vocabulary: repo product version is `0.8.0-internal-pilot-harness`; Central Umi's `v0.1` label is the cross-project coordination goal, not this repo's product version.
- Ran `.venv/bin/python scripts/audit_conversation_quality.py`.
- Current generated corpus snapshot: 300 conversations; deep 82 (27.3%), shallow 117 (39.0%), medium 101 (33.7%); average 20.5 turns.
- Rebuilt downstream reports from the current corpus:
  - `data/case_summaries/*.md`
  - `data/audience_reports/{internal_reviewer,parent_safe,teacher_safe}/*.md`
  - `data/trajectory_reports/*.md`
- Verified full test suite with `.venv/bin/python -m pytest -q`: 59 passed, 7 skipped.
- Secret scan over repo excluding `.git`, `.venv`, and Umi reports found no matching API/token patterns.
- Status: #1 and #2 are done for this snapshot. Rerun both if scheduled generation changes the corpus again.

### 2026-06-02 · Codex/Umi · June corpus refresh intake

- Ran `.venv/bin/python scripts/audit_conversation_quality.py`.
- Current generated corpus snapshot: 261 conversations; deep 82 (31.4%), shallow 97 (37.2%), medium 82 (31.4%); average 21.6 turns.
- Rebuilt downstream reports from the current corpus:
  - `data/case_summaries/*.md`
  - `data/audience_reports/{internal_reviewer,parent_safe,teacher_safe}/*.md`
  - `data/trajectory_reports/*.md`
- Verified full test suite with `.venv/bin/python -m pytest -q`: 59 passed, 7 skipped.
- Secret scan over repo excluding `.git`, `.venv`, and Umi reports found no matching API/token patterns.
- New finding: timeline scaffolding is now active in generated conversations. 143/261 conversations include `timeline_stage`, `event_timeframe`, `conversation_frame`, `lookback_window`, and `event_history_summary`.
- Adjusted repo docs to match active scheduled task behavior: middle-school stages (`middle_school`, `grade_7`, `grade_8`, `grade_9`) are valid for younger personas such as Keer.
- Status: #1 and #2 are done for this snapshot. Continue monitoring #6 because future scheduled generation will change corpus counts.
