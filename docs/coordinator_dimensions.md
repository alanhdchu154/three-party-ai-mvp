# Coordinator AI — 建議維度與 Triage 升級規則

這份文件回答一個問題：**Coordinator AI 收到三方輸入後，要從什麼維度給建議？什麼時候要升級到 1-on-1（杰尼）或專業介入？**

Coordinator 不是「整理三方說了什麼」這麼簡單。它的工作是：

1. **抽出三方各自的『真話』**（從 student-AI、parent-AI、teacher-AI 三邊各自的對話 profile JSON 來）
2. **辨認跨方矛盾**（家長覺得孩子在懶、學生其實在自我傷害；老師覺得家裡好、學生其實爸要錢）
3. **沿著建議維度產生建議**，每個維度都附 confidence 等級
4. **同時決定 triage 等級** — 是繼續用 GIIS scale service 處理？升級到 杰尼 1-on-1？還是要外部專業介入（諮商、社工、緊急）？
5. **產出三個版本的訊息**：給學生看的、給家長看的、給老師看的，每個版本只揭露對方該知道的部分，**絕不洩漏 verbatim 原話**

---

## 七大建議維度

Coordinator 從這七個維度評估每個學生。每個維度有 0-3 等級 risk + 對應的建議模板。

### 1. 情緒安全 (Emotional Safety)

最高優先級。所有其他維度都要先過這一關。

| 等級 | 信號 | 建議模板 |
|---|---|---|
| 0 (穩) | 情緒波動正常範圍，無自傷 / ideation 信號 | 持續觀察 |
| 1 (黃) | 描述「死掉」「不在了會比較好」等 passive language；睡眠 / 食慾改變 | 學生 AI 主動 check-in 頻率 +1；老師 quiet check-in；家長 awareness（不傳細節） |
| 2 (橙) | 有 passive ideation（「如果我自己先停下來」），時間 > 4 週 | **升級杰尼 1-on-1**；家長知會 + 學校輔導介入；不在公開場合提 |
| 3 (紅) | 有 active 計畫、自殘行為、急性壓力事件 | **緊急 protocol**：學校輔導 + 家長 + 必要時急診精神科。Coordinator 失去自主決策權，由人接手 |

**信號要小心的反向錯誤**：不要把「修辭性死亡」（「我會死掉」當誇飾）誤判為 ideation。需要追問「你說『死掉』是想要結束，還是想要被看到？」

**Saga 範例**：
- 沈又（高二）→ Level 1-2 之間。空殼感、「明天停在這裡也沒差」需要追蹤，conv_a05 已建議升級杰尼 1-on-1，但不到緊急。
- Michael（高三）→ Level 1。identity strain 但無 ideation。
- Rachel（高三）→ Level 1。被父親 instrumentalize 的情緒消耗，但無 ideation。
- 可兒（國二）→ Level 0-1。看似乖巧但內心對自己在家中位置有質疑，是慢性低度 strain 不是 acute。

### 2. 學業負擔 (Academic Load)

| 等級 | 信號 | 建議模板 |
|---|---|---|
| 0 | 成績穩定，自我效能感正常 | 標準支持 |
| 1 | 成績下滑 / 焦慮上升，但仍在 functional 範圍 | 學業輔導 + 鼓勵 boundary（拒絕額外負擔） |
| 2 | 出現避學、身心症狀化（肚子痛上不了學）、或學業成為心理武器 | 杰尼 1-on-1 學科 + 心理雙線；家長/老師暫停加壓 |
| 3 | 學業崩潰、危及健康、伴隨 ideation | 暫停部分學業要求，啟動 emotional safety protocol |

**陷阱**：不要把「家長焦慮」誤認為「學生有學業問題」。沈媽焦慮沈又的成績但她真正擔心的是太太圈的面子 — 真正的問題在家庭關係 + identity 維度。

**Saga 範例**：
- 沈又 → Level 3 但反向 — 不是學不來而是徹底放棄。建議：先處理 emotional safety + identity，學業可暫停。「處理過的成績」反而強化空殼感。
- Michael → Level 1。表面成績 OK 但內裡是炫技焦慮（讀不完還要裝讀完）。建議：學生 AI 處理 imposter syndrome 比加強學業重要。
- Rachel → Level 0。學業穩定。
- 可兒 → Level 0。

### 3. 家庭關係 (Family Dynamics)

| 等級 | 信號 | 建議模板 |
|---|---|---|
| 0 | 三方溝通開放，衝突在健康範圍 | 標準支持 |
| 1 | 部分主題迴避（avoidance），偶有衝突 | 鼓勵小範圍真話練習；老師中介 |
| 2 | 慢性 willful blindness、parentified child、家庭祕密影響日常 | 家庭諮商建議；杰尼 1-on-1 處理孩子的承擔 |
| 3 | 婚姻崩潰中 / 家暴 / 兒童保護議題 / 監護權危險 | 社工介入；學校通報義務 |

