# Release Readiness Report

Status: `PASS`
Generated at: `2026-06-19T20:16:28.303631+00:00`

> Evidence v1 is a synthetic-benchmark gate. Passing this report does not prove real-student validation, clinical validity, deployment readiness, or outcome improvement.

## Commands

| Check | Return code | Command |
|---|---:|---|
| `corpus_audit` | `0` | `python3 scripts/audit_conversation_quality.py --json` |
| `baseline_comparison` | `0` | `/Users/alanhdchu/three-party-ai-mvp/.venv/bin/python scripts/run_baseline_comparison.py` |
| `reviewer_summary` | `0` | `/Users/alanhdchu/three-party-ai-mvp/.venv/bin/python scripts/generate_reviewer_summary.py` |
| `audience_report_leak_audit` | `0` | `/Users/alanhdchu/three-party-ai-mvp/.venv/bin/python scripts/audit_audience_report_leaks.py --json umi/reports/audience-report-leak-audit-latest.json` |
| `semantic_trace_audit` | `0` | `/Users/alanhdchu/three-party-ai-mvp/.venv/bin/python scripts/run_semantic_trace_audit.py` |
| `relationship_leak_audit` | `0` | `/Users/alanhdchu/three-party-ai-mvp/.venv/bin/python scripts/run_relationship_leak_audit.py` |
| `runtime_trace_privacy_audit` | `0` | `/Users/alanhdchu/three-party-ai-mvp/.venv/bin/python scripts/run_runtime_trace_privacy_audit.py` |
| `pytest` | `0` | `/Users/alanhdchu/three-party-ai-mvp/.venv/bin/python -m pytest -q` |

## Evidence Summary

- Corpus: `348` conversations; depth counts `{'deep': 85, 'shallow': 142, 'medium': 121}`.
- Baseline sample size: `11`.
- Raw coordinator reconstructability-risk cases: `11`.
- Privacy-wall reconstructability-risk cases: `0`.
- Privacy-wall over/under escalation flags: `0` / `0`.
- Privacy-wall unsupported recommendation flags: `0`.
- Audience report leak audit: `18` checked / `0` failures.
- Semantic trace audit: `22` checked / `0` failures.
- Relationship leak audit: `18` checked / `0` failures.
- Runtime trace privacy audit: `51` checked / `0` failures.
- Reviewer coverage: `37` notes / `22` artifacts.
- Reviewer artifact mix: `12` baseline / `3` audience-report artifacts.
- Second reviewer coverage: `15` baseline/audience artifacts.
- Reviewer verdict counts: `{'agree': 2, 'privacy_concern': 3, 'true_positive': 2, 'under_evidenced': 2, 'minor_issue': 2, 'safe': 26}`.

## Gate Failures

- None.

## Claim Boundary Scan

- No positive public overclaim hits found.

## Secret Scan

- No secret-like values found in git-visible files.

## Boundary

This gate supports public synthetic-benchmark packaging only. It does not authorize real minor-data use, school deployment, clinical claims, or autonomous support workflows.
