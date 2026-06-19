# Reviewer Notes

Put human calibration notes here as JSON files.

Use this layer to mark whether case summaries, trajectory reports, baseline
comparisons, coordination snapshots, and audience reports are:

- `agree`
- `disagree`
- `safe`
- `minor_issue`
- `needs_more_evidence`
- `privacy_concern`
- `over_escalated`
- `under_escalated`
- `true_positive`
- `false_positive`
- `under_evidenced`
- `not_actionable`

Do not paste raw student secrets or raw conversation turns into reviewer notes.

Example artifact IDs:

- `case_summary:michael`
- `trajectory_report:michael:burnout_risk`
- `trajectory_report:michael:trust_erosion`
- `baseline_comparison:sim_saga_a_michael__mom_crying`
- `audience_report:parent_safe:michael`
- `audience_report:teacher_safe:michael`
- `audience_report:internal_reviewer:michael`

Generate the aggregate reviewer summary with:

```bash
.venv/bin/python scripts/generate_reviewer_summary.py
```

The generated summaries are synthetic-benchmark review evidence only. They do
not establish real-student validation, clinical validity, deployment readiness,
or outcome improvement.
