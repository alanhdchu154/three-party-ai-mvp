# 投資人視角 — 這個產品會吸引到誰，為什麼

這份文件是給 Alan 在自我評估時用的，不是 pitch deck。目的是 (1) 釐清誰會給錢、(2) 釐清為什麼是現在、(3) 釐清這個產品該被估值在哪個量級。

直接講：這個產品比 founder 自己以為的還要大。但要 think big 必須先承認它的 moat 真的在哪裡，再思考如何放大。

---

## 一句話定位

**Three-Party AI 不是 EdTech 公司，是「成年人之前的人類關係 OS」。**

它解決的問題不是「學生學不會」，是「青少年身邊的成年人聽不到真話、青少年自己也不知道怎麼說」。教育只是它最早能落地的場域。

把這個定位想清楚之後，TAM 就從「EdTech 學習工具市場」跳到「青少年情緒基礎建設市場」，後者跟 BetterHelp、Headspace 同個量級。

---

## 為什麼是現在 (Why Now)

三個趨勢同時發生：

1. **後疫情青少年心理危機**：US CDC 2023, 中國衛健委 2024 都顯示 13-18 歲焦慮 / 憂鬱率十年內翻倍。學校 counselor 對學生比 1:400-1:800。傳統 1-on-1 諮商 supply 完全不夠。
2. **LLM 進入「能做細膩中文情緒對話」的臨界點**：2024 之前的 LLM 不足以扮演夠細膩的青少年對話夥伴（特別是中文文化脈絡 — 孝順、丟臉、家族壓力）。2025-2026 的 Claude / Gemini / DeepSeek 級別模型才剛剛能做到。
3. **華人家庭的「不溝通」結構是文化常數**：孝順文化、丟臉文化、移民翻身焦慮 — 這些不會在 5 年內被治癒。AI 是少數能合法繞過這些自我審查的介面。

時間視窗：3-5 年。再過 5 年，所有大廠都會做類似 feature，這時候要靠 closed-loop data 跟品牌站住。

---

## 五層 Moat（按 defensibility 排序）

### 1. Closed-loop dataset（最強）

Alan 同時擁有 GIIS（學校端）+ 杰尼（1-on-1 端）。這代表這個系統可以：
- 從學生入學就開始累積七維度時間序列
- 從 coordinator triage 推薦到 杰尼，知道 1-on-1 後續成效
- 把成效回饋 train coordinator 的下次推薦

這是其他競爭者複製不了的，因為：
- 純 SaaS 賣給學校：拿不到 1-on-1 後續成效（不是同一個 vendor）
- 純線上補教：拿不到入學前 6 個月的 baseline
- 大廠（騰訊 / 百度 / 字節）：政策風險 + 父母對大廠收集子女資料的恐懼

### 2. 文化授權（Cultural Authority）

這個產品需要「會講孝順、丟臉、家族壓力」的 AI。Western EdTech AI（Khan, Duolingo, Quizlet）用美式心理話術會直接 trigger 華人家長的「太美式」「不適合我家小孩」反應。Alan 自己是 GIIS owner、教過第一線學生、用中文思考 — 他在 prompt engineering / dataset curation 上有不可外包的優勢。

### 3. Founder Vertical Integration

學校 owner + 補教 CEO + AI builder 同一個人。這個組合：
- 沒有「賣給學校」的銷售週期
- 可以 6-8 週 pilot 而不是 18 個月
- 可以承擔 AI 風險（最壞 case 是「我自己的學校先測試」）

外部競爭者想要複製，要嘛先買學校（極貴），要嘛先說服學校（極慢）。這個 advantage 至少 24 個月。

### 4. 隱私架構

「AI 跟學生講的話絕不流到家長」這個 design constraint，**大部分學校 IT 採購流程其實偏好相反**（學校希望可以監督學生）。Alan 的產品願意對家長 / 學校 say no，這個 brand stance 是建立家長信任的長期資產。一旦建立，家長口碑會自我擴散。

### 5. 跨方協調的演算法 IP

七維度 coordinator + cumulative strain scoring + cross-saga privacy wall，這些是 patentable / publishable 的演算法層。短期不是最強 moat（其他 LLM-native 公司能在 6-12 個月複製演算法），但時間久了會結晶成標準。

---

## 誰會買單

### Tier 1 — 高機率投資、cheque size $1-5M（種子 / Pre-A）

