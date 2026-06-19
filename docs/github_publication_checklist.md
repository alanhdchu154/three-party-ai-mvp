# GitHub Publication Checklist

Last updated: 2026-06-19

## Status

This repository is ready to share as a public synthetic benchmark and reference
architecture if the current release gate remains green:

```bash
.venv/bin/python scripts/run_release_readiness.py
```

Current gate result:

- Release readiness: PASS
- Corpus: 348 synthetic conversations
- Raw coordinator baseline reconstructability risk: 11/11 cases
- Privacy-wall pipeline reconstructability risk: 0/11 cases
- Audience report leak audit: 18 pass / 0 fail
- Semantic trace audit: 22 pass / 0 fail
- Relationship leak audit: 18 pass / 0 fail
- Reviewer annotation: 37 notes / 22 artifacts
- Second local reviewer coverage: 15 baseline/audience artifacts
- Full pytest: 77 passed / 7 skipped
- Public claim-boundary scan: no positive overclaim hits
- Git-visible secret scan: no secret-like values found

## Public Claim Boundary

Safe public framing:

> Synthetic benchmark and reference architecture for privacy-preserving,
> human-led, multi-party student support coordination.

Do not claim:

- real-student validation;
- clinical validity;
- deployment readiness for minors;
- outcome improvement;
- autonomous counseling or crisis response;
- proof that synthetic disclosure patterns match real schools or families.

## What To Share

Good public entry points:

- `README.md`
- `docs/startup_thesis.md`
- `docs/literature_review.md`
- `docs/benchmark_datasheet.md`
- `umi/reports/release-readiness-latest.md`
- `umi/reports/baseline-comparison-latest.md`
- `umi/reports/semantic-trace-audit-latest.md`
- `umi/reports/relationship-leak-audit-latest.md`
- `data/reviewer_summaries/reviewer_annotation_summary.md`

## Before Pushing

Run:

```bash
.venv/bin/python scripts/run_release_readiness.py
git diff --check
git status --short --untracked-files=all
```

Confirm that no `.env`, real student data, API keys, private school records, or
unreviewed generated raw data are staged. Synthetic generated conversations are
part of the benchmark only under the synthetic-data claim boundary.

## Good Next Public Step

After publishing, the next useful proof is not more synthetic corpus growth. It
is either:

- an external independent reviewer pass;
- stronger semantic privacy evaluation beyond deterministic report checks;
- a small reviewer UI for inspecting evidence refs and report surfaces.
