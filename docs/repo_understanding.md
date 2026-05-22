# Repo Understanding — Three-Party AI Safety/Benchmark Mode

**Last updated: 2026-05-20**

## Current Architecture

This repo is a Streamlit MVP for a three-party education coordination system.

- `app.py`: Streamlit UI for analysis reports, corpus/history views, live student chat, profile abstraction, coordinator, and triage.
- `src/student_agent.py`: student-facing AI wrapper.
- `src/abstraction.py`: privacy wall layer. Converts raw student chat into abstract profile JSON and now also provides deterministic privacy audit/sanitization helpers.
- `src/coordinator.py`: combines student profile + parent input + teacher input into a three-party action plan.
- `src/triage.py`: combines LLM triage with deterministic guardrails from structured profile flags and dimension scores.
- `src/profile_store.py`: local JSON profile storage, intentionally not storing raw chat history.
- `prompts/*.txt`: role and module prompts.
- `data/sagas.md`: Saga A benchmark bible.
- `data/generated_conversations/`: generated raw conversations for benchmark pressure tests.
- `data/analysis_reports/`: coordinator outputs.
- `data/dimension_scores/`: seven-dimension scoring used by cumulative strain triage.

## Current Safety Boundaries

- Raw live chat history lives only in Streamlit session state unless explicitly transformed into an abstract profile.
- Saved student profiles are JSON summaries without raw conversation text.
- `validate_no_raw_quotes()` catches exact student quote leakage.
- Privacy Wall v2 adds deterministic entity-level, event-level, numeric/proper-noun, and reconstructability checks.
- `sanitize_for_privacy()` removes sensitive keys and replaces protected terms with abstract placeholders.
- Raw conversation UI is dev-only and requires both dev mode and `SHOW_RAW_CONVERSATIONS=1` or `UMI_DEV_MODE=1`.
- Demo/pilot mode hides raw JSON expanders, scenario seeds, secret truths, and raw conversations.

## Raw Conversation Leak Points

Known risky surfaces:

- `app.py` corpus tab can show full turns, persona background, secret truth, and scenario seed in dev raw mode.
- `app.py` history tab can show scenario labels; these are hidden outside dev mode.
- `data/analysis_reports/*.json` may contain highly specific synthetic details; app display sanitizes them outside dev mode.
- `scripts/run_analysis.py` and eval scripts print details to stdout for developer workflows only.
- `prompts/persona_roleplay.txt` includes `secret_truth` and `scenario_seed`; this is generation-only and should not be used in pilot-facing UI.

## Triage

`triage.should_escalate()` now accepts optional `dimension_scores`, `previous_dimension_scores`, and `student_id`.

Deterministic rules:

- `crisis_intervention` need or emotional safety Level 3 => critical crisis intervention.
- Any dimension Level 3 => high urgency human review.
- Same Level 2 dimension across multiple reports, or trend text indicating persistence => human review / 1-on-1 recommendation.
- Worsening cumulative trajectory => escalate one level to medium urgency check-in.
- Three or more Level 1 dimensions => monitor/light intervention.
- Structured safety flags still prevent LLM downgrades.

LLM triage remains useful for language and nuance, but cannot downgrade deterministic safety guardrails.

## Tests

Pure non-LLM tests cover:

- exact raw quote leakage
- Privacy Wall v2 entity/event leakage and sanitization
- parent-facing field restriction
- triage safety flags
- cumulative strain triage
- UI mode separation
- Saga A report sanitization and dimension-score triage regression

LLM/API tests are opt-in only through `RUN_LLM_TESTS=1`.

## Current Limitations

- Privacy Wall v2 is deterministic and conservative. It catches obvious reconstructability risks but is not a semantic privacy proof.
- Entity detection is heuristic, not full Chinese NER.
- Demo/pilot sanitization protects UI display but does not rewrite existing JSON files on disk.
- Cumulative strain persistence is approximated from either previous score objects or trend notes. A real time-series store is still needed.
- Crisis escalation protocol is not yet operationalized into notifications or human handoff.
