# Project Context — Three-Party AI Education Tool

This file is for any AI assistant (Cowork, Claude Code, etc.) picking up work on this project. Read this first.

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

### 1. Architecture document
`three_party_ai_architecture.md` — system architecture, privacy wall design, MCP positioning, mermaid diagrams, 12-week execution plan, 8 decision points pending Alan's review. (May still need to be copied into `/docs/` from the Dispatch session that produced it.)

### 2. Synthetic dataset
30 personas (10 students + 10 parents + 10 teachers), 91 conversations, includes:
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
├── CLAUDE.md              # ← this file
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
