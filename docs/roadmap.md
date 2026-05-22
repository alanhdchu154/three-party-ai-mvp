# Three-Party AI — Roadmap

**最後更新：2026-05-21**

這份是 living doc。每完成一件事就在這裡 mark complete，每出現新的 scope 改動就更新對應 phase。

---

## 北極星 (North Star)

**核心信念**：大部分人不是沒有秘密，而是沒有一個安全、低壓、不中斷關係的地方可以把秘密說出來。當一件事已經能對真人親口說出來時，很多時候那個人其實已經跨過最痛、最孤單、最混亂的那道坎。AI 的價值是成為更早期、更低摩擦的承接層。

**短期**：在 GIIS 這個 online high school 場景中，驗證「學生 / 家長 / 老師各自跟 AI 說出更真實的資訊，coordinator 安全翻譯成支持行動」是否成立。

**中期**：把 GIIS 的 learning data、學生 AI 對話、家長 AI 對話、老師 AI observations 整合成 **AI Student Success & Support Layer**，判斷學生下一步真正需要什麼支持。

**長期**：把這套 privacy-preserving truth capture + support coordination layer 推向更廣市場：online schools、international programs、tutoring organizations、families，甚至一般人用來整理自己不敢說出口的困難。但 GIIS 仍是第一個 proof point，不是唯一終點。

**杰尼定位**：杰尼是 optional routing destination，不是唯一商業主線。只有當 case 屬於 academic support、study planning、learning gap、exam pressure、1-on-1 mentoring 能解決的問題時，才應導向杰尼。

---

## Version Ladder — v0.5 到 v1.0

目前版本：`0.11.0-party-aware-reporting`

這個版本號是「產品成熟度」，不是 production readiness。v1.0 的定義不是功能做滿，而是：**可以安全地跑一個小規模 GIIS 真實 pilot，並且能把 AI 的建議、人類 review、隱私邊界、triage handoff 全部留下可審計紀錄。**

### v0.5 — Synthetic Calibration Release ✅

**狀態**：已完成。

**用途**：
- synthetic benchmark review
- case summary / trajectory report 生成
- reviewer notes 校準
- rule confidence vs calibrated confidence 分離

**不是**：
- 真實學生 pilot
- parent-facing system
- teacher-facing system
- clinical / counseling tool

### v0.6 — Pilot Readiness Pack ✅

**狀態**：已完成 deterministic baseline。仍需要 Alan 確認實際 human owner。

**目標**：把目前 internal reports 拆成不同 audience 的安全輸出，並補齊 pilot 前的文件與配置。

**必做**：
- [x] `internal_reviewer` / `parent_safe` / `teacher_safe` 三種 report variant（2026-05-21）
- [x] reviewer assignment config example：primary reviewer、backup reviewer、Level 3 SLA（2026-05-21）
- [x] pilot onboarding checklist（2026-05-21）
- [x] consent / privacy explanation draft baseline（2026-05-21）
- [x] emergency / crisis checklist via crisis handoff runbook（2026-05-21）
- [x] existing `source_type` migration script + run（2026-05-21）
- [x] existing dimension score snapshot backfill script + run（2026-05-21）

**Exit criteria**：
- parent_safe / teacher_safe report 不含 raw secrets、scenario seeds、do_not_share 細節
- crisis Level 3 有明確 human owner，不只是 code flag
- 所有 existing artifacts 有 source type
- 所有 current dimension scores 有 snapshot

### v0.7 — Local Provider & Data Boundary Release ✅

**狀態**：文件與 config 邊界已完成；local provider full loop 仍需在 Alan 的機器上用 real selected model 做一次手動驗證。

**目標**：真實學生資料不進 Gemini free tier；本機或 approved provider path 可以跑完整 loop。

**必做**：
- [x] Ollama local provider runbook baseline in README / provider matrix（2026-05-21）
- [x] provider safety matrix：Gemini dev-only、Ollama pilot、DeepSeek/Jieni future（2026-05-21）
- [x] `.env.example` 明確標註真實資料禁用 provider（2026-05-21）
- [ ] smoke test：student chat → abstraction → coordinator → triage 全流程可在 selected local/private provider 跑
- [x] no-network / no-API-key default test posture preserved（2026-05-21）

**Exit criteria**：
- Alan 可以在本機用 local/private provider 跑一個假學生 session
- README 清楚寫哪些 provider 可以/不可以處理真資料
- CI/default tests 不需要外部 LLM key

### v0.8 — Controlled Internal Pilot Harness ✅

**狀態**：已完成 existing-artifact harness。注意：目前不跑真實 conversation loop，也不打 LLM。

**目標**：不是正式 pilot，而是 Alan/Umi 自己可以用 pilot mode 模擬真實流程，檢查資料留存、review、handoff。

