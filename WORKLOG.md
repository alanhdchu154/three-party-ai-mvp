# WORKLOG - Three-Party AI Current Handoffs

Last updated: 2026-06-02

This file is for current coordination only. Completed 2026-05-21 build and
generation history was removed from the active worklog; use git history for
historical details.

## Usage

1. Read open handoffs before changing files.
2. Run `python3 scripts/audit_conversation_quality.py` before reporting corpus
   counts.
3. Do not record hourly scheduled generation here; use
   `data/generated_conversations/index.json` plus the audit script.
4. Treat old corpus counts and reports as historical snapshots.

## Open Handoffs

| # | Item | Owner | Status |
|---|---|---|---|
| 1 | Confirm whether latest case summaries and audience reports are current against the latest generated corpus. | Codex / Umi | done for 2026-06-02 snapshot |
| 2 | Run full audit + pytest when preparing any release or pilot-readiness claim. | Codex or cc | done for 2026-06-02 snapshot; rerun before release |
| 3 | Clean stale generated/cache artifacts only after confirming they are not needed for current audit/repro. | Alan / Codex | open |
| 4 | Revoke any previously exposed Gemini / Groq / GitHub PAT secrets if not already done outside this repo. | Alan | open |
| 5 | Review `docs/generation_logic.md` privacy and automation-risk sections before expanding automation. | Umi | open |
| 6 | Continue monitoring corpus balance; scheduled generation should keep moving away from deep-heavy distribution. | Automation + periodic human review | watch |

## Current Reporting Rule

Any answer about "current" corpus state must include:

- audit command run
- generated corpus count
- depth distribution
- whether downstream reports were refreshed after that snapshot
- whether the statement is current evidence or historical context

## Work Log

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
