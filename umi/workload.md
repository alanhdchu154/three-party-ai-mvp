# Umi Workload

This file is the active task handoff contract between Alan, Codex, Umi, and Claude Code.

Use this for one focused worker task at a time. Keep longer multi-agent state and open handoffs in `WORKLOG.md`.

## Active Task

### Task ID
2026-05-21-cc-generate-saga-a-conversation-smoke

### Status
READY_FOR_CLAUDE

### Assigned Worker
Claude Code

### Goal
Generate exactly one new Saga A synthetic conversation directly with Claude Code, following the scheduled task rules.

### Inputs
- CLAUDE.md
- WORKLOG.md
- docs/generation_logic.md
- docs/conversation_quality_framework.md
- data/sagas.md
- data/synthetic_dataset.json
- data/generated_conversations/index.json
- prompts/student_system.txt
- prompts/parent_system.txt
- prompts/teacher_system.txt

### Output Files
- data/generated_conversations/sim_<selected_persona_id>__<new_scenario_seed_id>.json
- data/generated_conversations/index.json

### Requirements
- Pick one persona with the fewest generated conversations, following the scheduled task tie-breaker if possible.
- Prefer `shallow` or `medium` because the corpus is currently too deep-heavy.
- Generate exactly one new conversation JSON with valid `depth`, `scenario_type`, `scenario_seed_id`, `scenario_seed`, `generated_at`, `occurred_at`, `model`, `source_type`, `expected_risk_flags`, and `turns`.
- Keep the conversation natural and consistent with Saga A canon.
- Do not make shallow conversations turn into therapy sessions.
- Update `data/generated_conversations/index.json` with the new conversation entry.
- Do not run the Python LLM generation script.
- Do not call paid APIs.
- Do not upload or publish anything.
- Do not delete files.
- Focus on this repo's real purpose: three-party AI education coordination, synthetic safety benchmark, and pilot readiness.

### Safety
- Claude Code may only write the output files listed above.
- Do not modify scripts, prompts, docs, case summaries, audience reports, dimension scores, or analysis reports.
- Do not upload to YouTube or any external service unless Umi is run with `--upload`.
- Do not call paid APIs.
- Do not delete files.

### Done Criteria
- One new conversation JSON exists.
- `index.json` includes the new conversation.
- Claude Code stdout summarizes selected persona, depth, scenario_type, scenario_seed_id, and why this is safe for the corpus.
