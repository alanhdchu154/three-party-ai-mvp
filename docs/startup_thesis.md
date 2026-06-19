# Startup Thesis

**Privacy-preserving AI coordination layer for schools and family-support workflows.**

This repo is not positioned as a polished education chatbot demo. It is a
technical thesis: families, schools, and support teams need AI systems that can
hear private signals without turning private disclosure into uncontrolled
cross-party surveillance.

The current evidence is a synthetic benchmark and reference architecture. It
does not claim real-student validation, clinical validity, deployment
readiness, or outcome improvement.

## Who Would Buy

- **Schools and school networks** that need student support coordination without
  exposing raw student disclosures to every adult.
- **Student support organizations** that coordinate families, coaches,
  counselors, tutors, and case managers.
- **LMS / SIS platforms** that already hold school workflows but lack a
  privacy-aware coordination layer for sensitive human context.
- **EdTech companies** that want AI support features without becoming a parent
  surveillance product.
- **AI governance teams** that need an auditable example of party-aware
  information flow, human review, and report boundaries.

## Their Pain

Student support breaks because each party sees a different slice of reality.

Students may tell AI what they would not say directly to parents or teachers.
Parents may see grades, logistics, and family stress. Teachers may see behavior,
participation, and classroom patterns. The useful signal lives across those
perspectives, but raw disclosure cannot simply flow across parties.

The buyer problem is not "add a chatbot." The problem is safe information flow:
what can be abstracted, what must stay private, who should review it, and what
each audience can safely receive.

## What This Solves

The architecture separates disclosure from coordination:

```text
private chats
  -> abstraction
  -> privacy wall
  -> coordinator
  -> audience-safe reports
  -> human reviewer annotation
```

The product thesis is that schools and support organizations need a reusable
coordination layer that can:

- preserve raw student, parent, and teacher boundaries;
- translate private signals into abstract support needs;
- generate different internal, parent-safe, and teacher-safe views;
- keep escalation and crisis decisions human-reviewable;
- provide audit evidence that the system did not leak raw or reconstructable
  private details.

## Current Evidence v1

The current repo has synthetic conversations, privacy-wall abstraction,
audience-safe reports, deterministic leak audit, a raw-coordinator baseline, and
human reviewer annotation.

- **Baseline comparison**: 11 fixed synthetic cases compare a raw-coordinator
  baseline against the privacy-wall pipeline. The raw baseline shows
  reconstructability risk in 11/11 cases; the privacy-wall pipeline shows 0/11
  reconstructability-risk cases under deterministic checks.
- **Human reviewer annotation**: 22 notes cover 22 artifacts, including 12
  baseline artifacts, 3 audience-report artifacts, and 7 legacy calibration
  artifacts.
- **Leak audit**: current parent-safe and teacher-safe reports are 18 pass / 0
  fail under deterministic leak checks.

## What Proof Is Still Missing

The current proof is useful but still early:

- a second independent reviewer pass;
- stricter semantic privacy checks beyond deterministic leakage;
- runtime trace privacy review across intermediate prompts and tool calls;
- real-world usability evidence only after consent, deletion, provider, and
  reviewer-governance boundaries are defined.

Until those proof layers exist, this should be presented as a credible technical
asset and synthetic benchmark, not a validated school deployment.
