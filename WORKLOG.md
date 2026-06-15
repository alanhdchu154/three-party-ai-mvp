# WORKLOG - Three-Party AI Current Evidence

Last updated: 2026-06-14

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
| 6 | Continue monitoring corpus balance; scheduled generation should keep moving away from deep-heavy distribution. | Automation + periodic human review | watch |
| 7 | Wire the leak audit and reviewer gate into a broader release-readiness command before pilot-readiness claims. | Codex or cc | open |

## Current Reporting Rule

Any answer about "current" corpus state must include:

- audit command run
- generated corpus count
- depth distribution
- whether downstream reports were refreshed after that snapshot
- whether the statement is current evidence or historical context

## Work Log

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
