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
audience-safe reports, deterministic privacy audits, a raw-coordinator baseline,
local reviewer annotation, and a one-command release-readiness gate.

- **Baseline comparison**: 11 fixed synthetic cases compare a raw-coordinator
  baseline against the privacy-wall pipeline. The raw baseline shows
  reconstructability risk in 11/11 cases; the privacy-wall pipeline shows 0/11
  reconstructability-risk cases, 0 over-escalation flags, and 0
  under-escalation flags under deterministic checks.
- **Reviewer annotation**: 37 notes cover 22 artifacts, including 12 baseline
  artifacts and 3 audience-report artifacts, with a second local reviewer pass
  over 15 baseline/audience-report artifacts.
- **Privacy audits**: current parent-safe and teacher-safe reports are 18 pass /
  0 fail under audience-report leak checks, 22 pass / 0 fail under semantic trace
  checks, 18 pass / 0 fail under relationship-context checks, and 51 pass / 0
  fail under runtime trace checks over generated local benchmark artifacts.
- **Release gate**: `.venv/bin/python scripts/run_release_readiness.py` is
  currently PASS, with 89 passed / 7 skipped tests.

## What Proof Is Still Missing

The current proof is useful but still early:

- an external independent reviewer pass from privacy/governance and
  school-support operations reviewers;
- stronger reviewer-agreement reporting and disagreement handling if this moves
  toward a paper claim;
- production-grade runtime trace privacy review if the system moves beyond
  generated local benchmark artifacts;
- real-world usability evidence only after consent, deletion, provider,
  escalation, and reviewer-governance boundaries are defined.

Until those proof layers exist, this should be presented as a credible technical
asset and synthetic benchmark, not a validated school deployment.