| 投資人類型 | 為什麼會看 | 風險 / 顧慮 |
|---|---|---|
| **EdTech VC（亞洲）**：GGV、Sequoia China、Hillhouse、Trustbridge | GIIS + 杰尼 雙引擎 + closed loop 是教育投資人罕見的乾淨故事 | 中國雙減後對教育更謹慎；要看是 cross-border 還是純中國 |
| **EdTech VC（美國）**：Owl Ventures, Reach Capital, GSV Ventures, Learn Capital | Asia-focused EdTech 罕見有英文 communication + 完整閉環的標的 | 不熟華人家庭文化、不敢押 founder 一個人 |
| **Mental Health VC**：Two Sigma Ventures (mental health portfolio), Boundless Capital | 「青少年情緒基礎建設」這個 framing 是他們的 thesis | 教育 vertical 不熟、不知道怎麼 underwrite 學校 ownership 風險 |
| **二代 family office**：亞洲多家 2nd-gen office | Michael Saga 描述的就是他們自己。產品同理心極強 | 投資紀律比 VC 弱、要看 founder 是否能 navigate family politics |

**最該開啟對話的 5 個名字**（基於 thesis fit）：
1. Owl Ventures（教育 AI、亞洲覆蓋）
2. GGV（消費 + 教育、亞洲 + US）
3. Reach Capital（青少年福祉 thesis）
4. Sequoia Capital China（教育 + AI、有 ByteDance 經驗）
5. Hillhouse（深度教育投資、跨境）

### Tier 2 — 中機率投資、$3-15M（Series A）

| 投資人類型 | 為什麼會看 |
|---|---|
| **AI infra / agent 投資人**：Index, Greylock, Sequoia US | 三方協調的 coordinator 架構是個有意思的 agent pattern。教育只是 wedge |
| **Cross-border 教育基金**：Asia-US bridge funds | 華人 diaspora 是未被充分服務的市場 |
| **保險 / 健康集團 CVC**：諾華、保險公司風險基金 | 青少年心理健康預防勝於治療 ROI |

### Tier 3 — 戰略夥伴 / 潛在收購方

| 對象 | 為什麼會收 | 時機 |
|---|---|---|
| **新東方 / 好未來 國際部** | 雙減後轉做華人 diaspora 國際升學，需要差異化產品 | Phase 2 證明漏斗後 |
| **Pearson / 培生** | 全球教育巨頭，缺青少年心理 / 升學焦慮 angle | Phase 3 對外擴張時 |
| **Khan Academy / Course Hero / Chegg** | 想擴張到非學科內容領域 | 中期 |
| **Anthropic / OpenAI 教育部門** | 想要垂直 vertical agent 案例 | 早期戰略合作多過收購 |
| **杰尼 自己** | Alan 自己把這個 spin out 後再買回去整合 | 取決於戰略決策（見下方） |

---

## TAM / SAM / SOM

### 保守版（Realistic 5-Year）

- **GIIS 直接 B2C**：500-2000 學生 × $1,500/yr = **$0.75-3M ARR**
- **杰尼 triage-driven**：200-500 學生 × $5,000/yr = **$1-2.5M ARR**
- **B2B 授權 2-5 校**：× $50k/yr = **$0.1-0.25M ARR**

**5 年保守 SOM：$5-10M ARR**

這個 size 對 VC 偏小。但對家族 office、戰略基金、Alan 自己控股很 OK。

### 中型版（Believable Stretch 5-Year）

把 GIIS 擴展到「全球華人線上高中」(diaspora + 港澳台 + 跨境)、杰尼 擴展到全亞洲線上 1-on-1：

- **GIIS 擴版**：5,000 學生 × $2,000 = **$10M ARR**
- **杰尼 擴版**：2,000 學生 × $7,000 = **$14M ARR**
- **B2B 授權 10-20 校**：× $80k = **$0.8-1.6M ARR**
- **白標 / 補教夥伴**：5-10 機構 × $150k = **$0.75-1.5M ARR**

**5 年中型 SOM：$25-30M ARR**

這個量級足以拿 Series B / 走獨立 SaaS 路徑、估值 $150-250M。

### 大型版（Think Big — 改變 framing）

**不是教育公司，是青少年情緒基礎建設**。產品延伸：

- **核心**：三方 AI coordination（原 GIIS+杰尼）
- **延伸 1**：成年人協調（夫妻 + 個別諮商師、職場員工 + 主管 + HR）
- **延伸 2**：高齡父母 + 成年子女 + 醫療照護的三方協調
- **延伸 3**：B2B SaaS sold to schools, therapy networks, EAP providers

