# Three-Party AI — Roadmap

**最後更新：2026-05-17**

這份是 living doc。每完成一件事就在這裡 mark complete，每出現新的 scope 改動就更新對應 phase。

---

## 北極星 (North Star)

**短期**：證明「三方各自跟 AI 講真話 + coordinator 翻譯」這個產品假設在 GIIS 真實用戶身上成立。

**中期**：把 GIIS → 杰尼 的 AI triage 漏斗跑通，讓 杰尼 1-on-1 業務有可預期、可量化的 inbound pipeline。

**長期**：把這套「閉環 AI 三方協調」變成一個其他學校 / 教育機構也可以採用的產品，但 GIIS+杰尼 永遠是 best-in-class 案例 / proof point。

---

## Phase 1 — MVP & GIIS 內部 Pilot

**目標**：跑得起來、跑得安全、跑得真。讓 5-10 個真實 GIIS 家庭使用，驗證核心假設。

**時間預估**：4-8 週（依招募 pilot 家庭速度）

**成功指標**：
- 80%+ 學生對話包含至少一個「AI is the only entity that can hear the truth」moment（內部評分）
- 0 verbatim 原話跨方洩漏（自動 audit）
- Triage 決策跟人類專家 agreement > 90%（小樣本人工標註）
- Pilot 家庭 NPS > 40
- 至少 2 個家庭從 pilot 升級成 杰尼 1-on-1 客戶（驗證漏斗）

### 已完成 ✅
- [x] 系統架構文件（three_party_ai_architecture.md）
- [x] 核心 modules 骨架：`src/student_agent.py` / `src/abstraction.py` / `src/coordinator.py` / `src/triage.py` / `src/profile_store.py` / `src/llm.py`
- [x] Streamlit UI 骨架（`app.py` 四個 tab）
- [x] 外部化 prompts (`prompts/*.txt`)
- [x] 隱私牆基礎檢查 `validate_no_raw_quotes()`
- [x] Synthetic dataset 重寫：聚焦 Michael Saga，9 個 personas、9 段對話（2026-05-17, 後縮回 Saga A only）
- [x] Coordinator 建議維度規格（`docs/coordinator_dimensions.md`）（2026-05-17）
- [x] `dummy_inputs.json` Saga A 對齊：Michael / Rachel / 沈又 三組家長+老師 demo case（2026-05-17）

### 進行中 / 下一步
- [ ] **實作 coordinator 七大維度評分**（從 docs/coordinator_dimensions.md 落地）
- [ ] **跑 dataset eval**：用 `scripts/run_dataset_eval.py` 跑全部 17 段對話、看 coordinator output 是否合乎 docs/coordinator_dimensions.md 的 worked examples
- [ ] **隱私牆強化**：除了 verbatim quote check，加入 entity-level check（人名、具體事件不能跨方流動）
- [ ] **Triage 升級自動化**：實作 docs/coordinator_dimensions.md 裡的兩條升級規則（杰尼 / 緊急）
- [ ] **跨家庭情報隔離**：abstraction layer 強制單一學生 scope（一個老師教多個學生時，coordinator 拉 profile 時要按學生隔離）
- [ ] **provider 切到 Ollama local**：pilot 前必須完成，因為不能讓真實學生對話進 Gemini free tier
- [ ] **Pilot 招募**：找 5-10 個 GIIS 家庭。建議從學生主動意願高的開始，避免家長端阻力過大造成 false negative。
- [ ] **Pilot run-book**：包含 onboarding 流程、隱私說明、退出機制、緊急聯絡人 protocol
- [ ] **Crisis escalation protocol**：Level 3 紅燈出現時 coordinator 怎麼通知學校輔導 + 家長 + 必要時 911 / 1995。**這個沒做完不能上線**。

### 阻擋 / 風險
- **Gemini free tier 不能放真資料**：在切到 Ollama / 杰尼-grade provider 前，pilot 不能跑真實對話。
- **家長端的 buy-in**：家長一旦覺得「AI 在跟我兒子講悄悄話」就會抗拒。Pilot onboarding 必須親自做，不能丟 demo 影片。
- **緊急 case 的責任歸屬**：如果 Level 3 出現而 coordinator 推薦延遲，誰負法律責任？建議 pilot 階段所有 Level 3 都 100% 人工複核。
- **Alan 個人的時間**：所有 pilot family 的初始 onboarding 一定要 Alan 親自做，這是 founder dependency 風險。

---

## Phase 2 — 杰尼 1-on-1 整合 + Triage 自動化

**目標**：把 GIIS → 杰尼 的漏斗從「我們覺得這個學生需要 1-on-1 就介紹」變成「coordinator 自動觸發、附帶 context handoff、學生家長同意機制」的可量化流程。

**時間預估**：Phase 1 完成後 8-12 週