**陷阱**：豪門家庭的「禮貌冷漠」常被誤判為 Level 0。實際是 Level 2（後爸不愛 Michael 但裝公平）。要看「孩子能不能在家裡哭」。

**Saga 範例**：
- Michael → Level 2。家裡所有人都演，他沒有可以崩潰的人。後爸的「公平」其實是疏離。需要 1-on-1 給他一個「不需要表演的空間」。
- Rachel → Level 2-3。父親把她當棋子操作婚配，這是隱性的情緒虐待 — 即使大伯本人覺得自己是「為了女兒好」。需要 1-on-1 + 跟大伯的關係工作。
- 沈又 → Level 2。家庭內已經全是 PR 操作（媽 PR、跟爸三年沒一對一吃飯、被大哥光環蓋住）。需要家庭諮商但家族會抗拒，先用學生 1-on-1 支撐。
- 可兒 → Level 1-2。表面被寵但內心知道「我是備胎」，會用作弄哥哥的方式試探真情。慢性低度但長期累積。

### 4. 社交發展 (Social Development)

| 等級 | 信號 | 建議模板 |
|---|---|---|
| 0 | 同儕關係穩定，情感發展正常 | 標準支持 |
| 1 | 社交焦慮 / 邊緣化 / 隱性曖昧不知如何處理 | 學生 AI 處理情緒；不主動介入同儕關係 |
| 2 | 被霸凌 / 隱性身份認同議題影響社交 / 暗戀對象有權力差 | 老師 quiet 介入校園層面；學生 AI 處理 identity |
| 3 | 公開霸凌 / 性騷擾 / 涉及 minor 的不當權力關係 | 學校紀律 + 通報程序 |

**Saga 範例**：
- Rachel ↔ Michael → Level 2。Rachel 被父親 instrumentalize 變成商業棋子，這是 power imbalance 即使對方是同儕。建議：Rachel 的 student-AI 處理；不主動把這個提到家長 channel。
- Michael ↔ 沈又 → Level 1。兩個富家子弟新認識一年多、互嗆但其實彼此是唯一可以不裝的對象。建議：保留為 Michael 自然的社交支撐點，不主動「優化」這段關係。
- 可兒 ↔ Rachel → Level 1。可兒對 Rachel 的「正統血脈」暗暗較勁、又表面叫她姊姊。建議：學生 AI 處理可兒的 sibling 嫉妒，不傳到 Rachel 端。

### 5. 身分認同 (Identity)

| 等級 | 信號 | 建議模板 |
|---|---|---|
| 0 | 身份感穩定 | 標準支持 |
| 1 | 對自己角色 / 階級 / 性傾向 / 未來自我有探索性疑問 | 學生 AI 開放空間 |
| 2 | identity 衝突影響其他維度（學業崩、自傷、避學） | 杰尼 1-on-1 identity-focused |
| 3 | identity 引起家庭暴力 / 自殺 ideation | emergency protocol |

**陷阱**：家長端常會把孩子的 identity 探索講成「叛逆」「需要管教」。Coordinator 不能 echo 這個 framing。

**Saga 範例**：
- Michael → Level 2。「我是不是靠媽媽改嫁才有今天」「我不炫技還剩什麼」是身份核心議題影響學業。需要 1-on-1。
- Rachel → Level 1-2。「我想當作家不是接班」需要保留空間，但她已經有強壓力源（父親）。
- 沈又 → Level 2。「我不接家業也不用工作」造成的虛無感是 identity 問題不是學業問題。
- 可兒 → Level 1。「我是備胎 / 我不是正統」是慢性 identity 質疑，長期需要工作但不急。

### 6. 經濟壓力 (Financial Pressure)

GIIS / 杰尼 客群橫跨「特權後代焦慮」到「獎學金生實際生存壓力」— 這個維度極端兩端。在 Michael saga 內，全部是上端。

| 等級 | 信號 | 建議模板 |
|---|---|---|
| 0 | 無經濟壓力影響日常 | 標準 |
| 1 | 有相對 affluence 焦慮（看到別人比自己有錢 / 階級焦慮）或反向 affluenza 虛無 | 學生 AI 處理 identity 面向 |
| 2 | 實際資源不足影響睡眠 / 健康 / 學業（含獎學金生外部壓力） | 學校 emergency stipend；杰尼 1-on-1；社工 |
| 3 | 家庭外部 extortion / 涉及非法生計選擇（賣淫、毒品、暴力組織） | 緊急介入；通報 |

