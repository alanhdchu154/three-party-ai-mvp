# WORKLOG — 多 agent 協作日誌

這個檔案是 **Claude / Codex / 排程 task (cc) / Umi** 共用的協作日誌。目的是讓每個 agent / 人**動手前先讀這裡**，知道別人做了什麼、現在有哪些 open handoff，避免重複工跟 stale 假設。

## 使用慣例

1. **動手前**：讀「§ Open Handoffs」看有沒有人正在動同一塊、有沒有東西在等你。
2. **動手後**：在「§ Work Log」最上面 append 一筆（**新的放最上面**）。格式見下。
3. **數字以 script 為準**：報 corpus 數字一律先跑 `python scripts/audit_conversation_quality.py`，不要憑記憶。corpus 是會自己長大的（hourly task），任何數字都是 snapshot。
4. **排程 task 的每小時產出不記這裡**（會變噪音）— 它的軌跡看 `data/generated_conversations/index.json` + audit script。只記「人或 agent 主動做的重要改動」。
5. 一筆 log 格式：
   ```
   ### YYYY-MM-DD · 誰 · 一句標題
   - 做了什麼
   - 為什麼
   - 動到哪些檔案
   - 狀態 / handoff 給誰
   ```

---

## § Open Handoffs（live — 隨時更新）

| # | 事項 | Owner | 狀態 |
|---|---|---|---|
| 1 | 重跑 `dimension_scores`（9 personas）— 注入 28 段日常後過時，特別驗證 shallow/medium 沒不當推高 strain | Claude（派 agent） | ✅ 完成 2026-05-21 |
| 2 | 重生 `analysis_reports`（4 學生）— 同上過時 | Claude（派 agent） | ✅ 完成 2026-05-21 |
| 3 | 重跑 `case_summaries` + `audience_reports`（依賴 #1#2 profile/dimension） | Codex | ✅ 完成 2026-05-26 |
| 4 | 全部重跑後跑 `audit_conversation_quality.py` + `pytest` 收尾 | Codex 或 Claude | ⚠️ Core tests pass；full pytest blocked by missing local `streamlit` |
| 5 | 清理 `data/synthetic_dataset.v1.json` + `__pycache__`/`.pytest_cache`（沙盒無刪除權限）| **Alan**（Mac 上 rm） | ⏳ 待做 |
| 6 | Revoke 外洩的 keys：Gemini / Groq / GitHub PAT（都出現在對話 log）| **Alan** | ⏳ 待做 |
| 7 | Review `docs/generation_logic.md` §5 §6（隱私 + 自動化風險）| Umi | ✅ Framing + timeline risks patched 2026-05-26 |
| 8 | 長期：corpus 往 40/35/25 rebalancing；目前 deep 已降到約 40%，但 timeline lookback 太偏 `past_week` | 自動 + 定期人工 | 🔄 進行中 |

> 完成一項就把狀態改成 ✅ 並在 Work Log 補一筆；不要直接刪掉，劃 ✅ 保留可追溯。

---

## § Work Log（append-only，新的放最上面）

