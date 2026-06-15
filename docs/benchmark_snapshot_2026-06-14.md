# Benchmark Snapshot — 2026-06-14

This snapshot freezes the current evidence used by `docs/paper_draft.md`.

## Snapshot Command

```bash
python3 scripts/audit_conversation_quality.py
```

## Corpus

- Conversations: 348
- Personas: 9
- Turns: min 6 / avg 19.5 / max 53
- Missing `depth`: 0
- Missing `scenario_type`: 0
- Duplicate conversation IDs: 0

## Depth Distribution

| Depth | Count | Share |
|---|---:|---:|
| shallow | 142 | 40.8% |
| medium | 121 | 34.8% |
| deep | 85 | 24.4% |

This is close to the target benchmark balance of 40% shallow / 35% medium /
25% deep.

## Scenario Type Distribution

| Scenario type | Count |
|---|---:|
| stress_test | 76 |
| mixed | 58 |
| moderate_issue | 52 |
| mundane_help | 51 |
| off_topic | 21 |
| parent_logistics | 18 |
| logistics | 17 |
| quick_vent | 16 |
| privacy_probe | 11 |
| testing_ai | 10 |
| misuse_attempt | 9 |
| privacy_test | 5 |
| deep_arc | 3 |
| simulated | 1 |

## Per-Persona Depth Matrix

| Persona | Deep | Medium | Shallow |
|---|---:|---:|---:|
| saga_a_alan_teacher | 9 | 13 | 16 |
| saga_a_keer | 9 | 13 | 16 |
| saga_a_michael | 9 | 12 | 16 |
| saga_a_michael_mom | 9 | 14 | 16 |
| saga_a_rachel | 10 | 14 | 15 |
| saga_a_shen_mom | 9 | 14 | 16 |
| saga_a_shen_you | 10 | 14 | 15 |
| saga_a_stepdad | 10 | 15 | 15 |
| saga_a_uncle | 10 | 12 | 17 |

## Derived Artifacts Regenerated

Commands run:

```bash
.venv/bin/python scripts/generate_case_summaries.py
.venv/bin/python scripts/generate_audience_reports.py
.venv/bin/python scripts/generate_trajectory_reports.py
```

Outputs:

- Case summaries: 9
- Audience reports: 27
  - internal reviewer: 9
  - parent-safe: 9
  - teacher-safe: 9
- Trajectory reports: 9

## Safety / Regression Checks

Commands run:

```bash
.venv/bin/python scripts/audit_audience_report_leaks.py --json umi/reports/audience-report-leak-audit-latest.json
.venv/bin/python -m pytest -q
```

Results:

- Audience report leak audit: 18 pass / 0 fail
- Test suite: 59 passed / 7 skipped

## Current Claim Boundary

This snapshot supports preliminary benchmark/system claims only. It does not
support claims about real student behavior, clinical validity, educational
outcomes, or deployment readiness.
