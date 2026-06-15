# Project Context — Three-Party AI Education Tool

This file is for any AI assistant (Codex, Claude Code / cc, or another bounded worker) picking up work on this project. Read this first.

## Central Umi coordination

This repo follows the global Central Umi coordination contract in `/Users/alanhdchu/.codex/AGENTS.md`.

- Central Umi remains Alan's primary interface and cross-project coordinator.
- `triad-product-manager` is the project manager for this repo, not a separate Umi persona.
- Claude Code / cc is a senior technical worker for bounded implementation, audit, corpus review, prompt review, and documentation tasks.
- Read `/Users/alanhdchu/umi-central/goals.md` before local planning. The central `three-party-ai-mvp` row is the v0.1 / weekly / daily routing layer; this repo's `umi/workload.md` is the active Codex/cc handoff, `WORKLOG.md` plus fresh audit output are today / last few days of current evidence, and `docs/roadmap.md` is concise durable direction.
- `WORKLOG.md` is not append-only. Completed, stale, duplicate, or fully captured items can be removed, summarized, or archived once they no longer drive the next action. Durable direction belongs in `docs/roadmap.md`.
- If the central daily goal conflicts with `WORKLOG.md` or `umi/workload.md`, pause and escalate to `triad-product-manager` / Central Umi instead of reconciling silently.
- For substantial coding or corpus-quality work, prefer `cc-first` or `Split-work` after reading `WORKLOG.md` and the current audit outputs. Coding-heavy or cc-strong work should go to cc first to balance token usage and use the right agent for the job. Umi still owns scope, acceptance, and the final Alan-facing summary.
- Before doing a substantial task locally, run the Claude Code delegation checkpoint and record `use cc` or `skip cc with reason`; do not skip cc merely because Codex/Umi can do the work.
- For deep engineering work, use a code-capable Claude Code surface such as Alan's VS Code Claude Code workflow or an equivalent code-mode CLI session with the correct repo cwd, current diff/status, scoped files, verification commands, and stop conditions. Default to the latest Opus alias (`model: opus` or `--model opus`); use Sonnet only for explicitly cheap/scouting passes. Do not treat cc-cowork/advisor chat as the primary executor for implementation, debugging, tests, diff review, or deep repo inspection.
- For assigned implementation, debugging, tests, refactor cleanup, repo-local docs, or other cc-strong execution tasks, cc has edit access from the first pass inside the allowed scope. Codex/Umi reviews the diff and accepts/rejects/revises before treating it as done.
- Do not require a numeric token/budget cap by default for cc. Use bounded scope, allowed files, expected output, and stop conditions; ask for a hard cap only if extra paid usage is enabled, external paid services are involved, Alan requests one, or the task is too broad to checkpoint safely.
- Prevent cc timeout by assigning one-pass tasks with exact allowed files and commands. Do not ask cc to run watch mode, long dev servers, full generation jobs, broad eval/browser suites, or full test suites unless explicitly scoped. If cc times out, returns no output, stalls, or needs broader scope, record the attempted repo/cwd, model target, prompt shape, allowed tools/files, elapsed time, partial output, and whether files may have changed. Stop the worker, inspect `git status` / relevant diffs if edits may have happened, narrow to one smaller code-mode pass, and retry once when safe. If retry fails, report the specific blocker instead of silently deciding, editing broadly, or treating timeout as approval.
- Translate Alan's shorthand into repo terms before assigning cc. First identify the current Three-Party goal, `WORKLOG.md` state, fresh audit needs, changed files, likely corpus/report/privacy directories, and whether cc should do all-current-diff alignment review, targeted file review, diagnosis, implementation, or verification.
- For bug-hunt or alignment questions, cc should get a findings-first review pass over current git diff/status, `WORKLOG.md`, fresh audit output, current goals, and relevant adjacent files. Do not over-narrow review to only the files Codex already suspects; let cc find regressions, missing tests, stale assumptions, and scope drift before implementation.
- Time-aware continuity applies. Scheduled generation and corpus reports can drift hourly, so old reports are historical evidence. When Alan asks about today, now, recently, or resumes an old thread, anchor to the current date/time and read current `WORKLOG.md` plus fresh audit output before answering as current.
- Project-local rules in this file control privacy, product framing, synthetic-data discipline, and repo-specific verification.
- Use `three-party-benchmark-readiness` for current corpus state, benchmark snapshot readiness, report freshness, privacy leak audit, pytest, and paper/release claim boundaries.
- Use `cc-code-mode-handoff` before substantial implementation, corpus audit wiring, report regeneration, review, cleanup, or technical documentation work.
- After meaningful Three-Party work, update `/Users/alanhdchu/umi-central/ai/HANDOFF.md` before marking the task complete.
- If Alan works directly in a Three-Party project-lead conversation, align Central Umi immediately for benchmark/paper direction changes, privacy/safety risk, real-student/pilot claims, or cross-project validation claims; align at end of turn when `WORKLOG.md`, `docs/roadmap.md`, `umi/workload.md`, corpus evidence, blocker, risk, or next action changes.