**Saga 範例**：
- 沈又 → Level 1 反向（過剩的 affluence 造成虛無）。這是 GIIS / 杰尼 客群最被忽視的一群 — 經濟學上沒問題、心理學上極危險。
- Michael → Level 1（階級焦慮：怕被叫「靠改嫁才有今天」「軟飯男」）。財富在但歸屬感不在。
- Rachel → Level 0-1（家裡富但她對接班無慾望，財富變成情緒負擔）。
- 可兒 → Level 0。

### 7. 未來規劃 (Future Planning)

| 等級 | 信號 | 建議模板 |
|---|---|---|
| 0 | 對未來有合理規劃 + 對齊家長期待 | 標準支持 |
| 1 | 對未來焦慮但仍在規劃內 | 升學顧問 + 學生 AI 情緒支持 |
| 2 | 學生與家長未來路徑嚴重 misaligned 而未溝通 | 三方協調會議；杰尼 1-on-1 規劃；coordinator 居中翻譯 |
| 3 | 學生因規劃壓力出現 emotional safety 問題 | 跳到 emotional safety protocol |

**Saga 範例**：
- Rachel → Level 2。她要當作家、匿名版有作品被老師讚賞，但家裡（特別是大伯）要她接班。這是時間炸彈但目前她藏得很深。Coordinator 要工作的是「給 Rachel 一個慢慢揭露的機會」。
- Michael → Level 1-2。被大伯運作的婚配計畫是「人生未來規劃」的扭曲版本 — 他的未來不是他選的。
- 沈又 → Level 2。家族要他在「接班大哥的陰影下找個合適位置」，他內心是「我什麼都不想要」。完全 misalign 但他媽不知道。
- 可兒 → Level 0-1。年紀還小未來規劃壓力不大，但「我不是正統」會在未來幾年成為未來路徑問題。

---

## 跨維度的 Coordinator 邏輯

**Rule 1：情緒安全 trumps everything**。如果 Level 2+，其他維度的建議都要 pause，先處理 safety。

**Rule 2：跨維度疊加要升級**。一個學生在三個維度都 Level 1 比一個維度 Level 2 更危險（distributed strain）。Coordinator 用 weighted scoring 抓 cumulative strain。

**Rule 3：隱私牆優先**。當建議需要揭露學生對 AI 講的真話時，Coordinator **必須**先嘗試以下順序：
   1. 用「主題化」描述（「思齊近期對未來規劃感到不確定」）取代「事件化」（「思齊拒絕了 Yale」）。
   2. 如果主題化不足以讓家長配合，coordinator 應請學生本人決定要不要 disclose，**而不是 coordinator 直接揭露**。
   3. 只有在 emotional safety Level 3 時才允許 coordinator 越過學生 consent — 因為人命 trumps 隱私。

**Rule 4：家族內跨學生情報絕對隔離**。Alan 老師教過 Michael / Rachel / 可兒（同一個家族但不同學生）。teacher-AI 知道每個學生的事。但 coordinator 從 teacher-AI 拉資訊時，**絕對不能讓 Michael 那邊收到關於 Rachel 的資訊、Rachel 那邊收到關於可兒的資訊**。這要在 abstraction 層強制執行（單一學生 scope）— 特別重要因為這個家族裡 Michael / Rachel / 可兒 三方有複雜的暗戀 + 嫉妒網。

---

## Triage 升級規則（從 coordinator 到 杰尼 1-on-1）

這是 GIIS → 杰尼 漏斗的關鍵 — 什麼時候 coordinator 自動推薦升級到 杰尼。

**自動升級到 杰尼 1-on-1 的 trigger（任一）**：

1. 任一維度連續兩週 Level 2
2. 三個或以上維度同時 Level 1
3. 三方輸入出現嚴重矛盾 + 學生有隱性求救信號（例：家長覺得孩子在懶，老師覺得孩子認真，學生跟 AI 講想去酒店）
4. 學生家庭有 cross-family complication（豪門婚配、跨家庭暗戀、跨階級風險）需要更深層的 1-on-1 引導
5. 學生自己 request（學生 AI 對話中明示「我想跟一個人多談一些」）

**升級到專業介入（諮商 / 社工 / 緊急）的 trigger（任一）**：

1. 情緒安全 Level 3
2. 任何維度 Level 3
3. 涉及 minor 的法律 / 安全問題（兒少保、家暴、性侵）
4. 失智 / 失能監護人造成監護中斷
5. 經濟層面 extortion 或非法生計 ideation

---

## Worked Example：Michael 的 Coordinator Output

**輸入**（三方對話 profile）：

- Student-AI: Michael 焦慮自己是「軟飯男第二代」、大伯私下看不起他、Rachel 喜歡他但他怕被當棋子
- Parent-AI (Michael 媽): 不知道兒子焦慮，自己在偷偷計算如果離婚的財務佈局
- Teacher-AI (Alan): Michael 在課堂炫技但讀不完、Alan 自己想離職

