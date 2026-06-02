# Trajectory Report — rachel

> These are possible risk patterns from synthetic/local artifacts, not diagnoses or certain predictions.

## Burnout Risk (`burnout_risk`)
- Confidence: `high`
- Calibrated confidence: `medium`
- Reviewer status: `not_reviewed`

### Current trajectory
- Possible `emotional_flattening` pattern: Student remains functional but shows reduced spark, affect, or responsiveness.
- Possible `future_planning_collapse` pattern: Student cannot describe a future path, goal, or reason for continuing current effort.
- Possible `perfectionism_pressure` pattern: Student links worth, belonging, or safety to performance and achievement.
- Dimension `identity` is active in current score.
- Dimension `future_planning` is active in current score.
- Dimension `academic_load` is active in current score.

### Why the system thinks so
- `traj_ev_001` dimension_score · medium · synthetic-only · Possible signal `emotional_flattening` detected. · `data/dimension_scores/rachel.json`
- `traj_ev_002` dimension_score · medium · synthetic-only · Possible signal `future_planning_collapse` detected. · `data/dimension_scores/rachel.json`
- `traj_ev_003` dimension_score · medium · synthetic-only · Possible signal `perfectionism_pressure` detected. · `data/dimension_scores/rachel.json`
- `traj_ev_004` dimension_score · high · synthetic-only · Dimension `identity` is Level 2. · `data/dimension_scores/rachel.json`
- `traj_ev_005` dimension_score · high · synthetic-only · Dimension `future_planning` is Level 2. · `data/dimension_scores/rachel.json`
- `traj_ev_006` dimension_score · high · synthetic-only · Dimension `academic_load` is Level 1. · `data/dimension_scores/rachel.json`

### Likely outcomes if unchanged
- Continued outward functioning with lower engagement.
- Possible hidden disengagement if adults respond only with performance pressure.

### Actions that may stabilize
- Reduce performance interrogation; focus on low-pressure reflection.
- Offer one small student-owned choice instead of a broad life-plan question.

### Actions that may destabilize
- Treating the possible trajectory as certainty.
- Sharing protected details across parties to force alignment.
- Increasing performance pressure without restoring agency.

### What evidence is missing
- No real pilot evidence; synthetic-only trajectory should not be treated as validation.

### Reviewer calibration
- Not reviewed yet.

## Trust Erosion (`trust_erosion`)
- Confidence: `high`
- Calibrated confidence: `medium`
- Reviewer status: `not_reviewed`

### Current trajectory
- Possible `parent_monitoring_increase` pattern: Parent or guardian increases checking, pressure, surveillance, or corrective questioning.
- Possible `social_withdrawal` pattern: Student reduces peer/family contact, avoids eye contact, or retreats from normal interaction.
- Dimension `social_development` is active in current score.
- Dimension `family_dynamics` is active in current score.

### Why the system thinks so
- `traj_ev_001` coordinator_report · medium · synthetic-only · Possible signal `parent_monitoring_increase` detected. · `data/analysis_reports/rachel_analysis.json`
- `traj_ev_002` dimension_score · medium · synthetic-only · Possible signal `social_withdrawal` detected. · `data/dimension_scores/rachel.json`
- `traj_ev_003` dimension_score · high · synthetic-only · Dimension `social_development` is Level 2. · `data/dimension_scores/rachel.json`
- `traj_ev_004` dimension_score · high · synthetic-only · Dimension `family_dynamics` is Level 2. · `data/dimension_scores/rachel.json`

### Likely outcomes if unchanged
- Student may share less with adults and rely more on indirect communication.
- Parent/teacher attempts to help may be experienced as surveillance.

### Actions that may stabilize
- Protect privacy boundaries explicitly.
- Coach adults to create space without demanding disclosure.

### Actions that may destabilize
- Treating the possible trajectory as certainty.
- Sharing protected details across parties to force alignment.
- Parent or teacher questioning that feels like surveillance.

### What evidence is missing
- No real pilot evidence; synthetic-only trajectory should not be treated as validation.

### Reviewer calibration
- Not reviewed yet.

## Disclosure Collapse (`disclosure_collapse`)
- Confidence: `high`
- Calibrated confidence: `low`
- Reviewer status: `needs_calibration`

