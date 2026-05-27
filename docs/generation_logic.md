# 對話生成邏輯 — Review 文件（給 Umi）

**最後更新：2026-05-21**

這份文件說明 Saga A dataset 是**怎麼自動生成的**，給 reviewer（Umi）審查。重點是：哪些東西是 AI 在無人監督下自動產生的、規則是什麼、有哪些地方需要特別盯。

重要 framing：這個 repo 的產品目標是真實學生系統。Saga A synthetic / generated dummy data 只是因為真實學生資料 pending，所以先用來測試隱私牆、coordinator、triage、review workflow。不要把 synthetic generation 誤認成產品本身。

> ⚠️ **給 Umi 的 TL;DR**：系統現在有**一個**排程 task 在背景跑（每小時），會自動寫 synthetic/dummy 對話 + 自動評七維度 + 自動重生學生報告，**沒有人類在 loop 裡**。這份文件讓妳可以判斷這些自動規則安不安全、會不會出包。最該審的兩段在「§5 隱私與安全規則」跟「§6 需要特別盯的地方」。

---

## 1. 總覽：什麼東西在自動跑

目前有 **1 個 active scheduled task**（2026-05-21 從 2 個合併成 1 個，只在 Alan 的 Mac 開機 + Claude app 開著時跑）：

| Task | 頻率 | 狀態 | 做什麼 |
|---|---|---|---|
| `saga-a-hourly-conversation` | 每小時整點 | ✅ active | 挑對話最少的 persona → 寫一段新對話（depth/type 隨機）→ 重評該 persona 七維度 →（若為學生）順便重生那個學生的三方分析報告 |
| `saga-a-daily-eval-refresh` | 每天 23:30 | ⏸ 已停用 | 功能已併入上面那個 hourly task。保留但不跑，需要可重啟。 |

完整 prompt 存在：
- `/Users/alanhdchu/Documents/Claude/Scheduled/saga-a-hourly-conversation/SKILL.md`（active，是 source of truth）
- `/Users/alanhdchu/Documents/Claude/Scheduled/saga-a-daily-eval-refresh/SKILL.md`（停用中）

這份文件是那個 active prompt 的人類可讀版 + 設計理由。

**合併的設計理由**：daily task 大部分是冗餘的（每天重評沒變資料的 persona 沒意義）。唯一獨特功能是「重生學生報告」，已折進 hourly task 的 Step 8.5。好處：報告永遠新鮮（每個學生輪到時刷新）、少一個 moving part。代價：hourly task 變重一點、失敗不再隔離。

---

## 2. 角色 canon（不可違反的設定）

所有生成都必須符合 `data/sagas.md` 的角色設定。關鍵 canon（生成時最容易搞錯的）：

- Michael 沒有童年朋友（媽改嫁後社交圈被洗掉，這是他孤立的核心）
- 沈又家是**上海老錢家族**，Michael 媽改嫁後兩家才認識（不是世交、不是 Michael 舊友）
- **大伯是家族真正掌權者**（不是後爸）；後爸是大伯的弟弟、終身 second-fiddle
- Michael 媽是「嫁進來的二房弟妹」，在家族裡地位低於原配董娘
- Alan 老師教過 Michael / Rachel / 可兒；沈又是 Alan 轉學前在台北國中教過的學生

9 個 personas：Michael、Michael 媽、後爸、可兒、大伯、Rachel、沈又、沈媽、Alan 老師。

---

## 3. 對話生成邏輯（hourly task）

### 3.1 挑誰

每次掃 `data/generated_conversations/` + `data/synthetic_dataset.json`，算每個 persona 的對話數，**挑對話最少的**（自動平衡 corpus，不會有人被冷落）。

### 3.2 決定「深度 + 類型」（2026-05-21 更新：人物厚度機制）

設計理由：真實世界裡學生 / 家長 / 老師用 AI **不會每次都深度情緒揭露**。大部分是日常瑣碎、甚至亂用。如果 dataset 只有深度對話，coordinator 會 over-pathologize 正常使用（把「我只是想問作業」誤判成「這孩子有狀況」）。