**必做**：
- [x] pilot mode controlled harness script（2026-05-21）
- [x] one-student data folder isolation under `data/pilot_runs/`（2026-05-21）
- [x] audit log：controlled run writes append-only JSONL metadata（2026-05-21）
- [x] reviewer CLI：不用手寫 JSON（2026-05-21）
- [x] red-team privacy scan for one complete Michael smoke case（2026-05-21）

**Exit criteria**：
- 一個測試學生可以完整跑完 existing artifacts → case summary → safe reports → trajectory → reviewer calibration → audit log
- 可以刪除或封存該測試學生資料
- privacy audit 對 pilot-facing reports 通過

### v0.9 — GIIS Pilot Candidate + Market Thesis Release

**狀態**：產品 thesis / pilot ops 文件 baseline 已完成；仍需 provider + crisis notification final sanity pass 才能進真實家庭。

**目標**：準備進 1-2 個真實 GIIS 家庭的 extremely controlled pilot，同時把「可賣給誰、解決什麼問題、怎麼證明有用」寫清楚。

**必做**：
- [x] Problem validation doc：明確定義 truth capture、privacy-preserving translation、support routing 要解決的問題（2026-05-21）
- [x] Market positioning doc：GIIS / online school / tutoring org / family B2C / broader personal AI support 的客戶假設與風險（2026-05-21）
- [x] 1-2 家庭 pilot protocol（2026-05-21）
- [x] student / parent onboarding wording（2026-05-21）
- [x] opt-out / data deletion procedure（2026-05-21）
- [x] parent-safe expectation setting：AI 會保護學生原話，不提供秘密內容（2026-05-21）
- [x] Level 2 / Level 3 escalation tabletop exercise（2026-05-21）
- [x] Alan time budget：每週最多 3 小時；Umi primary reviewer、Mahiru backup reviewer（2026-05-21）

**Exit criteria**：
- Alan 能清楚對家長說：系統會做什麼、不會做什麼、什麼情況會升級
- Alan 能清楚對潛在買家說：這不是偷看孩子秘密，而是安全承接秘密、翻譯 pattern、協調支持
- Roadmap 不再把杰尼漏斗當唯一目的，而是把杰尼視為合理支持路由之一
- Level 3 不依賴 AI 自己判斷後續，而是指定人類流程
- pilot 家庭不是被當成產品實驗白老鼠，而是有明確退出與保護機制

### v0.10 — Three-Party Abstraction Layer ✅

**狀態**：deterministic baseline 已完成。這修正了一個重要產品問題：不能只有學生被抽象化，家長與老師也需要同等的 self-disclosure privacy boundary。

**目標**：讓 coordinator 接收三方 abstracted profiles，而不是把家長/老師當成 raw text input。系統仍然 student-centered，但 coordination 必須 party-fair。

**已完成**：
- [x] 新增 `PARTY_PROFILE_FIELDS`，包含 concerns、needs、fears/constraints、blind spots、what they can offer、safe summary、`what_not_to_share`（2026-05-21）
- [x] 新增 `normalize_party_profile()`，可把家長/老師輸入轉成 deterministic party profile baseline（2026-05-21）
- [x] 新增 `party_profile_view()`，預設隱藏成人 `what_not_to_share`，只在 `internal_reviewer` view 顯示（2026-05-21）
- [x] Coordinator 改為接收 `student_profile + parent_profile + teacher_profile`，並把成人 `what_not_to_share` 納入 protected terms（2026-05-21）
- [x] Coordinator prompt 更新為 `student-centered, party-fair coordination`，明確禁止洩漏任何一方的 raw words / private constraints（2026-05-21）
- [x] 新增 party abstraction tests，覆蓋家長/老師 profile normalization、view gating、coordinator sanitization（2026-05-21）
- [x] Streamlit active case selector 從 sidebar 移到 `💬 三方 Live` 主工作區，sidebar 只保留 status summary（2026-05-21）
- [x] `💬 三方 Live` 新增學生 / 家長 / 老師三個 live chat entry points，家長與老師可各自更新 party profile（2026-05-21）
- [x] 新增 `src/party_agent.py` + parent/teacher prompts，成人 AI 回覆遵守不索取/不暴露學生秘密的 boundary（2026-05-21）
- [x] `src/profile_store.py` 新增 parent/teacher party profile atomic save/load；保存 abstraction，不保存 raw turns（2026-05-21）

**仍未完成**：
- [ ] 家長/老師各自的 LLM abstraction prompt；目前保存 profile 使用 deterministic privacy-safe abstraction baseline
- [ ] 更完整的三方 reviewer dashboard，例如一次比較 needs / constraints / blind spots / what each party can safely offer
- [ ] case summary / audience reports 納入 parent/teacher needs、constraints、blind spots 的更完整呈現

