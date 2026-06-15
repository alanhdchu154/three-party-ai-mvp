# Research Positioning

Last updated: 2026-06-11

## One-Sentence Framing

This project is a research prototype and synthetic benchmark for evaluating
privacy-preserving, human-led coordination in multi-party student support
scenarios.

It is not currently positioned as a GIIS/Jieni deployment, a counseling product,
or evidence that real students will disclose to AI in the same way.

## Research Problem

Students, parents, and teachers often hold asymmetric information about a
student's needs. A student may privately disclose distress or confusion; a
parent may frame the same situation as discipline or achievement; a teacher may
only see classroom behavior. A coordination system must help adults respond
without exposing raw disclosures or turning support infrastructure into
surveillance.

The central research question is:

> How can LLM-based systems support multi-party educational coordination while
> preserving contextual privacy boundaries between students, parents, and
> teachers?

## What This Project Claims

This project can claim:

- It defines a multi-party educational support benchmark with student, parent,
  and teacher perspectives.
- It models different conversation depths: shallow, medium, and deep.
- It includes privacy-sensitive failure modes such as raw quote leakage,
  entity/event leakage, reconstructability, privacy probes, and misuse attempts.
- It implements a reference architecture: private party chats, abstraction,
  privacy wall, coordinator, triage, party-aware reports, and human review.
- It can evaluate whether a coordination pipeline leaks private information,
  over-escalates shallow conversations, under-escalates high-risk synthetic
  cases, or produces recommendations without sufficient evidence.

## What This Project Does Not Claim

This project must not claim:

- Synthetic conversations represent real students, parents, or teachers.
- Students will disclose to AI in real deployments at the rates shown here.
- The system improves mental health, learning outcomes, retention, or family
  relationships.
- The system is clinically valid or suitable for autonomous counseling.
- The system is ready to handle real minors' data without consent, reviewer
  ownership, data deletion, and crisis handoff procedures.

## Research Contribution

The contribution is best described as a benchmark plus system paper:

1. **Problem formulation**: multi-party educational support as a contextual
   privacy and coordination problem.
2. **Synthetic benchmark**: a controlled corpus for testing coordination
   failures that would be risky to discover first with real minors.
3. **Reference architecture**: a privacy-wall pipeline separating private
   disclosure, abstracted profiles, coordinator synthesis, triage, and
   audience-safe reporting.
4. **Evaluation protocol**: leakage, reconstructability, false escalation,
   under-escalation, evidence discipline, and human-reviewability metrics.

## Best-Fit Research Areas

- HCI / CSCW: multi-party coordination, family-school information boundaries,
  human-AI decision support.
- Responsible AI / AI safety: privacy leakage, human review, minors and
  sensitive disclosures.
- Learning analytics / AIED: early support signals and student success
  coordination, with no claim of outcome improvement yet.
- NLP evaluation: synthetic dialogue benchmark and model/pipeline evaluation.

## Related Work Anchors

Use these as starting points, not as a final literature review:

- Contextual Integrity: privacy as appropriate information flow, not simply
  secrecy. This is the theoretical frame for why raw student disclosures should
  not flow to parents/teachers while abstract support needs may.
- Multi-agent LLM privacy leakage benchmarks such as AgentLeak: useful for
  framing leakage across internal agent channels, memory, tools, and outputs.
- Learning analytics early-warning systems: adjacent but often focused on
  behavioral/academic data rather than private multi-party dialogue.
- AI chatbot safety for minors: motivates human-led boundaries and avoiding
  autonomous counseling claims.
- Synthetic dialogue generation research: supports synthetic data as a useful
  benchmark material while requiring explicit limitations.

## Current Strategic Decision

The active route is now:

> Research prototype + synthetic benchmark first.

GIIS/Jieni are no longer the active framing. They can remain historical product
context or possible future deployment settings, but they should not drive the
paper claims or immediate roadmap.