## What this product is

A three-party AI coordination tool for online education. Each party — student, parent, teacher — has their own dedicated AI to talk to privately. A **coordinator AI** synthesizes the three perspectives into a plan that is best for the student while being acceptable to all three parties. The coordinator also acts as a **triage layer**, deciding when a student needs more intensive 1-on-1 support.

## Core product thesis (the founder's own insight — preserve this)

**"AI is the only entity that can hear the truth."**

All three parties self-censor in face-to-face communication:
- Students fear being scolded
- Parents fear looking like failures
- Teachers fear complaints

People will tell AI things they would never say out loud. The product's unique value is collecting those truths and translating them between parties.

**Critical implication for design**: The student's confessions to their AI must NEVER be shown verbatim to parents or teachers. The coordinator AI translates themes / needs without exposing the raw words. Breaking this trust collapses the product's value.

## Business context

The founder is **Alan** (alanhdchu@genesisideas.school). His roles:
- **Owner of GIIS (Genesis Ideas International School)** — an online high school
- **CEO of 杰尼教育 (Jieni Education, Shanghai)** — a 1-on-1 tutoring company
- **Future possibility**: management role at a Shanghai International School

This product is designed as a **two-stage funnel between two organizations Alan controls**:

```
GIIS (online HS, broad reach, lead-gen)
        ↓
AI triage (this product's coordinator)
        ↓
杰尼教育 (1-on-1, premium, monetization)
```

Implications:
- The coordinator AI is **simultaneously a coordination tool AND a triage / diagnostic layer**. When student/parent/teacher input shows a student needs more than scale services can offer, the system recommends escalation to 杰尼's 1-on-1.
- **No "selling to schools" friction.** Alan is the owner. Pilot can deploy internally as soon as code is ready. Bottleneck is product, not distribution.
- **Target audience is GIIS students first, then 杰尼.** NOT Taiwan general K-12 market — that framing was explicitly rejected by Alan.

## How to collaborate with Alan

- He writes in **Traditional Chinese**. Respond in Traditional Chinese unless he switches.
- He thinks in **product / business model terms**, not just feature terms. He spotted the GIIS → 杰尼 AI-triage funnel himself.
- Treat him as a **founder/CEO** — he can make and execute decisions unilaterally.
- He prefers **direct, candid advice** over diplomatic hedging. He asked for honest recommendations on monetization and accepted pushback.
- He explicitly **rejected user interviews** as a starting point — because he believes users won't tell the truth in interviews either, only to AI. Don't suggest interview-driven research as a default.

## What has been built so far

This section contains historical project context. For current corpus counts and
generated-conversation distribution, always read `WORKLOG.md` first and run
`python scripts/audit_conversation_quality.py`; scheduled generation can change
the numbers every hour.

### 1. Architecture document
`three_party_ai_architecture.md` — system architecture, privacy wall design, MCP positioning, mermaid diagrams, 12-week execution plan, 8 decision points pending Alan's review. (May still need to be copied into `/docs/` from the Dispatch session that produced it.)

### 2. Synthetic dataset
The original seed dataset used 30 personas (10 students + 10 parents + 10 teachers) and 91 conversations. The active corpus is now larger and should be treated as a moving snapshot. It includes:
- Crisis escalation arcs (passive ideation, not active emergency)
- Hidden help-seeking (bullying, sexual orientation, learning disability, abandonment threat)
- Privacy probe attacks from parents (legal framing, technical gray zones, panic pressure, advice reverse-engineering)
- Three-party signal contradictions
- Cultural sensitivity (Chinese family frameworks: 孝順, 丟臉, 移民翻身焦慮)
- Misjudgment traps (high-functioning depression, gifted burnout)
- Triage escalation triggers
The JSON likely needs to be copied into `data/synthetic_dataset.json` from the Dispatch session.