**TAM**：BetterHelp $4B revenue 2024，Headspace $300M。如果這個產品打到「家庭情緒 OS」這個 framing，TAM = **$15-50B**，SOM 5 年可能 **$50-200M ARR**。

這是「估值 $1-3B」級別的故事。但需要：
1. Phase 1-2 證明核心
2. 把產品架構從「教育」抽離成「三方協調 platform」
3. Founder 願意 step beyond 自己的學校 / 補教身份

---

## 戰略決策的三條路（從 CLAUDE.md C 點延伸）

### 路徑 A：純內部工具
- **scope**：只服務 GIIS + 杰尼
- **moat**：最深、最 defensible
- **TAM**：$5-10M（極限）
- **資金**：不需要外部
- **誰會喜歡**：家族 office、自己控股
- **缺點**：產品 underperforms 市場價值

### 路徑 B：內部先驗證再外推 SaaS（推薦）
- **scope**：Phase 1-2 內部、Phase 3 對外
- **moat**：仍強（closed-loop + 文化授權）
- **TAM**：$25-50M ARR 5 年內
- **資金**：種子 $1-3M + Series A $5-15M
- **誰會喜歡**：Owl / GGV / Reach 級
- **缺點**：scope 受限於華人市場

### 路徑 C：獨立 portfolio company，think big
- **scope**：把產品從「教育」抽離成「家庭 / 關係協調 platform」
- **moat**：強但需要 founder 重新 reposition narrative
- **TAM**：$200M+ ARR potential
- **資金**：種子 $3-5M + Series A $15-25M + B $50M+
- **誰會喜歡**：a16z, Sequoia US, Index, mental health VC
- **缺點**：Founder 必須 step back from 學校 / 補教日常，risk 是 GIIS / 杰尼 失去 hands-on owner

---

## 直接給 Alan 的判斷建議

1. **不要太早做戰略決策**。Phase 1 pilot 跑完再說。pilot 跑出來的數據會自動 dictate 哪條路徑可行。
2. **如果你想 think big，先把 narrative 從『EdTech』改成『家庭關係 OS』**。這不只是包裝，是真的會影響你後面的招募、定價、發展方向。
3. **二代 family office 是最便宜的第一筆錢**。他們不會 push 你跑得太快，也最懂這個產品的同理心。建議從這裡開始 raise，再評估要不要做 institutional round。
4. **不要太早接 institutional VC**。一旦接了，他們會 push 你做 SaaS scale，但你 Phase 1 還沒驗證閉環。你會被逼著做你還沒準備好的事。
5. **保留 杰尼 + GIIS 的雙頭控股**作為談判籌碼。任何投資人都會想把 三方 AI 跟 杰尼 解綁，但解綁 = 你失去 closed-loop moat。要 hold the line。
6. **think big 但不要 think alone**。找一個能跟你 think big 的 co-founder / advisor。產品 vision 你有，但策略 / 募資 / hire 不是一個人可以做完的。

---

## 你問「會吸引到誰」的精準答案

**最快會出價的人**：亞洲二代 family office、Owl Ventures、GGV、Reach Capital。

**最該被吸引的人但需要被教育**：Mental health VC（Two Sigma, Boundless）— 因為他們會給最高估值如果 framing 對。

**潛在收購方**：新東方國際、好未來國際、Pearson、Khan Academy。

**會 pass 的人**：純美國 K-12 EdTech VC（Learn Capital 等） — 他們對華人市場不熟、對中國政策風險過敏。

**最危險的「假興趣」**：純 LLM infra 公司想 partner 做 vertical case study — 他們會佔用你時間但不會給錢，最後拿你的故事去 raise 自己的 round。

---

## 接下來的具體動作

如果你今天就要動，順序：

1. 把 docs/sagas.md + docs/coordinator_dimensions.md + docs/roadmap.md 整理成一份 **2-page memo**（不是 pitch deck）
2. 跟 3 個你認識的二代 family office 喝咖啡，testing the framing — 看他們聽完是「想保護自己小孩」還是「想投資」
3. 如果二代 office 反應強烈 → 順勢開始 institutional 對話
4. 如果二代 office 只想「我家小孩用」 → 證明你應該先收 B2C 訂閱、不急著 raise

不要先做 deck。Memo 比 deck 真實，VC 看完 memo 才知道你會不會 BS。