**Exit criteria**：
- coordinator 不再直接依賴 raw parent / raw teacher statements
- 三方都有自己的 private disclosure boundary
- student raw secrets、parent `what_not_to_share`、teacher `what_not_to_share` 都不會出現在 cross-party outputs
- 使用者在主面板完成 active case selection，不再被 sidebar selector 與 tab-specific selectors 混淆

### v0.11 — Party-Aware Reporting ✅

**狀態**：已完成 deterministic + optional LLM baseline。重點是讓三方 abstraction 不只進 coordinator，也進 case summary / audience reports。

**目標**：把 parent/teacher needs、constraints、blind spots、what each party can offer 變成可審計的 report layer，同時保護 raw turns、student secrets、adult `what_not_to_share`。

**已完成**：
- [x] 新增 `prompts/parent_abstraction.txt` 與 `prompts/teacher_abstraction.txt`，定義成人 LLM abstraction JSON schema 與安全邊界（2026-05-21）
- [x] 新增 `extract_party_profile_llm()` 與 `extract_party_profile_with_fallback()`：可用 LLM abstraction，但本機/失敗時回 deterministic baseline（2026-05-21）
- [x] LLM party abstraction 產物會通過 Privacy Wall v2 audit；命中 protected entities 時強制 sanitize（2026-05-21）
- [x] Analysis Layer `student_case_summary` 新增 `party_profiles` 與 `coordination_snapshot`（2026-05-21）
- [x] Internal case report 新增 `Three-Party Coordination Snapshot`：Student / Parent / Teacher / Coordination Problem / Risks / Safe Bridges（2026-05-21）
- [x] Parent-safe / teacher-safe audience reports 新增 party-aware guidance 與 privacy boundary，仍不顯示 raw evidence claims（2026-05-21）
- [x] 重新生成 `data/case_summaries/*.md` 與 `data/audience_reports/*/*.md`（2026-05-21）
- [x] 新增 regression tests：LLM party abstraction sanitization、coordination snapshot schema、audience report privacy（2026-05-21）

**仍未完成**：
- [ ] Streamlit reviewer UI 尚未直接顯示 `coordination_snapshot`
- [ ] parent/teacher LLM abstraction 在 Ollama timeout 情況下仍預設走 deterministic fallback
- [ ] party-aware reports 還沒有 human reviewer annotation flow

**Exit criteria**：
- case summary 能說明三方各自 needs / constraints / blind spots / safe offers
- parent_safe / teacher_safe reports 可行動，但不暴露其他方秘密
- LLM abstraction 不能把 protected entities 或 high-specificity events 寫進 party profile

### v1.0 — GIIS Micro-Pilot Release

**目標**：安全跑 3-5 個 GIIS 真實學生/家庭，驗證核心產品假設：AI 能否更早承接真話，並在不洩漏秘密的前提下，把它轉成可行動的支持。

**v1.0 成功標準**：
- 0 raw quote / raw secret 跨方洩漏
- 100% Level 3 human review
- 90%+ triage / reviewer agreement on high-risk cases（小樣本）
- 每個家庭都有 signed consent / onboarding record
- 每個 AI recommendation 都能追到 evidence refs 或 reviewer note
- 至少 2 個 case 產生有價值的 student disclosure，但沒有破壞信任
- 至少 1 個 case 能合理判斷是否需要 teacher support / parent coaching / school human review / external counseling / 杰尼 1-on-1 其中一種 routing

**v1.0 仍然不是**：
- 對外 SaaS
- 自動心理諮商
- 自動危機干預
- 可無人監督處理未成年人資料的系統

### 合理性評估

**技術上合理**：v0.6 到 v0.8 多數是資料邊界、報告分層、review workflow、provider runbook，不需要重寫架構，也不需要 ML / vector DB。這是合理的工程路線。

**產品上合理**：v1.0 不該定義成「很多功能」，而應該定義成「3-5 個真實家庭安全跑完」。GIIS 是第一驗證場，不代表未來只能賣給 GIIS 或學校。

**最大風險不是技術**：真正 bottleneck 是 human operations：誰 review、多久 review、遇到 Level 3 怎麼辦、家長怎麼理解「AI 會保護學生原話」。這些沒做完，再多模型都不能上真學生。

**時間估計**：
- v0.6：2-4 天，如果只做文件 + deterministic report variants
- v0.7：1-3 天，取決於 local provider 是否已穩
- v0.8：3-5 天，要把 review / audit / pilot harness 串起來
- v0.9：3-7 天，主要是 operational docs + tabletop exercise
- v1.0：2-4 週，因為真實家庭 pilot 需要等待人、溝通、觀察，不是 coding speed 決定

**我的判斷**：到 v0.8 很快且合理；到 v1.0 合理但不能硬趕。v1.0 的節奏應該由「第一批真實家庭願不願意、安全不安全」決定，不是由 repo 裡有多少功能決定。大眾市場可以是遠方，但第一步仍需要 GIIS 這種可控場域來證明 trust loop。