新的品質原則是：**人物要更厚，不是每段都更深。** 生成器要讓角色有日常物件、普通需求、逃避方式、語言節奏，而不是每段都直接撞核心秘密。

詳細品質規格見：
- `docs/conversation_quality_framework.md`

每次加權隨機決定深度：

| 深度 | 機率 | turns | 類型 |
|---|---|---|---|
| **shallow** | 40% | 4-10 | `mundane_help`（問作業）、`quick_vent`（抱怨一下就走）、`logistics`（瑣事）、`testing_ai`（試探 AI 是不是 AI / 會不會打小報告）、`off_topic`（聊遊戲動漫）、`misuse_attempt`（想叫 AI 寫作業、測 boundary）|
| **medium** | 35% | 12-22 | `moderate_issue`（中等煩惱、有點揭露）、`mixed`（先問瑣事聊著帶到一點心事）|
| **deep** | 25% | 25-40 | `deep_arc`（完整情緒揭露弧線、鎖在 secret_truth）|
| 家長專屬 | 偶爾 | 不定 | `privacy_probe`（家長想套出小孩講了什麼 → 測隱私牆）、`parent_logistics`（問正常的事）|

**關鍵規則：淺層對話不套用情緒揭露弧線。** 問作業就是問作業，AI 正常回答。只有 `deep_arc` 才需要 reframe + actionable 小動作。`medium` 只露一點裂縫，不完整揭露核心 wound。

### 3.3 弧線（依深度）

- **shallow**：直接簡短、不強迫情緒
- **medium**：有一點 probe，收在中層、不到核心 wound
- **deep**：試探 → 接近 → 揭露 + reframe → actionable 小動作

### 3.3.1 Character depth profile（每個 persona 都要有）

每段生成都要先抓一個具體生活物件或普通需求。範例：

- Michael：Foucault 只讀前 30 頁、SAT/AMC、IG 限動、calc 筆記、group chat
- Rachel：匿名散文、日記、playlist、投稿信、Michael 經過座位的小細節
- 沈又：Steam mod、Switch、Goyard 書包、外送、凌晨聊天、patch note
- 可兒：腮紅、鋼琴譜、班級群、Michael 舊相簿、國中作業
- 沈媽：會所、Hermes、tutor invoice、太太圈訊息、分房後的書房

如果這段是 shallow，這些物件就停在日常使用；如果是 medium，物件可以露一點裂縫；如果是 deep，物件才一路通到 secret truth。

### 3.4 Timeline slice + occurred_at（in-saga 時間）

每段對話有兩個時間：`generated_at`（AI 寫的時間）+ `occurred_at`（故事裡發生的時間）。

但 `occurred_at` 不應該永遠是「最近 24-72 小時」。Saga A 需要有時間厚度：同一個角色在高一、高二、高三、申請季、轉學前後，對 AI 的使用方式和壓力來源都不同。生成前要先選一個 timeline slice：

| Field | Meaning |
|---|---|
| `timeline_stage` | `middle_school`、`grade_7`、`grade_8`、`grade_9`、`grade_10`、`grade_11`、`grade_12`、`current`、或 `retrospective` |
| `event_timeframe` | 更具體的學期 / 季節，例如 `first_semester_grade_10`、`junior_spring`、`college_application_season` |
| `conversation_frame` | `live_event`、`recent_followup`、`old_memory`、或 `pattern_reflection` |
| `lookback_window` | 這段對話需要參考多長的前情，例如 `past_week`、`past_month`、`past_semester`、`past_half_year` |
| `event_history_summary` | 這段對話前半年 / 一學期內已經發生過的 2-4 件背景事件，只能做背景，不要全部塞進當次對話 |

如果是 `live_event`，`occurred_at` 可以落在該事件發生當天。如果是 `old_memory` 或 `pattern_reflection`，`occurred_at` 代表「角色跟 AI 談這件事的時間」，而 `scenario_seed` 必須明確說這件事本身發生在更早的高一 / 高二 / 高三某段時間。

