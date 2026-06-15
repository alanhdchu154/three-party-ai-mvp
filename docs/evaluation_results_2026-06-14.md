# Evaluation Results — 2026-06-14 Preliminary Snapshot

These are preliminary benchmark results for the paper draft. They are generated
from a synthetic corpus and deterministic report audits.

## Evaluation Status

| Area | Status |
|---|---|
| Corpus audit | Complete for 348-conversation snapshot |
| Case summary regeneration | Complete |
| Audience report regeneration | Complete |
| Trajectory report regeneration | Complete |
| Audience-safe leak audit | 18 pass / 0 fail |
| Full test suite | 59 passed / 7 skipped |
| Human reviewer study | Not yet run |
| Raw-coordinator baseline comparison | Not yet run |

## Corpus Quality

The current corpus is balanced around the intended depth distribution:

| Depth | Count | Share |
|---|---:|---:|
| shallow | 142 | 40.8% |
| medium | 121 | 34.8% |
| deep | 85 | 24.4% |

This matters because earlier corpus versions were deep-heavy and risked
rewarding over-escalation. The current snapshot includes enough shallow and
medium material to evaluate whether the system over-pathologizes daily use.

## Report Generation Coverage

| Artifact | Count |
|---|---:|
| Case summaries | 9 |
| Internal reviewer reports | 9 |
| Parent-safe reports | 9 |
| Teacher-safe reports | 9 |
| Trajectory reports | 9 |

## Audience-Safe Leak Audit

Command:

```bash
.venv/bin/python scripts/audit_audience_report_leaks.py --json umi/reports/audience-report-leak-audit-latest.json
```

Result:

| Audience surface | Reports checked | Failures |
|---|---:|---:|
| parent_safe | 9 | 0 |
| teacher_safe | 9 | 0 |
| total | 18 | 0 |

The deterministic audit checks for raw conversation paths, scenario seed
markers, raw turn labels, private JSON references, long quoted passages, and
exact private chunks from the generated conversation corpus.

## Dimension Score Snapshot

Current dimension-score files exist for 9 personas.

| Persona | Cumulative strain | Highest concern |
|---|---:|---|
| alan_teacher | 8 | future_planning |
| keer | 6 | family_dynamics |
| michael | 9 | family_dynamics |
| michael_mom | 8 | family_dynamics |
| rachel | 11 | family_dynamics |
| shen_mom | 10 | family_dynamics |
| shen_you | 13 | academic_load |
| stepdad | 6 | family_dynamics |
| uncle | 8 | family_dynamics |

These dimension scores are synthetic-evidence artifacts. They should be used to
test pipeline behavior and reviewer workflow, not to infer anything about real
people.

## What We Can Report in the Paper

Supported preliminary claims:

- The benchmark contains a balanced shallow/medium/deep synthetic corpus.
- The current privacy-wall reporting pipeline generated parent-safe and
  teacher-safe reports with 0 deterministic leak-audit failures.
- The report pipeline produces human-reviewable artifacts for 9 personas.
- The project has automated checks for privacy regressions and schema-level
  safety behavior.

Not yet supported:

- Comparative leakage reduction versus a raw coordinator baseline.
- Human reviewer agreement.
- Real-world student, parent, or teacher behavior.
- Educational or clinical effectiveness.

## Next Evaluation Needed for Submission

Before submission, add:

1. Raw-coordinator baseline run on a frozen subset.
2. Privacy-wall coordinator run on the same subset.
3. Table comparing raw quote/entity/event/reconstructability leakage.
4. Human reviewer annotation on a sampled set of reports.
5. Reviewer agreement or at least percent agreement with confidence caveat.
