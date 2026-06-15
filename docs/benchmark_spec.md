# Benchmark Specification

Last updated: 2026-06-11

## Benchmark Name

Working title:

**MPSC-Bench: Multi-Party Student Support Coordination Benchmark**

The name is temporary. The paper can use a clearer title later.

## Purpose

The benchmark tests whether an AI coordination pipeline can synthesize
student/parent/teacher perspectives into safe, actionable support guidance
without leaking raw disclosures, private constraints, or reconstructable events.

It is a synthetic stress-test environment, not a behavioral sample of real
students.

## Core Entities

Each case may include:

- `student`: private student-AI conversations.
- `parent`: private parent-AI conversations or parent-facing inputs.
- `teacher`: private teacher-AI conversations or teacher-facing observations.
- `coordinator`: consumes abstracted profiles, not raw conversations.
- `reviewer`: human reviewer who evaluates privacy, escalation, and actionability.

## Conversation Depth

Each generated conversation should have a `depth` field:

| Depth | Intended meaning | Typical use |
|---|---|---|
| `shallow` | Daily-life or task-oriented interaction | homework help, logistics, off-topic chat, testing AI boundaries |
| `medium` | Moderate concern or partial disclosure | academic stress, friend conflict, family friction, small crack in coping |
| `deep` | High-salience disclosure or multi-turn emotional arc | privacy probes, identity/family strain, high-risk support patterns |

The benchmark should include enough shallow/medium cases to measure false
positive escalation and over-pathologizing.

## Scenario Types

Current or target scenario types:

- `mundane_help`
- `quick_vent`
- `logistics`
- `parent_logistics`
- `off_topic`
- `testing_ai`
- `misuse_attempt`
- `moderate_issue`
- `mixed`
- `stress_test`
- `privacy_test`
- `deep_arc`
- `crisis` or Level 3 safety scenario, only with strict human-review framing

## Required Per-Conversation Fields

Each generated conversation file should include:

- `id`
- `persona_id`
- `scenario_seed_id`
- `scenario_type`
- `depth`
- `source_type`
- `model`
- `generated_at`
- `occurred_at`
- `turns`
- optional timeline fields such as `timeline_stage`, `event_timeframe`,
  `conversation_frame`, `lookback_window`, and `event_history_summary`

## Derived Artifacts

The benchmark may produce:

- `dimension_scores`: structured risk/support dimensions.
- `analysis_reports`: coordinator-style analysis artifacts.
- `case_summaries`: normalized student case summaries.
- `audience_reports`: internal, parent-safe, and teacher-safe reports.
- `trajectory_reports`: possible longitudinal risk patterns.
- reviewer notes and calibration summaries.

Derived artifacts must record source type and should not be treated as direct
ground truth.

## Labels and Targets

Useful labels include:

- `depth`
- `scenario_type`
- `expected_risk_flags`
- `source_type`
- dimension levels, especially emotional safety and cumulative strain
- whether a case should trigger monitor, human review, urgent review, or no
  escalation
- whether an output leaks raw quote, entity, event, number, paraphrase, or
  reconstructable private detail

## Current Corpus Health Rule

Before reporting corpus state, run:

```bash
python3 scripts/audit_conversation_quality.py
```

Report:

- conversation count
- depth distribution
- scenario type distribution
- average turns
- whether downstream reports were refreshed after that corpus snapshot

## Benchmark Splits

For a paper, freeze a versioned snapshot:

- `benchmark_v0`: current synthetic corpus after quality audit.
- `dev_split`: prompt/system development.
- `eval_split`: held out for final metrics.
- `adversarial_split`: privacy probes, misuse attempts, and high-risk
  reconstructability cases.

Do not evaluate final claims on the same cases used to design prompts and
heuristics without labeling the result as in-sample.

## Quality Criteria

A benchmark snapshot is usable when:

- no conversation is missing `depth` or `scenario_type`
- no duplicate conversation IDs exist
- shallow/medium cases are present for each major persona group
- privacy probe and misuse attempt cases exist
- downstream reports can be regenerated from the snapshot
- leakage audit passes for audience-safe reports
- full tests pass

## Known Limitations

- Dialogue is LLM-generated.
- Persona behavior is authored/simulated, not measured.
- Labels may reflect generator assumptions.
- Synthetic depth distribution does not imply real-world prevalence.
- The benchmark can evaluate system behavior under controlled conditions, but
  cannot validate real educational outcomes.
