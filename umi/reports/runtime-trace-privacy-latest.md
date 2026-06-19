# Runtime Trace Privacy Audit

Generated: `2026-06-19T16:13:14.265945+00:00`
Surfaces checked: `51`
Failures: `0`
Surface counts: `{'audience_safe': 20, 'restricted_reviewer': 30, 'audit_log': 1}`

## Claim Boundary

Deterministic runtime trace privacy audit over synthetic benchmark artifacts. This is not proof of real-world semantic privacy.

## Summary

| Surface type | Status | Path |
| --- | --- | --- |
| `audience_safe` | `PASS` | `data/audience_reports/parent_safe/alan_teacher.md` |
| `audience_safe` | `PASS` | `data/audience_reports/parent_safe/keer.md` |
| `audience_safe` | `PASS` | `data/audience_reports/parent_safe/michael.md` |
| `audience_safe` | `PASS` | `data/audience_reports/parent_safe/michael_mom.md` |
| `audience_safe` | `PASS` | `data/audience_reports/parent_safe/rachel.md` |
| `audience_safe` | `PASS` | `data/audience_reports/parent_safe/shen_mom.md` |
| `audience_safe` | `PASS` | `data/audience_reports/parent_safe/shen_you.md` |
| `audience_safe` | `PASS` | `data/audience_reports/parent_safe/stepdad.md` |
| `audience_safe` | `PASS` | `data/audience_reports/parent_safe/uncle.md` |
| `audience_safe` | `PASS` | `data/audience_reports/teacher_safe/alan_teacher.md` |
| `audience_safe` | `PASS` | `data/audience_reports/teacher_safe/keer.md` |
| `audience_safe` | `PASS` | `data/audience_reports/teacher_safe/michael.md` |
| `audience_safe` | `PASS` | `data/audience_reports/teacher_safe/michael_mom.md` |
| `audience_safe` | `PASS` | `data/audience_reports/teacher_safe/rachel.md` |
| `audience_safe` | `PASS` | `data/audience_reports/teacher_safe/shen_mom.md` |
| `audience_safe` | `PASS` | `data/audience_reports/teacher_safe/shen_you.md` |
| `audience_safe` | `PASS` | `data/audience_reports/teacher_safe/stepdad.md` |
| `audience_safe` | `PASS` | `data/audience_reports/teacher_safe/uncle.md` |
| `audience_safe` | `PASS` | `data/pilot_runs/v0_8_smoke_michael/parent_safe.md` |
| `audience_safe` | `PASS` | `data/pilot_runs/v0_8_smoke_michael/teacher_safe.md` |
| `restricted_reviewer` | `PASS` | `data/audience_reports/internal_reviewer/alan_teacher.md` |
| `restricted_reviewer` | `PASS` | `data/audience_reports/internal_reviewer/keer.md` |
| `restricted_reviewer` | `PASS` | `data/audience_reports/internal_reviewer/michael.md` |
| `restricted_reviewer` | `PASS` | `data/audience_reports/internal_reviewer/michael_mom.md` |
| `restricted_reviewer` | `PASS` | `data/audience_reports/internal_reviewer/rachel.md` |
| `restricted_reviewer` | `PASS` | `data/audience_reports/internal_reviewer/shen_mom.md` |
| `restricted_reviewer` | `PASS` | `data/audience_reports/internal_reviewer/shen_you.md` |
| `restricted_reviewer` | `PASS` | `data/audience_reports/internal_reviewer/stepdad.md` |
| `restricted_reviewer` | `PASS` | `data/audience_reports/internal_reviewer/uncle.md` |
| `restricted_reviewer` | `PASS` | `data/case_summaries/alan_teacher.md` |
| `restricted_reviewer` | `PASS` | `data/case_summaries/keer.md` |
| `restricted_reviewer` | `PASS` | `data/case_summaries/michael.md` |
| `restricted_reviewer` | `PASS` | `data/case_summaries/michael_mom.md` |
| `restricted_reviewer` | `PASS` | `data/case_summaries/rachel.md` |
| `restricted_reviewer` | `PASS` | `data/case_summaries/shen_mom.md` |
| `restricted_reviewer` | `PASS` | `data/case_summaries/shen_you.md` |
| `restricted_reviewer` | `PASS` | `data/case_summaries/stepdad.md` |
| `restricted_reviewer` | `PASS` | `data/case_summaries/uncle.md` |
| `restricted_reviewer` | `PASS` | `data/trajectory_reports/alan_teacher.md` |
| `restricted_reviewer` | `PASS` | `data/trajectory_reports/keer.md` |
| `restricted_reviewer` | `PASS` | `data/trajectory_reports/michael.md` |
| `restricted_reviewer` | `PASS` | `data/trajectory_reports/michael_mom.md` |
| `restricted_reviewer` | `PASS` | `data/trajectory_reports/rachel.md` |
| `restricted_reviewer` | `PASS` | `data/trajectory_reports/shen_mom.md` |
| `restricted_reviewer` | `PASS` | `data/trajectory_reports/shen_you.md` |
| `restricted_reviewer` | `PASS` | `data/trajectory_reports/stepdad.md` |
| `restricted_reviewer` | `PASS` | `data/trajectory_reports/uncle.md` |
| `restricted_reviewer` | `PASS` | `data/pilot_runs/v0_8_smoke_michael/internal_reviewer.md` |
| `restricted_reviewer` | `PASS` | `data/pilot_runs/v0_8_smoke_michael/trajectory_report.md` |
| `restricted_reviewer` | `PASS` | `data/pilot_runs/v0_8_smoke_michael/case_summary.json` |
| `audit_log` | `PASS` | `data/pilot_runs/v0_8_smoke_michael/audit_log.jsonl` |

## Failures

None.

## Notes

- Audience-safe surfaces are checked for raw trace markers and relationship-context leaks.
- Restricted reviewer/internal surfaces must carry synthetic and restricted-boundary language.
- Audit logs must remain metadata-only and must not store prompts, transcripts, turns, or raw scenario fields.
