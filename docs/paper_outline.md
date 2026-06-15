# Paper Outline

Last updated: 2026-06-11

## Working Title

**A Synthetic Benchmark for Privacy-Preserving Multi-Party Student Support
Coordination**

Alternative:

**Privacy Walls for Multi-Party Educational AI: A Synthetic Benchmark and
Reference Architecture**

## Abstract Draft

Students, parents, and teachers often hold different and sometimes conflicting
information about a student's needs. LLM-based educational support tools may
help coordinate these perspectives, but they also create privacy risks when raw
disclosures or reconstructable details flow between parties. We present a
synthetic benchmark and reference architecture for privacy-preserving
multi-party student support coordination. The benchmark includes student,
parent, and teacher conversations across shallow, medium, and deep disclosure
depths, including daily-life interactions, misuse attempts, privacy probes, and
support-risk scenarios. The system separates private dialogue, abstracted
profiles, privacy-wall auditing, coordinator synthesis, triage guardrails,
party-aware reporting, and human review. We evaluate privacy leakage,
reconstructability, shallow false escalation, high-risk under-escalation, and
evidence discipline. We do not claim that synthetic dialogues represent real
student behavior; rather, we use them as a controlled testbed for identifying
coordination and privacy failures before real-world deployment.

## 1. Introduction

- Educational support is multi-party: students, parents, teachers, reviewers.
- Each party sees only part of the situation.
- LLM systems may collect more private disclosures, but privacy boundaries are
  fragile.
- The research gap: existing tutoring/early-warning systems rarely model
  cross-party disclosure boundaries.
- Contribution summary:
  - problem formulation,
  - synthetic benchmark,
  - reference architecture,
  - evaluation protocol.

## 2. Related Work

### Contextual Privacy

- Contextual Integrity.
- Appropriate information flows.
- Children's privacy literacy and privacy norms.

### LLM Privacy and Agent Leakage

- Multi-agent leakage benchmarks.
- Internal channel leakage, memory, tool calls, output-only audit limitations.

### Learning Analytics and Student Support

- At-risk identification.
- Early-warning systems.
- Ethical and privacy issues in learning analytics.

### AI Chatbots for Minors

- Risks of over-reliance, weak crisis response, parental controls, and privacy
  policy limitations.

### Synthetic Dialogue Benchmarks

- Synthetic dialogue generation as controlled evaluation material.
- Limitations of synthetic-only claims.

## 3. Benchmark Design

- Personas and roles.
- Student/parent/teacher private conversations.
- Depth labels: shallow, medium, deep.
- Scenario types.
- Privacy probes and misuse attempts.
- Derived artifacts:
  - dimension scores,
  - case summaries,
  - audience reports,
  - trajectory reports.
- Snapshot and split policy.

## 4. System Architecture

Pipeline:

1. Private party conversations.
2. Abstraction layer.
3. Privacy wall.
4. Party profiles.
5. Coordinator.
6. Cumulative strain triage.
7. Party-aware reports.
8. Human reviewer gate.

Include a diagram in the final paper.

## 5. Evaluation

### Research Questions

- RQ1: Does the privacy wall reduce raw quote/entity/event leakage compared with
  raw coordination?
- RQ2: Does the system avoid over-escalating shallow daily-life conversations?
- RQ3: Does the system preserve high-risk synthetic escalation flags?
- RQ4: Are recommendations evidence-grounded and human-reviewable?
- RQ5: Do party-aware reports provide actionable guidance without revealing
  cross-party secrets?

### Metrics

- leakage rates,
- reconstructability,
- false escalation,
- under-escalation,
- evidence reference completeness,
- reviewer ratings.

## 6. Results Placeholder

Tables to fill after evaluation:

- Corpus snapshot table.
- Privacy leakage table.
- Triage table.
- Reviewer table.
- Examples of safe vs unsafe outputs.

## 7. Discussion

- Privacy as translation, not disclosure.
- Why minors and family/school contexts require stricter boundaries.
- Why synthetic benchmarks are useful before real deployment.
- Human reviewer role.
- Risks of parent surveillance framing.

## 8. Limitations

- Synthetic-only data.
- No real behavioral validation.
- No clinical validity.
- Possible generator bias.
- Possible circularity if LLMs generate and evaluate.
- English/Chinese/cultural context limitations depending on snapshot.

## 9. Ethics and Safety

- No autonomous counseling claim.
- No real minors' data in benchmark.
- Human review required before any real deployment.
- Consent/deletion/crisis handoff required for future pilot.

## 10. Conclusion

The paper argues for a privacy-preserving benchmark and architecture for
multi-party educational support coordination. The main claim is not that the
system solves student wellbeing, but that this class of system needs explicit
privacy-wall and human-review evaluation before deployment.

## Candidate Venues

- HCI / CSCW-style venue if framed around multi-party coordination and privacy.
- FAccT / AIES-style venue if framed around responsible AI for minors and
  privacy.
- AIED / LAK-style venue if framed around student support infrastructure.
- ACL/EMNLP workshop if framed around synthetic dialogue benchmark and LLM
  privacy evaluation.