### 3. The MVP repo (this folder)
- **Stack**: Python + Streamlit + LiteLLM
- **Default provider**: `gemini/gemini-2.5-flash` (free tier)
- **Privacy wall**: `validate_no_raw_quotes()` checks that profile JSON never contains student's verbatim sentences
- **Modules**:
  - `src/student_agent.py` — student chat handler
  - `src/abstraction.py` — raw conversation → Profile JSON (no raw quotes)
  - `src/coordinator.py` — synthesizes 3-party inputs into plans + per-party messages
  - `src/triage.py` — escalation decision (1-on-1, counseling, emergency)
  - `src/profile_store.py` — JSON file storage with atomic writes + path traversal protection
  - `src/llm.py` — LiteLLM wrapper, provider-agnostic
- **Prompts** in `prompts/*.txt` — externalized so Alan can iterate without touching Python
- **Tests** in `tests/` — pure logic tests + API-required tests (auto-skip if no key)
- **Eval script**: `scripts/run_dataset_eval.py` — runs synthetic dataset through the system

### 4. Provider strategy (phased)
- **Now / dev**: Gemini Flash (free, generous quota, but free-tier data may be used for training — DO NOT put real student data through it)
- **Real GIIS pilot**: Ollama local (Qwen2.5 / Llama3.x) — completely free + privacy compliant
- **杰尼 Shanghai deployment**: DeepSeek (very cheap, China-domestic compliant)

Switching providers requires only changing `LLM_MODEL` in `.env` and the corresponding API key.

## Open follow-ups (in priority order)

### A. Persona depth rebuild
Alan finds the current student personas too "symptom-classification" and wants them rebuilt using **anime / classic-literature character archetypes** as personality skeletons. Suggested archetypes already discussed:

**Anime**: 比企谷八幡 (intellectualized cynicism), 我妻善逸 (high-functioning anxiety), 友利奈緒 (dissociation), 御坂美琴 (high-achiever + family pressure), parentified eldest child, 五條悟 (performative bravado masking loneliness)

**Literary**: 林黛玉 (sensitivity + illness mindset), 賈寶玉 (passive resistance to family expectations), Holden Caulfield (alienation), Esther Greenwood (high-achiever depression), Hermione Granger (perfectionism breakdown), 安藤潤子 (artistic obsession)

**Alan needs to pick 5-7 to prioritize** before the regeneration runs. Method: use each archetype as a personality skeleton, then add a realistic GIIS-context overlay (year, family situation, location).

### B. MVP cleanup (low priority)
There may be stale `__pycache__/`, `.pytest_cache/`, or a nested duplicate folder from earlier copy operations. If present, can be cleaned with:
```bash
cd ~/three-party-ai-mvp && \
  rm -rf __pycache__ .pytest_cache pytest-cache-files-* \
         src/__pycache__ tests/__pycache__ scripts/__pycache__ \
         three-party-ai-mvp
```

### C. Strategic positioning (unresolved)
Whether to scope this product as:
1. Pure internal tool for GIIS + 杰尼 (competitive moat)
2. Internal-validated then external SaaS
3. Independent third entity / portfolio company

Alan has not committed. Revisit when there's real pilot traction.

### D. Security reminder
Alan shared a Gemini API key in plaintext chat during the Dispatch session. He has agreed to **rotate the key after testing**. If you see him still using the same key after a few days, remind him.

## Tone reminders

- Don't be sycophantic. Push back when his ideas have flaws.
- Don't pad with summaries he can read in the diff.
- Avoid em-dashes (he hasn't said so but the host UI prefers conversational tone).
- Skip bullet-list overload in normal chat — reserve lists for spec docs.
- He responds well to direct honest recommendations even if uncomfortable.

## Files in this repo

```
three-party-ai-mvp/
├── README.md              # User-facing, includes free-provider guide
├── AGENTS.md              # ← this file
├── requirements.txt       # streamlit, litellm, pydantic, pytest, python-dotenv
├── .env / .env.example    # provider keys
├── .gitignore
├── app.py                 # Streamlit UI: chat tab, profile tab, coordinator tab, triage tab
├── src/                   # core modules (see "What has been built")
├── prompts/               # *.txt prompts — edit freely
├── data/
│   ├── dummy_inputs.json          # 3 hard-coded parent/teacher inputs for demos
│   └── synthetic_dataset.json     # 91-conversation test dataset (paste from prior session)
├── tests/                 # pytest tests using synthetic dataset
└── scripts/
    └── run_dataset_eval.py        # batch eval; supports EVAL_LIMIT=N for cost control
```

## Quick start (for Alan)

```bash
cd ~/three-party-ai-mvp
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# .env already populated with Gemini key
streamlit run app.py
```

Browser opens at `http://localhost:8501`.
