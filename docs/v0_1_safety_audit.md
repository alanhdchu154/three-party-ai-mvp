# v0.1 Safety Release Audit

**Date:** 2026-05-20

## Scope Reviewed

This audit reviews the safety-relevant diff from the Privacy Wall v2 / Cumulative Strain Triage / Demo-Pilot separation work.

Intentional safety files changed:

- `app.py`
- `src/abstraction.py`
- `src/coordinator.py`
- `src/triage.py`
- `tests/test_privacy.py`
- `tests/test_triage.py`
- `tests/test_modes.py`
- `tests/test_saga_a_regression.py`
- `docs/roadmap.md`
- `docs/repo_understanding.md`

The worktree also contains pre-existing generated data changes under `data/` and generation scripts. They are not treated as part of this release audit.

## What This Release Protects Against

- Verbatim student quote leakage from abstraction profiles.
- Named-entity leakage for protected Saga A / student-specific terms.
- Numeric detail leakage in demo/pilot surfaces.
- Event-level reconstructability when an output contains enough specific terms to identify the source event.
- Indirect identity descriptions such as "the only student who..." patterns.
- High-overlap paraphrases that avoid exact raw-quote copying.
- Coordinator output accidentally exposing `do_not_share` terms.
- Demo/pilot UI exposure of raw conversations, scenario seeds, secret truths, and raw JSON.
- LLM triage downgrading deterministic safety flags.
- Emotional safety Level 3 being treated as ordinary monitoring.

## What This Release Does Not Protect Against

- Full semantic privacy attacks where a human can infer the source from broad context not captured by deterministic terms.
- Cross-student or cross-family retrieval bugs in a future database-backed system.
- Provider-side privacy risk if real pilot data is sent to Gemini free tier or any non-approved cloud model.
- Operational crisis response. The code flags Level 3 escalation, but it does not contact humans or emergency resources.
- UI bypass by someone with local filesystem access to raw JSON files.
- Malicious prompt injection inside raw conversations that targets future LLM prompts.
- False reassurance from synthetic benchmark success. Synthetic Saga A coverage is useful for pressure testing, not proof of real-world safety.

## Safety-Critical Logic Added

- `src/abstraction.py`
  - Adds `audit_privacy_leakage()`, `reconstructability_score()`, `sanitize_for_privacy()`, and `privacy_rewrite_if_needed()`.
  - Detects raw quotes, entities, events, numeric details, indirect identity patterns, and high-overlap paraphrases.
  - Removes sensitive keys such as `turns`, `secret_truth`, `scenario_seed`, `scenario_seed_id`, `raw_conversation`, and `transcript`.
  - Redacts `_privacy_audit` metadata before attaching it to profile/coordinator outputs, because raw audit hit strings can themselves leak private details.

- `src/coordinator.py`
  - Runs coordinator output through Privacy Wall v2 using `do_not_share` / protected terms.

- `src/triage.py`
  - Adds deterministic guardrails from structured profile flags and `data/dimension_scores`.
  - Prevents LLM output from downgrading urgent deterministic flags.

- `app.py`
  - Adds explicit `APP_MODE=dev|demo|pilot`.
  - Raw conversation view requires dev mode plus `SHOW_RAW_CONVERSATIONS=1` or `UMI_DEV_MODE=1`.
  - Demo/pilot analysis surfaces sanitize output and hide raw JSON details.

## Brittle Assumptions

- Protected entity detection depends on a static term list plus caller-provided `protected_terms`.
- Chinese name/entity extraction is heuristic, not a real NER pipeline.
- Event leakage detection depends on term overlap and character n-gram similarity; it can miss clever paraphrases.
- `APP_MODE` is environment-based, so a local operator can still intentionally run unsafe dev mode.
- `data/dimension_scores` is file-based and does not yet enforce time-series ordering or source integrity.
- Persistent Level 2 detection is approximated by previous score payloads or trend text.

## Mode Bypass Risks

- Anyone with repo/filesystem access can open raw JSON directly.
- Dev mode can expose raw conversations if `UMI_DEV_MODE=1` or `SHOW_RAW_CONVERSATIONS=1`.
- Other scripts can still print raw data if called manually.
- Existing generated reports on disk may contain rich details even if the UI sanitizes them.

## Privacy Wall False Negatives

- Semantic paraphrases with low character overlap.
- Family role descriptions that do not match the indirect identity regexes.
- Details implied by combinations of otherwise generic facts.
- New proper nouns not in `_SAGA_ENTITY_TERMS` and not passed as `protected_terms`.
- Chinese numeric wording such as "三千美元" is weaker than digit-based detection.

## Privacy Wall False Positives

- Generic English titlecase words can be treated as sensitive proper nouns.
- Broad family terms may be sanitized even when safe.
- Character n-gram paraphrase detection can flag legitimate abstract summaries if they reuse too much source wording.
- Numeric details can be removed even when harmless, such as a safe weekly count.

## Pilot-Readiness Status

**Status: not pilot-ready for real student data.**

The repo is now closer to a safety benchmark harness, but v0.1 should be treated as an internal safety release only. It is suitable for local demo, synthetic benchmark review, and human safety review of Saga A outputs.

## Go / No-Go Recommendation

**No-go for real GIIS pilot with real student data.**

Go only for:

- local demo with synthetic data,
- internal review by Alan/Umi,
- privacy-wall adversarial testing,
- triage rubric calibration against synthetic or anonymized historical cases.

Before a real pilot, complete:

- local/private provider path,
- crisis handoff procedure and named human reviewer,
- time-series dimension score storage,
- source-type enforcement,
- manual privacy review of all pilot-facing surfaces.