---

## Phase 1 — MVP & GIIS 內部 Pilot

**目標**：跑得起來、跑得安全、跑得真。先讓 1-2 個真實 GIIS 家庭使用，驗證核心假設，再擴到 3-5 個家庭。

**時間預估**：4-8 週（依招募 pilot 家庭速度）

**成功指標**：
- 80%+ 學生對話包含至少一個「AI is the only entity that can hear the truth」moment（內部評分）
- 0 verbatim 原話跨方洩漏（自動 audit）
- Triage 決策跟人類專家 agreement > 90%（小樣本人工標註）
- Pilot 家庭 NPS > 40
- 至少 2 個 case 產生清楚 support routing decision；可能是老師支持、家長溝通、學校 reviewer、外部諮詢、或杰尼 1-on-1

### 已完成 ✅
- [x] 系統架構文件（three_party_ai_architecture.md）
- [x] 核心 modules 骨架：`src/student_agent.py` / `src/abstraction.py` / `src/coordinator.py` / `src/triage.py` / `src/profile_store.py` / `src/llm.py`
- [x] Streamlit UI 骨架（`app.py` 四個 tab）
- [x] 外部化 prompts (`prompts/*.txt`)
- [x] 隱私牆基礎檢查 `validate_no_raw_quotes()`
- [x] Synthetic dataset 重寫：聚焦 Michael Saga，9 個 personas、9 段對話（2026-05-17, 後縮回 Saga A only）
- [x] Coordinator 建議維度規格（`docs/coordinator_dimensions.md`）（2026-05-17）
- [x] `dummy_inputs.json` Saga A 對齊：Michael / Rachel / 沈又 三組家長+老師 demo case（2026-05-17）
- [x] Streamlit 分析 UI 擴充：三方分析、對話庫、歷史資訊、七維度 scorecard（2026-05-20）
- [x] Raw conversation dev-only gate：`對話庫` 原話檢視需明確設定 `SHOW_RAW_CONVERSATIONS=1` 或 `UMI_DEV_MODE=1`（2026-05-20）
- [x] Triage deterministic guardrail：結構化 safety / crisis / academic flags 不能被 LLM 降級成 `none`（2026-05-20）
- [x] LLM API tests 改為 opt-in：需 `RUN_LLM_TESTS=1` 才會打外部模型，避免本機 / CI 被 API key 或網路狀態污染（2026-05-20）
- [x] Repo understanding report：`docs/repo_understanding.md` 記錄 current architecture / safety boundaries / raw leak points / triage / tests（2026-05-20）
- [x] Privacy Wall v2：entity-level、event-level、numeric/proper-noun leakage audit + reconstructability scoring + deterministic sanitization/rewrite（2026-05-20）
- [x] Cumulative Strain Triage v1：`src/triage.py` 可讀 `data/dimension_scores`，支援 emotional safety Level 3、Level 2 persistence、三個 Level 1、worsening trajectory 等 deterministic rules（2026-05-20）
- [x] Demo / Pilot mode separation：`APP_MODE=dev|demo|pilot`，demo/pilot 隱藏 raw conversation、secret truth、scenario seed、raw JSON；UI 顯示 synthetic vs pilot data label（2026-05-20）
- [x] Safety regression tests：privacy leakage、triage guardrail、mode separation、Saga A regression；本機 `python -m pytest -q` 綠燈（2026-05-20）
- [x] v0.1 Safety Release Audit：`docs/v0_1_safety_audit.md` 記錄保護範圍、不能保護的範圍、false positive / false negative、pilot go/no-go（2026-05-20）
- [x] Privacy Wall v2 adversarial tests：indirect identity、family-event reconstruction、numeric detail、quote paraphrase、coordinator `do_not_share` leak（2026-05-20）
- [x] Crisis handoff stub：`docs/crisis_handoff_runbook.md` 定義 emotional safety Level 3 時 AI 必須停止做什麼、人類要 review 什麼（2026-05-20）
- [x] Source type enforcement v1：`src/source_types.py` + profile save normalization，未知來源降回 `synthetic`，UI label 使用同一套白名單（2026-05-20）
- [x] Dimension time-series snapshots v1：`src/dimension_store.py` 支援 latest + immutable snapshots，triage 可用 snapshots 判斷連續 Level 2（2026-05-20）
- [x] Crisis handoff packet v1：`src/crisis_handoff.py` 產生 privacy-sanitized handoff packet，不做自動通知或外部 action（2026-05-20）
- [x] Analysis Layer v0.1：`src/analysis_layer.py` 讀現有 Saga A artifacts，產生 normalized `student_case_summary`、evidence refs、contradiction flags、synthetic-only warnings（2026-05-20）
- [x] Case summary markdown generator：`scripts/generate_case_summaries.py` 輸出 `data/case_summaries/*.md`，報告隱藏 raw turns / scenario seeds / secret truths / high-specificity family events（2026-05-20）
- [x] Analysis Layer regression tests：case summary schema、evidence refs required、contradiction detection、synthetic-only warning（2026-05-20）
- [x] Signal Library v0.1：`src/signal_library.py` 定義 masking_language、disclosure_drop、strategic_compliance、autonomy_loss、parent_monitoring_increase 等 human-readable signals（2026-05-20）
- [x] Trajectory & Coordination Models v0.1：`src/trajectory_model.py` 用 rule-based detection 產生 burnout_risk、trust_erosion、disclosure_collapse、hidden_disengagement、parent_escalation、dependency_risk（2026-05-20）
- [x] Trajectory report generator：`scripts/generate_trajectory_reports.py` 輸出 `data/trajectory_reports/*.md`，以 possible risk patterns 呈現，不做 diagnosis / certainty prediction（2026-05-20）
- [x] Trajectory regression tests：signal detection、trajectory schema/evidence consistency、false positive protection、missing evidence confidence downgrade（2026-05-20）
- [x] Reviewer Workflow v0.1：`src/reviewer_workflow.py` 支援 case / trajectory 人工標記，verdict 包含 agree、disagree、needs_more_evidence、privacy_concern、true_positive、false_positive、under_evidenced（2026-05-21）
- [x] Reviewer summary generator：`scripts/generate_reviewer_summary.py` 輸出 `data/reviewer_summaries/reviewer_calibration_summary.md`，目前可顯示尚未 review 的狀態與後續入口（2026-05-21）
- [x] Reviewer workflow tests：schema validation、privacy sanitization、save/load、aggregation、empty summary regression（2026-05-21）
- [x] Reviewer Calibration Pass 1：Umi review Michael / Rachel / 沈又 代表案例，標記 supported、under-evidenced、privacy_review_needed 等 calibration status（2026-05-21）
- [x] Calibrated trajectory reports：trajectory report 現在區分 rule confidence 與 calibrated confidence，synthetic-only high 預設降到 medium，under-evidenced/privacy concern 降到 low（2026-05-21）
- [x] v0.5 Synthetic Calibration Release：`VERSION` = `0.5.0-synthetic-calibration`，並新增 `docs/v0_5_release_notes.md`（2026-05-21）
- [x] v0.6 Pilot Readiness Pack：audience-safe reports、reviewer assignment example、pilot onboarding checklist、source-type migration、dimension snapshot backfill（2026-05-21）
- [x] v0.7 Local Provider & Data Boundary docs：provider safety matrix、README / `.env.example` warnings、dev-only provider boundaries（2026-05-21）
- [x] v0.8 Controlled Internal Pilot Harness：`src/pilot_harness.py`、`src/audit_log.py`、`scripts/run_pilot_harness.py`、`data/pilot_runs/v0_8_smoke_michael/`、`docs/v0_8_release_notes.md`（2026-05-21）
- [x] v0.9 market thesis baseline：`docs/problem_validation.md` + `docs/market_positioning.md`，把 GIIS 改成 first proof point，把 family/B2C 改成 long-term market，把杰尼改成 optional support route（2026-05-21）
- [x] v0.9 pilot operations docs：`docs/v0_9_pilot_protocol.md`、`docs/onboarding_wording.md`、`docs/data_rights_and_deletion.md`、`docs/tabletop_exercises.md`（2026-05-21）
- [x] v0.9 reviewer assignment：Umi primary reviewer、Mahiru backup reviewer、Alan parent-facing owner；`config/reviewer_assignment.local.json` + `docs/reviewer_assignment.md`（2026-05-21）
- [x] v0.10 Three-Party Abstraction Layer：家長/老師也有 party profile、`what_not_to_share`、safe coordinator view；coordinator 改為三方 abstracted profile input（2026-05-21）
- [x] v0.11 Party-Aware Reporting：case summaries / audience reports 納入 parent/teacher needs、constraints、blind spots、safe offers，並新增成人 LLM abstraction + deterministic fallback（2026-05-21）

