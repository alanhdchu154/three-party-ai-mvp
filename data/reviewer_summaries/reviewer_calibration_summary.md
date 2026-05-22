# Reviewer Calibration Summary

> Human reviewer notes calibrate synthetic case and trajectory outputs. They do not convert synthetic data into real pilot validation.

- Notes: `7`
- Artifacts reviewed: `7`

## case_summary:michael
- Reviews: `1`
- Status: `reviewed_supported`
- Verdicts: `{'agree': 1}`
- Confidence: `{'high': 1}`
- Reviewers: `Umi`

### Privacy Concerns
- None.

### Action Items
- Do not convert synthetic evidence into pilot validation.
- Keep recommended actions reversible and low-pressure.

## case_summary:rachel
- Reviews: `1`
- Status: `reviewed_supported`
- Verdicts: `{'agree': 1}`
- Confidence: `{'medium': 1}`
- Reviewers: `Umi`

### Privacy Concerns
- Some recommended actions may reveal too much if shown outside an authorized internal review surface.

### Action Items
- Add an audience field for case summaries: internal_reviewer vs parent_safe vs teacher_safe.
- Keep creative/future-planning details abstract in any parent-facing surface.

## case_summary:shen_you
- Reviews: `1`
- Status: `privacy_review_needed`
- Verdicts: `{'privacy_concern': 1}`
- Confidence: `{'high': 1}`
- Reviewers: `Umi`

### Privacy Concerns
- Action recommendations include specific life/context details that should not be parent- or teacher-facing without another sanitization layer.
- Level 3 dimension conflict should route to human review before recommendations are trusted.

### Action Items
- Add parent_safe and teacher_safe report variants.
- Downgrade or block specific action recommendations when Level 3 conflict is unresolved.
- Generate saved triage output for this case before using the report operationally.

## trajectory_report:michael:burnout_risk
- Reviews: `1`
- Status: `reviewed_supported`
- Verdicts: `{'true_positive': 1}`
- Confidence: `{'medium': 1}`
- Reviewers: `Umi`

### Privacy Concerns
- None.

### Action Items
- Add a reviewer-approved badge rather than treating rule confidence as final confidence.
- Lower displayed confidence for synthetic-only trajectory reports unless human-reviewed.

## trajectory_report:michael:dependency_risk
- Reviews: `1`
- Status: `needs_calibration`
- Verdicts: `{'under_evidenced': 1}`
- Confidence: `{'medium': 1}`
- Reviewers: `Umi`

### Privacy Concerns
- None.

### Action Items
- Require explicit AI over-reliance evidence before dependency_risk is shown above low confidence.
- Separate autonomy_loss from dependency_risk in trajectory rules.

## trajectory_report:rachel:disclosure_collapse
- Reviews: `1`
- Status: `needs_calibration`
- Verdicts: `{'under_evidenced': 1}`
- Confidence: `{'medium': 1}`
- Reviewers: `Umi`

### Privacy Concerns
- None.

### Action Items
- Require explicit disclosure_drop or repeated reduced openness before labeling disclosure_collapse high confidence.
- Track disclosure volume and topic breadth over time before escalating this trajectory.

## trajectory_report:shen_you:hidden_disengagement
- Reviews: `1`
- Status: `reviewed_supported`
- Verdicts: `{'true_positive': 1}`
- Confidence: `{'medium': 1}`
- Reviewers: `Umi`

### Privacy Concerns
- None.

### Action Items
- Keep this trajectory visible but mark it human-reviewed medium confidence.
- Pair it with agency-building interventions, not punitive monitoring.