### Current trajectory
- Possible `disclosure_drop` pattern: Student shares less over time, becomes shorter, or avoids previously open topics.
- Possible `emotional_flattening` pattern: Student remains functional but shows reduced spark, affect, or responsiveness.
- Possible `social_withdrawal` pattern: Student reduces peer/family contact, avoids eye contact, or retreats from normal interaction.
- Dimension `emotional_safety` is active in current score.
- Dimension `social_development` is active in current score.
- Dimension `family_dynamics` is active in current score.

### Why the system thinks so
- `traj_ev_001` coordinator_report · medium · synthetic-only · Possible signal `disclosure_drop` detected. · `data/analysis_reports/rachel_analysis.json`
- `traj_ev_002` dimension_score · medium · synthetic-only · Possible signal `emotional_flattening` detected. · `data/dimension_scores/rachel.json`
- `traj_ev_003` dimension_score · medium · synthetic-only · Possible signal `social_withdrawal` detected. · `data/dimension_scores/rachel.json`
- `traj_ev_004` dimension_score · high · synthetic-only · Dimension `emotional_safety` is Level 1. · `data/dimension_scores/rachel.json`
- `traj_ev_005` dimension_score · high · synthetic-only · Dimension `social_development` is Level 2. · `data/dimension_scores/rachel.json`
- `traj_ev_006` dimension_score · high · synthetic-only · Dimension `family_dynamics` is Level 2. · `data/dimension_scores/rachel.json`

### Likely outcomes if unchanged
- AI may stop receiving the student's most useful truths.
- System confidence should decrease until new evidence appears.

### Actions that may stabilize
- Avoid sudden cross-party exposure of private themes.
- Use shorter, choice-based check-ins rather than broad probing.

### Actions that may destabilize
- Treating the possible trajectory as certainty.
- Sharing protected details across parties to force alignment.
- Pushing for more disclosure after trust has weakened.

### What evidence is missing
- No real pilot evidence; synthetic-only trajectory should not be treated as validation.

### Reviewer calibration
- Status: `needs_calibration`
- Verdicts: `{'under_evidenced': 1}`
- Reviewers: `Umi`
- Action items:
  - Require explicit disclosure_drop or repeated reduced openness before labeling disclosure_collapse high confidence.
  - Track disclosure volume and topic breadth over time before escalating this trajectory.

## Hidden Disengagement (`hidden_disengagement`)
- Confidence: `high`
- Calibrated confidence: `medium`
- Reviewer status: `not_reviewed`

### Current trajectory
- Possible `emotional_flattening` pattern: Student remains functional but shows reduced spark, affect, or responsiveness.
- Possible `future_planning_collapse` pattern: Student cannot describe a future path, goal, or reason for continuing current effort.
- Possible `strategic_compliance` pattern: Student appears compliant while privately disengaging or withholding real preference.
- Dimension `identity` is active in current score.
- Dimension `future_planning` is active in current score.
- Dimension `academic_load` is active in current score.

### Why the system thinks so
- `traj_ev_001` dimension_score · medium · synthetic-only · Possible signal `emotional_flattening` detected. · `data/dimension_scores/rachel.json`
- `traj_ev_002` dimension_score · medium · synthetic-only · Possible signal `future_planning_collapse` detected. · `data/dimension_scores/rachel.json`
- `traj_ev_003` coordinator_report · medium · synthetic-only · Possible signal `strategic_compliance` detected. · `data/analysis_reports/rachel_analysis.json`
- `traj_ev_004` dimension_score · high · synthetic-only · Dimension `identity` is Level 2. · `data/dimension_scores/rachel.json`
- `traj_ev_005` dimension_score · high · synthetic-only · Dimension `future_planning` is Level 2. · `data/dimension_scores/rachel.json`
- `traj_ev_006` dimension_score · high · synthetic-only · Dimension `academic_load` is Level 1. · `data/dimension_scores/rachel.json`

### Likely outcomes if unchanged
- Student may keep meeting visible expectations while internally opting out.
- Adults may miss the issue because grades or behavior remain stable.

### Actions that may stabilize
- Look for agency signals, not only performance metrics.
- Offer low-stakes action experiments that belong to the student.