### 進行中 / 下一步
- [ ] **v0.9 final sanity pass**：確認 provider path、secure Level 3 notification mechanism、jurisdiction-specific emergency contact rule，然後才可邀請第一個家庭。
- [ ] **Three-party reviewer view**：在 Streamlit 中並排顯示 student / parent / teacher abstracted profiles，讓 Alan 看得出 coordinator 是怎麼合成判斷的。
- [ ] **Party-aware report variants**：case summary / audience reports 要納入家長與老師的 needs、constraints、blind spots，但仍維持跨方隱私邊界。
- [ ] **Privacy Wall v3：semantic adversarial audit**：目前 v2 是 deterministic heuristic；下一步可加 opt-in LLM reviewer 問「能否反推原始對話？」但不要預設打 API。
- [ ] **Reviewer Workflow v0.2 UI**：把 reviewer notes 接到 Streamlit，讓 Alan 不用手寫 JSON。
- [ ] **跑 LLM dataset eval**：設定 `RUN_LLM_TESTS=1` 後，用 `scripts/run_dataset_eval.py` 跑全資料，分開統計 `handcrafted_gold` vs `llm_generated`
- [ ] **跨家庭情報隔離**：abstraction layer 強制單一學生 scope（一個老師教多個學生時，coordinator 拉 profile 時要按學生隔離）
- [ ] **provider 切到 Ollama local**：pilot 前必須完成，因為不能讓真實學生對話進 Gemini free tier
- [ ] **Pilot 招募**：先找 1-2 個 GIIS 家庭做 micro dry run，不要直接跳到 5-10 個。這是大眾市場前的 trust-loop proof，不是最終市場大小。
- [ ] **Pilot run-book finalization**：包含 onboarding 流程、隱私說明、退出機制、緊急聯絡人 protocol。
- [ ] **Crisis escalation protocol v1 completion**：已有 runbook + packet skeleton + reviewer assignment；下一步要確認 secure Level 3 notification mechanism、jurisdiction-specific emergency contact rule、外部專業/緊急服務規則。**這個沒做完不能上線**。
- [ ] **Reviewer UI for party-aware reports**：把 `coordination_snapshot` 接到 Streamlit，讓 Alan/Umi/Mahiru 可以直接標記三方 alignment、mismatch、risk、safe bridge 是否合理。