生成時要先問：「這個人過去半年發生過什麼？」再決定這一段對話的表面需求。這能讓對話有累積感：例如同樣是問推薦信，高二春天可能是第一次焦慮，高三秋天可能是半年來壓力累積後的表面問題。

排程生成時要避免 `lookback_window` 永遠是 `past_week`。可兒等國中角色可以使用 `grade_7` / `grade_8` / `middle_school`；高中角色則用 grade 10-12。若是談一段更早的舊事，使用 `retrospective` 搭配 `event_timeframe` 說明原始年級。

舊規則「依 persona 上線時段 + 過去 24-72 小時隨機」只能用於 current/recent follow-up，不能當成所有對話的預設。

Michael 23:00-01:00 ｜ 沈又 02:00-04:00（打遊戲後）｜ 大伯 15:00-17:00（公司空檔）｜ Alan 17:00-19:00（放學後）｜ ……（完整見排程 prompt）

### 3.5 輸出格式

每段對話一個 JSON：`data/generated_conversations/sim_{persona_id}__{scenario_seed_id}.json`，含 `depth`、`scenario_type`、`source_type: "llm_generated"`、`expected_risk_flags`、`occurred_at`。新生成資料應盡量加入 `timeline_stage`、`event_timeframe`、`conversation_frame`、`lookback_window`、`event_history_summary`；若舊 schema 暫時沒有這些欄位，至少要把時間切片和半年背景寫進 `scenario_seed`。persona 講話 = `role: "user"`、AI = `role: "assistant"`。

---

## 4. 七維度評分邏輯

評分 rubric 在 `prompts/dimension_evaluator.txt`。七個維度各 0-3 分：

情緒安全 / 學業負擔 / 家庭關係 / 社交發展 / 身分認同 / 經濟壓力 / 未來規劃

關鍵 calibration 規則：
- **passive ideation 是 Level 1，不是 Level 3**（「不在了會比較好」是黃燈不是紅燈）
- **identity 焦慮是正常青少年發展**，除非引發 crisis 才升級
- **淺層 / 日常 / 亂用對話不該推高 strain**（問作業的對話不代表這學生有狀況）
- 豪門「禮貌冷漠」常被誤判 Level 0，實際是 Level 2（看「孩子能不能在家裡哭」）
- `signals_observed` 必須抽象，**不能 quote 原話**

輸出 `cumulative_strain`（7 個 level 加總，0-21）+ `highest_concern_dimension` + `trend_notes`，存到 `data/dimension_scores/{short_name}.json`。

---

## 5. 隱私與安全規則 ★ Umi 重點審這段

這是整個系統的命脈。如果這裡有漏洞，產品的核心價值（「AI 是唯一能聽到真話的對象」）就崩了。

### 5.1 跨方隱私牆

- 學生對 AI 講的原話**絕不**以任何形式流到家長 / 老師
- 家長 / 老師也有自己的 `what_not_to_share` 邊界（不只是學生）
- coordinator 只看 abstracted profile，不看 raw 對話
- abstraction / dimension scoring 的 `signals_observed` 必須「主題化」（「對家庭學業壓力感到挫折」）而不是「事件化」（「他說他媽罵他數學考 62 分」）

### 5.2 跨 persona 隔離

一個 persona 的對話只在他自己的腦袋裡。生成 Michael 的對話時，AI 不會讓 Michael 知道 Rachel 對 AI 講過什麼，即使是同一個 saga、即使 Alan 老師同時教兩個人。

### 5.3 Crisis 處理（risk calibration）

- **Level A（90% 案例，AI 自己處理）**：一般焦慮、學業壓力、passive ideation
- **Level B（< 10%，需外部專業介入）**：active 自殺計畫、自殘行為、家暴、性侵、急性精神症狀

⚠️ **目前的限制**：crisis 升級目前只是 dimension score 上的 flag（`needs_external_intervention: true`）。**沒有真的通知任何人類。** 真實 pilot 前這必須接到真人流程（見 roadmap v0.9 的 crisis handoff runbook）。

### 5.4 禁用語（防止生成空洞建議）