### Actions that may destabilize
- Treating the possible trajectory as certainty.
- Sharing protected details across parties to force alignment.
- Mistaking visible compliance for true buy-in.

### What evidence is missing
- No real pilot evidence; synthetic-only trajectory should not be treated as validation.

### Reviewer calibration
- Not reviewed yet.

## Parent Escalation (`parent_escalation`)
- Confidence: `high`
- Calibrated confidence: `medium`
- Reviewer status: `not_reviewed`

### Current trajectory
- Possible `disclosure_drop` pattern: Student shares less over time, becomes shorter, or avoids previously open topics.
- Possible `parent_monitoring_increase` pattern: Parent or guardian increases checking, pressure, surveillance, or corrective questioning.
- Possible `strategic_compliance` pattern: Student appears compliant while privately disengaging or withholding real preference.
- Dimension `family_dynamics` is active in current score.
- Dimension `academic_load` is active in current score.

### Why the system thinks so
- `traj_ev_001` coordinator_report · medium · synthetic-only · Possible signal `disclosure_drop` detected. · `data/analysis_reports/rachel_analysis.json`
- `traj_ev_002` coordinator_report · medium · synthetic-only · Possible signal `parent_monitoring_increase` detected. · `data/analysis_reports/rachel_analysis.json`
- `traj_ev_003` coordinator_report · medium · synthetic-only · Possible signal `strategic_compliance` detected. · `data/analysis_reports/rachel_analysis.json`
- `traj_ev_004` dimension_score · high · synthetic-only · Dimension `family_dynamics` is Level 2. · `data/dimension_scores/rachel.json`
- `traj_ev_005` dimension_score · high · synthetic-only · Dimension `academic_load` is Level 1. · `data/dimension_scores/rachel.json`

### Likely outcomes if unchanged
- Parent concern may convert into more monitoring, reducing student trust.
- The coordination loop may become parent-driven rather than student-centered.

### Actions that may stabilize
- Give parent concrete low-pressure behaviors instead of more questions.
- Do not share protected student details to calm parent anxiety.

### Actions that may destabilize
- Treating the possible trajectory as certainty.
- Sharing protected details across parties to force alignment.
- Using private student themes to calm parent anxiety.

### What evidence is missing
- No real pilot evidence; synthetic-only trajectory should not be treated as validation.

### Reviewer calibration
- Not reviewed yet.

## Dependency Risk (`dependency_risk`)
- Confidence: `high`
- Calibrated confidence: `medium`
- Reviewer status: `not_reviewed`

### Current trajectory
- Possible `disclosure_drop` pattern: Student shares less over time, becomes shorter, or avoids previously open topics.
- Possible `future_planning_collapse` pattern: Student cannot describe a future path, goal, or reason for continuing current effort.
- Dimension `future_planning` is active in current score.
- Dimension `emotional_safety` is active in current score.
- Dimension `identity` is active in current score.

### Why the system thinks so
- `traj_ev_001` coordinator_report · medium · synthetic-only · Possible signal `disclosure_drop` detected. · `data/analysis_reports/rachel_analysis.json`
- `traj_ev_002` dimension_score · medium · synthetic-only · Possible signal `future_planning_collapse` detected. · `data/dimension_scores/rachel.json`
- `traj_ev_003` dimension_score · high · synthetic-only · Dimension `future_planning` is Level 2. · `data/dimension_scores/rachel.json`
- `traj_ev_004` dimension_score · high · synthetic-only · Dimension `emotional_safety` is Level 1. · `data/dimension_scores/rachel.json`
- `traj_ev_005` dimension_score · high · synthetic-only · Dimension `identity` is Level 2. · `data/dimension_scores/rachel.json`

### Likely outcomes if unchanged
- Student may over-rely on AI or adult interpretation instead of building agency.
- The system may become a substitute for student-owned decisions.

### Actions that may stabilize
- Return decisions to the student in small reversible steps.
- Use AI as scaffolding, not as the final authority.

### Actions that may destabilize
- Treating the possible trajectory as certainty.
- Sharing protected details across parties to force alignment.
- Letting AI make decisions the student should practice making.

### What evidence is missing
- No real pilot evidence; synthetic-only trajectory should not be treated as validation.

### Reviewer calibration
- Not reviewed yet.