### 阻擋 / 風險
- **Gemini / Groq / free cloud dev provider 不能放真資料**：在切到 Ollama / private approved provider 前，pilot 不能跑真實對話。
- **Synthetic conversation 不能等同真實驗證**：生成對話適合做 prompt pressure test，但不能證明真實學生、家長、老師會按同樣模式 disclosure。
- **Analysis Layer 不能變成診斷引擎**：case summary 只能整理 evidence 與 justified actions，不能做 clinical diagnosis 或 irreversible recommendations。
- **Trajectory 不能變成命運預測**：trajectory report 只能說 possible risk pattern；不能把 rule-based pattern 當確定走向。
- **Reviewer notes 不能貼 raw secrets**：human calibration 只應引用 evidence ref id 和抽象評語，不應把 raw conversation 或 secret truth 複製進 notes。
- **家長端的 buy-in**：家長一旦覺得「AI 在跟我兒子講悄悄話」就會抗拒。Pilot onboarding 必須親自做，不能丟 demo 影片。大眾版尤其不能賣成「看孩子秘密」。
- **B2C 市場的雙刃性**：一般人確實可能願意跟 AI 講秘密，但如果產品要把秘密轉給第三方，就必須有更嚴格的 consent、audience boundary、do-not-share policy。
- **緊急 case 的責任歸屬**：如果 Level 3 出現而 coordinator 推薦延遲，誰負法律責任？建議 pilot 階段所有 Level 3 都 100% 人工複核。
- **Alan 個人的時間**：所有 pilot family 的初始 onboarding 一定要 Alan 親自做，這是 founder dependency 風險。
- **家長/老師 LLM abstraction 依賴 provider 狀態**：v0.11 已支援成人 LLM abstraction，但本機 Ollama timeout 時會 fallback deterministic baseline；pilot 前要確認 selected local/private provider 的速度與穩定性。

### 2026-05-20 Engineering Notes
- 本機 smoke test：`python -m pytest -q` 預設不打 LLM API，應保持綠燈。
- LLM regression test：只有在明確設定 `RUN_LLM_TESTS=1` 時才跑，避免把 key 存在與否誤當測試意圖。
- Streamlit raw conversation view：本機 debug 可用 `SHOW_RAW_CONVERSATIONS=1 streamlit run app.py`；外部 demo / pilot 不應開。
- Privacy Wall v2 已完成 deterministic baseline，但不是語意安全證明；pilot 前仍需人工審查 + opt-in semantic eval。
- Cumulative Strain Triage v1 已接入 `data/dimension_scores`，但正式 pilot 需要 time-series store 與人工覆核流程。
- Analysis Layer v0.1 已可輸出 `data/case_summaries/*.md`，但它是 deterministic synthesis，不是 LLM reviewer，也不是真實臨床判斷。
- Trajectory v0.1 已可輸出 `data/trajectory_reports/*.md`；目前偏 recall-first，容易同時觸發多個 possible patterns，下一步需要 human calibration。
- Reviewer Workflow v0.1 已可產生 `data/reviewer_summaries/reviewer_calibration_summary.md`；目前尚無實際 review notes，下一步是人工標記 3 個代表案例。
- v0.5 已完成：目前版本是 `0.5.0-synthetic-calibration`。這代表 synthetic benchmark + human calibration 可用，不代表真實 pilot ready。
- v0.1 Safety Audit 結論更新：synthetic/local demo 可 go；真實 GIIS pilot 仍 no-go，直到 provider、crisis reviewer assignment、existing data migration、pilot runbook 完成。
- 目前測試：`45 passed, 7 skipped`。
- 下一個最小可交付版本：v0.6 Pilot Readiness Pack，包含 audience-safe reports、reviewer assignment、migration scripts、pilot onboarding + consent + emergency reviewer checklist。

