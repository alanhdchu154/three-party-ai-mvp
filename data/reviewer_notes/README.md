# Reviewer Notes

Put human calibration notes here as JSON files.

Use this layer to mark whether case summaries and trajectory reports are:

- `agree`
- `disagree`
- `needs_more_evidence`
- `privacy_concern`
- `true_positive`
- `false_positive`
- `under_evidenced`

Do not paste raw student secrets or raw conversation turns into reviewer notes.

Example artifact IDs:

- `case_summary:michael`
- `trajectory_report:michael:burnout_risk`
- `trajectory_report:michael:trust_erosion`

Generate the aggregate reviewer summary with:

```bash
python scripts/generate_reviewer_summary.py
```