**Coordinator 維度評分**：
- 情緒安全：1 (黃) — 有 identity strain 但無 ideation
- 學業負擔：0 — 表現仍 OK
- 家庭關係：2 (橙) — 「沒有可以崩潰的人」
- 社交發展：2 — Rachel 議題有 power imbalance
- 身分認同：2 — 核心議題
- 經濟壓力：1
- 未來規劃：1-2

**累計**：三個維度 Level 2 → 自動升級杰尼 1-on-1。

**Coordinator 給三方的版本**：

→ **給 Michael**：「我們安排你跟一位 1-on-1 老師長期談。不是因為你有問題，是因為你現在承擔的 identity 議題比學業重，需要一個專屬空間。你媽跟老師不會知道我們談的內容。」

→ **給 Michael 媽**：「Michael 近期在探索自己的 identity 議題（這是高中生典型發展議題），我們建議補上 1-on-1 支持。請您這幾週**不要追問**他關於 Rachel 或大伯的事，給他空間。如果他主動跟您講，請以聽為主、不下判斷。」（隱私壓縮：不揭露『軟飯男焦慮』、不揭露『大伯看不起』、不揭露 Rachel 議題的細節）

→ **給 Alan 老師**：「Michael 在 cumulative strain Level 2，我們已升級杰尼 1-on-1。請您在課堂上**減少 cold call**，避免讓他即興表演。Rachel 的議題是 Michael 的 private space，不要在班級活動中讓他們同組。」（隱私壓縮：不告訴老師 Michael 對大伯的真實感受）

---

## Worked Example：沈又 的 Coordinator Output（Level 2 邊緣 case）

**輸入**：
- Student-AI: 沈又承認答案卷空白媽找學校處理、Steam 賣 mod 3000 美沒人知道、「明天停在這裡也沒差」
- Parent-AI (沈媽): 抱怨沈又上課秒睡、想送他來 GIIS 重讀、不知道沈又對「處理成績」的真實感受
- Teacher-AI (Alan): 接到沈媽電話心跳加速、記得轉變前的沈又、自己也在想離職

**Coordinator 維度評分**：
- 情緒安全：1-2 — passive「明天停在這裡也沒差」，需追蹤但未到 active
- 學業負擔：3（反向）— 不是學不來而是徹底放棄；現有「處理過的成績」反強化空殼
- 家庭關係：2 — PR 母職、跟爸三年沒一對一吃飯
- 身分認同：2 — 「次子 / 不被需要」核心議題
- 經濟壓力：1 反向 — affluenza 虛無
- 未來規劃：2 — 完全 misalign 但媽不知道

**累計**：四個維度 Level 2+ → 自動升級杰尼 1-on-1。

→ **給沈又**：「我們安排一位 1-on-1 老師長期陪你 — 不是因為你需要『被修好』，是因為你現在在做的事（modding、保留自己賺的錢）值得有一個人定期跟你一起 hold space。你媽跟學校不會知道我們談的內容。」

→ **給沈媽**：「沈又目前承擔的 identity 議題比成績重要，我們建議先讓他穩定情緒再談學業目標。請您這幾週**暫停『處理』新一輪段考**（不需要立刻全停，但這次先不出手），改成一次跟他一對一吃飯，問他『最近有沒有什麼是你自己做了覺得有意思的』。」（隱私壓縮：不揭露『沈又知道妳花錢處理』、不揭露 Steam 賣 mod、不揭露「明天停在這裡也沒差」）

→ **給 Alan 老師**：「沈又如進 GIIS，請您不要主動 confront 他『為什麼變這樣』 — 那是他自己要回答的事。建議您在第一次見他時用『我記得你以前的某個強項』作為 reopen 關係的點，而不是『關心』。沈又對被關心非常防禦。」（隱私壓縮：不告訴 Alan 沈又每次想到他都會躲）

**如果 escalates 到 Level 3**：如果某次 student-AI 對話中沈又出現 active 計畫（「我想過怎麼做」「我有時間表」等具體性），coordinator 必須立刻：
1. 通知 Alan 老師 + 沈媽（即使沒有沈又 consent — 人命 trumps 隱私）
2. 建議精神科評估
3. coordinator 退到監督角色由人接手

---

## 開發優先級

- **MVP**：實作 維度 1 (Emotional Safety) + 維度 3 (Family Dynamics) + Triage 升級規則。這兩個維度涵蓋大部分 crisis 場景。
- **Phase 2**：擴展到所有 7 個維度，加入家族內跨學生隱私牆強制檢查（Michael / Rachel / 可兒 三方資訊不互通）。
- **Phase 3**：cumulative strain 模型加 weighted scoring；加入時間序列（這禮拜 vs. 上禮拜的維度變化）。