### 2026-05-21 Engineering Notes
- v0.8 已完成：目前版本是 `0.8.0-internal-pilot-harness`。
- 新增 audience-safe reports：`data/audience_reports/internal_reviewer/`、`parent_safe/`、`teacher_safe/`。
- 新增 controlled pilot harness：`python scripts/run_pilot_harness.py --student michael --run-id v0_8_smoke_michael`，輸出在 `data/pilot_runs/v0_8_smoke_michael/`。
- Source type migration 已執行：既有 generated conversations / analysis reports 補上 `source_type` metadata。
- Dimension snapshot backfill 已執行：9 份 snapshot 寫入 `data/dimension_scores/snapshots/*/2026-05-21T04_38_06Z.json`。
- Privacy smoke scan：針對 `data/audience_reports/` 與 `data/pilot_runs/v0_8_smoke_michael/` 搜尋 raw seed / secret truth / do_not_share 代表詞，未發現直接命中。
- 目前測試：`52 passed, 7 skipped`。
- 下一個最小可交付版本：v0.9 GIIS Pilot Candidate + Market Thesis Release。這一版重點不是多寫功能，而是把 problem/customer thesis、1-2 家庭 protocol、human reviewer ownership、Level 3 tabletop exercise 做完。
- Market thesis 已更新：GIIS 是第一驗證場，不是唯一終點；大眾 B2C 可以成立，但必須以「private AI support / consent-based sharing」為核心，不能賣成監控或偷看秘密。
- 新增 `docs/problem_validation.md` 與 `docs/market_positioning.md`，作為 v0.9 後續 build 的產品邊界。
- v0.9 pilot operations docs 已新增：pilot protocol、onboarding wording、data rights/deletion、Level 2/3 tabletop exercises。
- Reviewer chain 已指定：Umi primary reviewer、Mahiru backup reviewer，皆以 education + psychology PhD 背景作為 v0.9 planning assumption；Alan 是 GIIS operator 與 parent-facing final outreach owner。Alan pilot time budget 先設 3 小時/週。
- v0.10 已完成 party-fair abstraction baseline：`src/abstraction.py` 新增 parent/teacher party profile schema，`src/coordinator.py` 改為接收三方 abstracted profiles，並把成人 `what_not_to_share` 納入 cross-party privacy wall。
- v0.10 UI 已收斂：active case selector 移到 `💬 三方 Live` 主工作區；sidebar 只顯示 status/model，避免左欄與主面板 selector 混淆。
- v0.11 已完成 party-aware reporting：`student_case_summary` 現在包含 `party_profiles` 與 `coordination_snapshot`，internal / parent_safe / teacher_safe reports 都會呈現三方可行動支持邊界。
- 目前限制：Streamlit reviewer UI 尚未直接呈現 `coordination_snapshot`；成人 LLM abstraction 在 Ollama timeout 時仍會走 deterministic fallback。

---

## Phase 2 — Student Success Layer + Support Routing

**目標**：把 GIIS 的 learning data + AI conversation signals 整合成 student success layer，讓 coordinator 能把學生 route 到正確支持：老師調整、家長溝通、學校 human review、外部資源、或杰尼 1-on-1。

**時間預估**：Phase 1 完成後 8-12 週

**成功指標**：
- 80%+ human reviewer 同意 coordinator 的 support routing decision
- 家長 / 老師收到的 safe guidance 被評為「可行動、不洩漏、不造成逼問」> 4/5
- 杰尼 老師在被合理 route 的 academic cases 中，接到的 briefing 被評分為「有用、不洩漏隱私」> 4/5
- GIIS retention / parent trust / student support response time 有可觀察改善
- 杰尼 LTV per routed student 可被追蹤，但不作為唯一成功指標

