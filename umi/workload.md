# Umi Workload

Last updated: 2026-06-19

This file holds one active Codex / cc worker handoff at a time. The previous 2026-05-21
single-conversation handoff is stale and was removed from the active board.

## Active Task

GitHub publication readiness after Evidence v1 release gate, persona-depth
documentation, and external reviewer packaging.

Current worker should not generate new synthetic conversations. The first
baseline comparison and human reviewer annotation pass now exists. Use the
existing 348-case corpus, `scripts/run_baseline_comparison.py`, and
`data/reviewer_summaries/reviewer_annotation_summary.md` to keep GitHub / paper
claims bounded. README now includes an `Evidence v1` section, and
`docs/benchmark_datasheet.md` documents provenance, intended use, non-use,
risks, and maintenance rules. The baseline over-escalation heuristic has been
calibrated so conditional reviewer boilerplate is not treated as high-severity
escalation in shallow cases.

Persona and relationship depth are now documented in:

- `docs/persona_bible.md`
- `docs/relationship_graph.md`
- `docs/persona_depth_audit.md`

Current conclusion: the existing character and family-system layer is enough
for a synthetic benchmark / reference architecture claim. It is not evidence of
real-student validity, clinical validity, school deployment readiness, or
outcome improvement. Do not restart generation merely to add role depth; if
generation resumes later, constrain new cases with the persona bible and
relationship graph first.

External review packaging now exists:

- `docs/external_reviewer_packet.md`
- `docs/external_testing_instructions.md`
- `docs/external_reviewer_outreach.md`
- `.github/ISSUE_TEMPLATE/external-review.yml`

These files make it easier to ask outsiders for useful feedback on the
synthetic benchmark, privacy wall, public claim boundary, and evidence gaps.
They do not mean external independent validation has been completed.

Internal dry-run review exists:

- Claude Code read-only external testing review.
- Three reviewer agents: privacy/governance, school operations, and
  research/HCI.
- `docs/external_review_agent_dry_run_2026-06-19.md`

The dry run tightened the instructions around motivated-recipient
reconstructability, cross-artifact triangulation, school-ops actionability,
baseline sampling, reviewer independence, and confidentiality. It is not
external independent validation.

The one-command release-readiness gate now exists:

```bash
.venv/bin/python scripts/run_release_readiness.py
```

It reruns corpus audit, baseline comparison, reviewer summary generation,
audience-report leak audit, semantic trace audit, relationship-context leak
audit, runtime trace privacy audit, full pytest, public claim-boundary scan, and
git-visible secret scan. The latest report is
`umi/reports/release-readiness-latest.md`.

## Before Creating The Next Task

- Read `/Users/alanhdchu/umi-central/goals.md`.
- Read this repo's `WORKLOG.md`.
- Read this repo's durable roadmap at `docs/roadmap.md` when direction or
  pilot-readiness scope matters.
- Run `python3 scripts/audit_conversation_quality.py` before using corpus
  numbers.
- Current corpus evidence is 348 conversations from the 2026-06-19 audit:
  deep 85 (24.4%), shallow 142 (40.8%), medium 121 (34.8%). The project is
  framed as a synthetic benchmark / reference architecture and GitHub-first
  technical asset, not a real-student pilot claim.
- Reviewer annotation v1 exists: 37 notes / 22 reviewed artifacts, including a
  second local reviewer pass over 15 baseline/audience-report artifacts.
  New-style verdicts are 26 `safe`, 3 `privacy_concern`, and 2 `minor_issue`.
  Treat this as screening evidence, not deployment validation.
- Semantic trace audit exists: 22 pass / 0 fail across fixed-sample parent-safe
  and teacher-safe report surfaces.
- Relationship-context leak audit exists: 18 pass / 0 fail across current
  parent-safe and teacher-safe reports. It checks higher-specificity
  persona/family-system markers that can be reconstructable without being raw
  quote leaks.
- Runtime trace privacy audit exists: 51 pass / 0 fail across generated local
  runtime surfaces. It checks audience-safe reports, restricted
  reviewer/internal artifacts, pilot-run artifacts, and metadata-only audit
  logs under surface-specific privacy policies.
- Current calibrated baseline metrics on the 11-case sample: raw baseline
  reconstructability risk 11/11; privacy-wall pipeline 0 reconstructability
  risk, 0 over-escalation flags, 0 under-escalation flags, and 0 unsupported
  recommendation flags.
- Persona-depth audit exists: current personas are sufficient for the synthetic
  benchmark claim, with strongest systems around Rachel-Uncle, Shen You-Shen
  Mom, and the Michael-Keer-Michael Mom-Stepdad blended family.
- External reviewer packet and GitHub issue template exist, but no external
  independent review has been completed yet.
- External testing instructions and internal agent dry-run report exist. Treat
  them as pre-review QA, not external validation.
- External reviewer outreach messages exist. No external message has been sent
  automatically.
- Prefer `cc-first` or `Split-work` for bounded script fixes, audit review,
  report regeneration, and test runs.

## Likely Next Handoff

If work resumes, create a focused task for:

- final public GitHub push/PR packaging if Alan wants Codex to commit/push;
- inviting one privacy/governance reviewer and one school/student-support
  operations reviewer before investor or school outreach;
- optionally expanding privacy evaluation beyond local deterministic artifacts
  into production-grade runtime trace privacy review if real deployment starts;
- optionally maintaining the persona bible / relationship graph if Alan
  explicitly reopens synthetic generation or adds a new family system;
- rerunning `.venv/bin/python scripts/run_release_readiness.py`;
- preserving synthetic-data limitations and avoiding real-student validation
  claims.

Do not create a handoff for more synthetic generation until Alan explicitly
reopens generation.
