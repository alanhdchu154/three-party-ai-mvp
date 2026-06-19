# Baseline Comparison Plan

## Goal

Compare a raw-coordinator baseline against the privacy-wall pipeline without
generating new synthetic data or requiring live LLM calls.

The first version is a deterministic proof scaffold. It is designed to be
reproducible in GitHub and to identify where the privacy-wall architecture
should reduce leakage. It is not a final human-subjects or real-world outcome
evaluation.

## Systems Compared

1. **Raw coordinator baseline**
   - Uses raw synthetic conversation turns and scenario metadata as the
     coordination packet.
   - This approximates the risky architecture where the coordinator or report
     writer can see raw disclosures.
   - Expected risk: high raw quote, entity/event, and reconstructability
     leakage.

2. **Privacy-wall pipeline**
   - Uses existing generated parent-safe and teacher-safe reports.
   - These reports are downstream of abstraction, report variants, and leak
     audit constraints.
   - Expected risk: lower raw quote and reconstructability leakage, but still
     requires human review for usefulness and boundary judgment.

## Fixed Sample

`scripts/run_baseline_comparison.py` selects a stable sample from
`data/generated_conversations/`:

- 3 shallow conversations,
- 3 medium conversations,
- 3 deep conversations,
- 1 privacy-probe or privacy-test conversation,
- 1 misuse or boundary-testing conversation.

Selection is deterministic: files are sorted by ID, and the first matching
items are used. The script reports the selected case IDs so a reviewer can
inspect the exact sample.

## Metrics

The script reports:

- raw quote leaks,
- entity/event/detail leaks,
- reconstructability risk,
- over-escalation heuristic,
- under-escalation heuristic,
- recommendation-without-evidence heuristic,
- audience-safe report leak status.

These are deterministic heuristics. They are useful regression signals and
screening evidence, not substitutes for human annotation.

## Output

Running:

```bash
.venv/bin/python scripts/run_baseline_comparison.py
```

writes:

- `umi/reports/baseline-comparison-latest.json`
- `umi/reports/baseline-comparison-latest.md`

## Claim Boundary

This comparison can support a GitHub-facing claim that the repo contains a
reproducible privacy-boundary evaluation scaffold. It cannot claim real student
behavior, clinical safety, school deployment readiness, or outcome improvement.