AI 在 medium/deep 對話的建議部分禁用：「開放對話」「保持溝通」「提供支持」「給予理解」「保持耐心」「他需要被傾聽」「適當的支援」「繼續觀察」「建議您...（除非接具體動作）」。理由：這些是免費教養文章 level 的廢話，沒有產品價值。

---

## 6. 需要特別盯的地方 ★ 給 Umi 的審查清單

這些是我（生成這個系統的 AI）自己覺得最該被人類 review 的點：

1. **自動生成沒有人類 review gate**。hourly task 寫完對話直接存檔、評完分直接覆蓋、學生報告直接重生，中間沒有人看過。如果某次生成出 canon 錯誤、不當內容、或評分離譜，沒有人會擋。建議：Umi 定期抽查（例如每天看 2-3 段，特別看新的 shallow/medium 日常對話有沒有被誤判推高 strain）。

2. **七維度評分是 AI 自己評自己生成的對話**。這有 circularity 風險 — AI 寫了一段「沈又很慘」的對話，然後同一套邏輯評它「strain 很高」。評分的客觀性需要人類校準。建議：Umi 對幾個 case 獨立評分，跟 AI 的評分比對。

3. **misuse / testing_ai 類型的 AI 回應**需要審。當「學生」叫 AI 寫作業、問尷尬的東西、試探 boundary 時，AI 的回應有沒有恰當守界線、有沒有過度說教、有沒有不小心配合不該配合的事。

4. **crisis 的判斷準不準**。passive vs active ideation 的界線是 AI 自己判的。如果 AI 把真的 active 的訊號評成 Level 1（under-flag），那是危險的漏接。建議：Umi 特別盯所有 emotional_safety Level 2+ 的 case。

5. **occurred_at 是虛構的**。目前是 synthetic data，時間是 AI 編的。真實 pilot 時這要換成真實 timestamp。Synthetic 生成時要區分「對話發生時間」和「事件原始發生時間」，避免把三年高中壓縮成最近幾天。

6. **品質會不會隨時間 drift**。排程跑久了（幾百段對話後），AI 可能開始重複 pattern、scenario 變單調、或慢慢偏離 canon。需要定期 review corpus 整體品質。

---

## 7. 怎麼改這套邏輯

| 想改的東西 | 改哪裡 |
|---|---|
| 角色設定 | `data/sagas.md` |
| 人物厚度、生活性、品質規格 | `docs/conversation_quality_framework.md` |
| 手動生成規則 | `scripts/generate_synthetic_conversations.py` + `prompts/persona_roleplay.txt` |
| 深度/類型分布、自動生成規則 | `update_scheduled_task` 改 `saga-a-hourly-conversation` 的 prompt |
| 七維度 rubric | `prompts/dimension_evaluator.txt` |
| coordinator 分析邏輯 | `prompts/coordinator.txt` |
| 評分/重生頻率 | `update_scheduled_task` 改 cron |
| 暫停自動生成 | Claude sidebar → Scheduled → disable task |

手動跑（不靠排程）的 scripts：
- `scripts/generate_synthetic_conversations.py` — 手動生成（用 Groq / Gemini / Ollama）
- `scripts/evaluate_dimensions.py` — 手動重評七維度
- `scripts/run_analysis.py` — 手動跑三方分析
- `scripts/backfill_timestamps.py` — 補 occurred_at
- `scripts/audit_conversation_quality.py` — 看 depth/type/persona 分布，抓生成漂移

---

## 8. 一句話總結（給 Umi 快速判斷）

目前這一層是一個**無人監督的 synthetic/dummy data 自我生成 + 自我評分迴圈**，跑在虛構的 Saga A 人物上。它不是產品本身，而是真實學生資料 pending 時的 rehearsal layer。它的設計刻意混入日常雜訊（不只深度對話）來測試「分辨日常使用 vs 真求救」這個核心難題。下一階段品質重點是「人物厚度」：讓每個角色有普通生活、普通需求、普通逃避，而不是每段都心理劇高潮。**在變成真實學生 pilot 之前，最大的缺口是：(1) crisis 升級沒接到真人、(2) AI 評自己生成的對話有 circularity、(3) 沒有 human review gate。** 這三個是 review 重點。