**成功指標**：
- 20%+ GIIS pilot 學生被 coordinator 自動 triage 到 杰尼 1-on-1
- 杰尼 老師接到的 student handoff briefing 被評分為「有用、不洩漏隱私」> 4/5
- 杰尼 1-on-1 sessions 顯示可量化的學生狀況改善（vs. 自評基線）
- 杰尼 LTV per triaged student 可被追蹤

### 計畫項目
- [ ] **杰尼 onboarding flow**：coordinator 對學生說「我們建議你 1-on-1，因為 X」，學生 / 家長同意按鈕
- [ ] **Tutor briefing doc 自動產生**：杰尼 tutor 接到新學生時自動拿到 abstracted profile（不含 verbatim），主要是七大維度的當前狀態 + 建議優先 focus area
- [ ] **杰尼 端的對話 AI**：杰尼 tutor 的 1-on-1 session 也可以用 AI 輔助記錄、輔助下次 session preparation（但 tutor 是主角，不是 AI）
- [ ] **Multi-student teacher dashboard**：Alan 端的「我這個禮拜要關心哪 5 個學生」清單，按 cumulative strain 排序
- [ ] **Provider 切到 DeepSeek**（如果 杰尼 端要在中國 domestic 部署）+ provider abstraction 完成
- [ ] **Conversion 追蹤**：GIIS student → coordinator triage → 杰尼 enrollment → retention 全鏈路 metric
- [ ] **跨 saga 隱私牆**：擴展到 coordinator 一次處理多個學生時，學生之間絕對隔離
- [ ] **Coordinator 七維度全開**：Phase 1 只跑 維度 1 + 3，Phase 2 跑全部
- [ ] **時間序列**：學生的維度評分要可以看歷史曲線（這個月 vs. 上個月），讓 Alan 可以早期介入

### 阻擋 / 風險
- **杰尼 老師對 AI handoff 的接受度**：1-on-1 tutor 是高度技藝化的工作，他們可能會排斥「AI 跟我講這個學生需要什麼」。需要 tutor 共創 brief 格式。
- **杰尼 客戶單價 vs. GIIS 客單價**：升級從 GIIS 到 杰尼 是付費升級，要設計 frictionless 的試聽 / 第一堂免費機制，否則漏斗會卡。
- **跨境合規**（如果 杰尼 端在中國）：PIPL 對未成年人數據處理更嚴。Provider 必須 China domestic。

---

## Phase 3 — 對外擴張

**目標**：把這套系統變成可賣 / 可授權的產品。但保留 GIIS + 杰尼 作為 best-in-class 案例。

**時間預估**：Phase 2 證明 GIIS + 杰尼 closed-loop 有效後，再過 12-18 週

**成功指標**：
- 2-3 個外部 pilot 學校 / 機構（不一定要付費，但要簽 LOI + 真實使用）
- 至少 1 個 B2B 授權合約簽出
- demonstrably defensible：外部試用者不會輕易自己做一個（因為 GIIS + 杰尼 的閉環 dataset 是 moat）

### 計畫項目
- [ ] **Multi-tenant 架構**：每個機構獨立的 profile store、prompts 可客製、coordinator 維度可調權重
- [ ] **合規文件**：data residency、retention policy、未成年人 consent flow（FERPA-equivalent、PIPL、PDPA）
- [ ] **White-label 選項**：學校可以用自己的 branding
- [ ] **Pricing model**：B2B per-student / 按學校 size 階梯定價
- [ ] **Onboarding playbook**：給其他學校的 setup-to-pilot guide
- [ ] **Defensibility moat**：把 GIIS + 杰尼 的 closed-loop 經驗包裝成「我們是唯一一家學校 + 補教都自己跑過」這個 narrative
- [ ] **投資 / 戰略夥伴對話**：見 `docs/investor_angle.md`

### 戰略決策待定（從 CLAUDE.md C 點）
這個產品的範圍：
1. **純內部工具**（最深 moat、最小 TAM）
2. **內部先驗證再外推 SaaS**（推薦 — 平衡）
3. **獨立第三實體 / portfolio company**（最大 upside、最分散 founder attention）

→ 建議在 Phase 1 結束時做決定，依 pilot 真實反應決定。

---

## Roadmap 維護規則

1. **每完成一個 [ ] 改成 [x]** + 加上完成日期
2. **新發現的 blocker** 立刻記到對應 Phase 的「阻擋 / 風險」段落
3. **scope creep / drop**：要 drop 的項目不刪除，劃線並寫原因（「2026-06 跳過，因為...」）
4. **Phase 跳階**：不要為了趕進度跳 Phase 1 的 emotional safety / privacy 工作 — 那是這個產品存在的全部理由
5. **Founder time audit**：每個月評估 Alan 自己花在這上面的時間是不是還合理。MVP 階段 founder 必須 hands-on，但 Phase 2 後 founder 應該 step back 到 strategy 層面