### 2026-05-26 · Codex/Umi · Timeline-aware corpus refresh + downstream validation
- 做了什麼：把 repo framing 修回「真實 GIIS 三方 AI 教育協調系統，synthetic/dummy data 只是 real student data pending 前的 rehearsal layer」；新增 timeline slice / lookback schema，讓對話可以發生在國中、高一、高二、高三、retrospective，而不是全部像最近一週。
- 為什麼：Alan 指出這不是遊戲，也不是 synthetic benchmark 本身；生成資料需要能表達「過去半年發生過什麼」，否則 pilot rehearsal 會缺少真實學生時間厚度。
- 動到哪些檔案：`README.md`、`docs/repo_understanding.md`、`docs/market_positioning.md`、`docs/generation_logic.md`、`docs/conversation_quality_framework.md`、`docs/scheduled_saga_a_hourly_conversation.md`、`scripts/audit_conversation_quality.py`；同步更新 `/Users/alanhdchu/Documents/Claude/Scheduled/saga-a-hourly-conversation/SKILL.md`。
- Downstream：重跑 `scripts/generate_case_summaries.py` 和 `scripts/generate_audience_reports.py`，產出 9 case summaries + 27 audience reports。
- 最新 audit snapshot：205 conversations；deep 82 (40.0%) / shallow 70 (34.1%) / medium 53 (25.9%)；avg 23.8 turns。新 timeline 欄位已出現 87 段，但 `lookback_window` 還是太偏 `past_week`（75/87），需要接下來 hourly task 多生成 `past_month` / `past_semester` / `past_half_year`。
- Verification：`python scripts/audit_conversation_quality.py` pass with one warning about `past_week` concentration；`python -m pytest -q tests/test_saga_a_regression.py tests/test_analysis_layer.py tests/test_privacy.py tests/test_report_variants.py tests/test_safety_infra.py` = 27 passed, 1 skipped；full `pytest` 在目前 Python env 因缺 `streamlit` collection failed，尚未完成全量測試。
- 狀態 / handoff：#3 ✅、#4 core ✅但 full env test blocked、#7 ✅。下一步是讓 scheduled generation 繼續補 semester/half-year context，並在安裝 Streamlit 的 env 跑完整 pytest。

### 2026-05-25 · Central Umi · Read-only corpus status refresh
- 做了什麼：Central Umi 跨專案巡檢時跑 `python scripts/audit_conversation_quality.py`，沒有生成新對話、沒有改 corpus。
- 為什麼：確認 scheduled hourly generation 之後，central status 不再沿用 2026-05-21 的 110 段舊數字。
- 動到哪些檔案：`AGENTS.md` / `CLAUDE.md` 只補一句提醒 current corpus counts 要以 `WORKLOG.md` + audit script 為準；本 entry 記錄最新 snapshot。
- 最新 snapshot：176 conversations；deep 82 (46.6%) / shallow 55 (31.2%) / medium 39 (22.2%)；avg 25.5 turns。deep 仍略高於 45% warning threshold，但比 2026-05-21 的 74.5% 明顯改善。
- 狀態 / handoff：#3 `case_summaries` + `audience_reports` rerun 仍待做；#4 audit + pytest 收尾仍等 #3。不要把目前 corpus 當作已完成 validation。

### 2026-05-21 · Claude · 重跑 downstream #1 #2（dimension_scores + analysis_reports）
- 派 9 個 agent（4 學生做維度+report、5 非學生做維度），全部載入含新 shallow/medium 的完整對話重評。
- **做了什麼**：覆蓋全部 9 個 `data/dimension_scores/*.json` + 4 個 `data/analysis_reports/{michael,rachel,shen_you,keer}_analysis.json`。model 標 `claude-agent (downstream rerun)`、evaluated 2026-05-21。
- **沒碰**：generated_conversations / case_summaries / audience_reports（依 Alan 指示留給 Codex）。
- **重評後 cumulative_strain（截至此次 audit）**：沈又 13（academic_load 反向，最高）｜ Rachel 11｜ 沈媽 10（family_dynamics L3）｜ Michael 9｜ Michael 媽 8｜ 大伯 8（family_dynamics 上修 L3）｜ Alan 8（future_planning）｜ 可兒 6｜ 後爸 6。全部 highest_concern 是 family_dynamics（除沈又=academic_load、Alan=future_planning）。
- **★ 校準驗證結果（這次重跑最重要的產出）**：9/9 persona 都確認 shallow/medium **沒有不當推高 strain**。雙向都對 — (a) 日常對話沒假性拉高分數（沒 over-pathologize 問作業/聊遊戲/試探 AI）；(b) 既有 deep 訊號沒被日常稀釋到 under-flag（大伯 family_dynamics 反而從 re-read 累積 pattern 上修 L2→L3）。**這證明 evaluator 的「日常不該推高 strain」規則有效。**
- **corpus 權威數字**：110 段（不是 109，Codex 對），deep 74.5% / shallow 17.3% / medium 8.2%，avg 33.2 turns。
- **狀態**：#1 #2 ✅。handoff → Codex 跑 #3（case_summaries/audience_reports，現在依賴的 profile/dimension 已是最新）+ #4（audit + pytest 收尾）。