### 計畫項目
- [ ] **Support routing flow**：coordinator 對 reviewer 說明「這個 case 建議 teacher / parent / school / counselor / 杰尼 route，因為 X」
- [ ] **杰尼 onboarding flow**：只有對 academic support 合適 case，coordinator 才對學生/家長說「我們建議你 1-on-1，因為 X」
- [ ] **Tutor briefing doc 自動產生**：杰尼 tutor 接到新學生時自動拿到 abstracted profile（不含 verbatim），主要是七大維度的當前狀態 + 建議優先 focus area
- [ ] **杰尼 端的對話 AI**：杰尼 tutor 的 1-on-1 session 也可以用 AI 輔助記錄、輔助下次 session preparation（但 tutor 是主角，不是 AI）
- [ ] **Multi-student teacher dashboard**：Alan 端的「我這個禮拜要關心哪 5 個學生」清單，按 cumulative strain 排序
- [ ] **Provider 切到 DeepSeek**（如果 杰尼 端要在中國 domestic 部署）+ provider abstraction 完成
- [ ] **Routing outcome 追蹤**：GIIS student → coordinator routing → support action → outcome；杰尼 enrollment 是其中一種 outcome
- [ ] **跨 saga 隱私牆**：擴展到 coordinator 一次處理多個學生時，學生之間絕對隔離
- [ ] **Coordinator 七維度全開**：Phase 1 只跑 維度 1 + 3，Phase 2 跑全部
- [ ] **時間序列**：學生的維度評分要可以看歷史曲線（這個月 vs. 上個月），讓 Alan 可以早期介入

### 阻擋 / 風險
- **杰尼 老師對 AI handoff 的接受度**：1-on-1 tutor 是高度技藝化的工作，他們可能會排斥「AI 跟我講這個學生需要什麼」。需要 tutor 共創 brief 格式。
- **杰尼 客戶單價 vs. GIIS 客單價**：升級從 GIIS 到 杰尼 是付費升級，要設計 frictionless 的試聽 / 第一堂免費機制，否則漏斗會卡。
- **跨境合規**（如果 杰尼 端在中國）：PIPL 對未成年人數據處理更嚴。Provider 必須 China domestic。

---

## Phase 3 — 對外擴張：Schools + Families + Personal AI Support

**目標**：把這套系統變成可賣 / 可授權的產品。GIIS 是第一 proof point，但市場不只學校；長期也可以走家庭版、補教版、甚至個人 AI support 版。

**時間預估**：Phase 2 證明 GIIS + 杰尼 closed-loop 有效後，再過 12-18 週

**成功指標**：
- 2-3 個外部 pilot 學校 / 機構（不一定要付費，但要簽 LOI + 真實使用）
- 至少 1 個 B2B 授權合約簽出，或 1 個明確 B2C paid pilot cohort
- 家庭版 messaging 不被理解成「監控孩子」或「偷看秘密」
- demonstrably defensible：外部試用者不會輕易自己做一個，因為 trust boundary、privacy translation、support routing 都有實證與流程

### 計畫項目
- [ ] **Multi-tenant 架構**：每個機構獨立的 profile store、prompts 可客製、coordinator 維度可調權重
- [ ] **合規文件**：data residency、retention policy、未成年人 consent flow（FERPA-equivalent、PIPL、PDPA）
- [ ] **White-label 選項**：學校可以用自己的 branding
- [ ] **Pricing model**：B2B per-student / 按學校 size 階梯定價
- [ ] **Family / B2C model**：個人或家庭可購買 private AI support，但不自動分享秘密給第三方
- [ ] **Personal AI support model**：不限定學生，讓一般人整理自己不敢說出口的困難；若要分享給他人，必須用 explicit consent + sanitized summary
- [ ] **Onboarding playbook**：給其他學校的 setup-to-pilot guide
- [ ] **Defensibility moat**：把 GIIS 的 online-school support proof + privacy-preserving truth translation 經驗包裝成可複製方法
- [ ] **投資 / 戰略夥伴對話**：見 `docs/investor_angle.md`

### 戰略決策待定（從 CLAUDE.md C 點）
這個產品的範圍：
1. **純內部工具**（最深 moat、最小 TAM）
2. **內部先驗證再外推 SaaS**（推薦 — 平衡）
3. **內部先驗證再外推 family / personal AI support**（大眾市場更大，但 privacy / trust risk 更高）
4. **獨立第三實體 / portfolio company**（最大 upside、最分散 founder attention）

→ 建議在 Phase 1 結束時做決定，依 pilot 真實反應決定。

---

## Roadmap 維護規則

1. **每完成一個 [ ] 改成 [x]** + 加上完成日期
2. **新發現的 blocker** 立刻記到對應 Phase 的「阻擋 / 風險」段落
3. **scope creep / drop**：要 drop 的項目不刪除，劃線並寫原因（「2026-06 跳過，因為...」）
4. **Phase 跳階**：不要為了趕進度跳 Phase 1 的 emotional safety / privacy 工作 — 那是這個產品存在的全部理由
5. **Founder time audit**：每個月評估 Alan 自己花在這上面的時間是不是還合理。MVP 階段 founder 必須 hands-on，但 Phase 2 後 founder 應該 step back 到 strategy 層面
