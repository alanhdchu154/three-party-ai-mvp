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
| 3 | 重跑 `case_summaries` + `audience_reports`（**現在過時，依賴 #1#2 已完成的新 profile/dimension**） | **Codex**（熟那兩個 script 的 flag） | ⏳ 待做（可開始） |
| 4 | 全部重跑後跑 `audit_conversation_quality.py` + `pytest` 收尾 | Codex 或 Claude | ⏳ 待做（等 #3） |
| 5 | 清理 `data/synthetic_dataset.v1.json` + `__pycache__`/`.pytest_cache`（沙盒無刪除權限）| **Alan**（Mac 上 rm） | ⏳ 待做 |
| 6 | Revoke 外洩的 keys：Gemini / Groq / GitHub PAT（都出現在對話 log）| **Alan** | ⏳ 待做 |
| 7 | Review `docs/generation_logic.md` §5 §6（隱私 + 自動化風險）| **Umi** | ⏳ 待做 |
| 8 | 長期：corpus 仍 deep-heavy（~75%），讓 hourly task 慢慢拉向 40/35/25，定期看 audit | 自動 + 定期人工 | 🔄 進行中 |

> 完成一項就把狀態改成 ✅ 並在 Work Log 補一筆；不要直接刪掉，劃 ✅ 保留可追溯。

---

## § Work Log（append-only，新的放最上面）

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