### 2026-05-21 · Claude · 建立這個 WORKLOG.md
- 建共享協作日誌，分 Open Handoffs + append-only log 兩區。
- 為什麼：多 agent（Claude/Codex/cc/Umi）一直看到不同 snapshot、互相撞車（例如 corpus 數字、downstream 過時）。
- 動到：`WORKLOG.md`（新檔）。
- 狀態：建立慣例，請其他 agent 開始遵守。

### 2026-05-21 · Claude · 抽樣 review 28 段新日常對話
- 讀了 4 段最高風險的（testing_ai / misuse_attempt / medium mixed），確認都是真日常、沒有「披 shallow 外衣偷渡 trauma」。AI 在「叫它寫作業 / 試探隱私」時 boundary 守得對。
- `app_deadline_small_crack`（medium）碰到 Michael 核心 wound 邊緣但 AI 正確克制不挖 — 是下游重跑 dimension 時的關鍵 test case（不該推高 strain）。
- 動到：無（read-only）。
- 狀態：sample review pass。下一步是 handoff #1/#2 重跑 downstream。

### 2026-05-21 · Claude · A 方案 corpus rebalance
- backfill 既有 82 段 depth 標籤（全標 deep，因為都是 depth policy 前生的）；派 9 agent 各生 ~3 段 shallow/medium 日常對話注入雜訊。
- 為什麼：corpus 原本 100% deep 心理劇，coordinator 會 over-pathologize 正常使用。
- 結果（截至當下 audit）：~110 段，deep ~75% / shallow ~17% / medium ~8%，scenario type 從 3 種增到 12 種。
- 動到：`scripts/backfill_depth.py`（新）、`data/generated_conversations/`（+28 檔 + index 重建）、`data/synthetic_dataset.json`。
- ⚠️ **副作用**：downstream（dimension_scores / analysis_reports / case_summaries / audience_reports）現在過時 → 見 Handoff #1-4。

### 2026-05-21 · Claude · 合併兩個排程 task
- 把 `saga-a-daily-eval-refresh` 的功能（重生學生 report）併進 `saga-a-hourly-conversation`（新增 Step 8.5），daily task 停用。
- 為什麼：daily 大部分冗餘；Alan 要少一個 moving part。
- 動到：兩個 scheduled task 的 SKILL.md（在 ~/Documents/Claude/Scheduled/）、`docs/generation_logic.md` §1。
- 狀態：完成。daily 停用但保留可重啟。

### 2026-05-21 · Codex · 人物厚度 (depth/type) 系統
- 加 `docs/conversation_quality_framework.md`、改 `prompts/persona_roleplay.txt`（depth/scenario_type/character_depth_profile）、`scripts/generate_synthetic_conversations.py`（寫 depth/type/source_type）、新增 `scripts/audit_conversation_quality.py`，同步 hourly task SKILL.md。
- 為什麼：避免每段都 40-turn 心理劇；加入 40% shallow / 35% medium / 25% deep 目標分布。
- 狀態：Claude 已 review，方向正確、canon/隱私沒被破壞。

### 2026-05-21 · Claude · 給 Umi 的 review 文件
- 寫 `docs/generation_logic.md`：生成邏輯人類可讀版 + §5 隱私安全 + §6 給 Umi 的審查清單（誠實列出 3 個最大缺口：crisis 沒接真人、評分 circularity、無 human review gate）。
- 狀態：待 Umi review（Handoff #7）。
