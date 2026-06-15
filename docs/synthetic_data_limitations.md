# Synthetic Data Limitations

Last updated: 2026-06-11

## Summary

The corpus in this project is synthetic. Conversations, personas, conflicts,
signals, and many derived artifacts are generated or authored rather than
observed from real students, parents, or teachers.

This is acceptable for a benchmark paper only if the claim is framed correctly.

## Correct Use

Synthetic data can be used to:

- stress-test privacy wall behavior;
- create adversarial leakage and reconstructability cases;
- test whether shallow conversations are over-escalated;
- test whether deep/high-risk synthetic cases are under-escalated;
- compare pipeline variants under controlled conditions;
- prototype reviewer workflows without exposing real minors' data.

## Incorrect Use

Synthetic data cannot be used to claim:

- real students will disclose to AI in the same way;
- real parents/teachers will behave like the generated personas;
- the system improves wellbeing, learning, retention, or family trust;
- the system is clinically safe;
- the system is deployment-ready for minors;
- the observed depth distribution reflects real-world prevalence.

## Major Bias Risks

### Generator Bias

LLMs may produce conversations that reflect training-data stereotypes, the
prompt author's assumptions, or over-coherent narrative arcs.

### Over-Pathologizing

If too many conversations are deep or crisis-adjacent, the system may learn that
ordinary support requests are risk signals.

### Under-Representing Boring Reality

Real student support includes many mundane interactions. The benchmark must
include shallow and medium cases so the evaluator is not rewarded for treating
everything as crisis.

### Circular Evaluation

If the same LLM family generates conversations, abstractions, and judgments,
the evaluation may reflect model agreement rather than independent validity.

### Cultural and Class Assumptions

Synthetic personas may encode narrow assumptions about family pressure,
achievement, international schools, tutoring, or status anxiety.

## Mitigations

- Maintain depth/type audit.
- Freeze benchmark snapshots before evaluation.
- Keep generated data separate from real pilot data.
- Use deterministic privacy tests in addition to LLM judgments.
- Include human reviewer ratings.
- Report synthetic-only status in every derived report.
- Do not use synthetic cases as clinical evidence.

## Recommended Paper Wording

Use:

> We use synthetic conversations as a controlled benchmark for evaluating
> privacy-preserving coordination failures. We do not claim that the generated
> dialogues represent real student, parent, or teacher behavior.

Avoid:

> Students disclose more honestly to AI.

Avoid:

> The system detects student mental health risk.

Use:

> The system identifies synthetic support signals and routes them through a
> human-reviewable privacy-preserving workflow.

## Path Toward Real-World Evidence

Only after benchmark safety is stable should the project consider:

1. IRB-style protocol or equivalent ethics review.
2. Explicit consent and deletion rights.
3. Human reviewer ownership and crisis handoff.
4. Small non-clinical usability study with adults first.
5. Carefully scoped pilot with real educational stakeholders.

Until then, this remains a synthetic benchmark and research prototype.
