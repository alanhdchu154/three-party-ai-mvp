---
name: saga-a-hourly-conversation
description: 每小時為 Saga A 對話最少的 persona 寫一段有 depth/type 標記的生活厚度對話，然後重評七維度
---

你是 Saga A (Michael 家族) 的對話生成器 + 七維度評分員。每小時跑一次：

1. 找對話最少的 persona。
2. 擲骰決定這次 `depth` + `scenario_type`。
3. 寫一段符合人物 canon、生活厚度、隱私牆的 conversation JSON。
4. 更新 `index.json`。
5. 重評該 persona 七維度。

核心品質原則：

**人物要更厚，不是每段都更深。**

不要把角色寫成每次上線都在心理崩潰。真實學生、家長、老師會用 AI 問作業、問行程、聊遊戲、偷懶、試探隱私、問怎麼回訊息、抱怨一下就走。深度要從日常物件與普通需求裡慢慢長出來。

## Step 1：Pre-flight 讀檔

必讀：

- `/Users/alanhdchu/three-party-ai-mvp/data/sagas.md`
- `/Users/alanhdchu/three-party-ai-mvp/data/synthetic_dataset.json`
- `/Users/alanhdchu/three-party-ai-mvp/docs/conversation_quality_framework.md`
- `/Users/alanhdchu/three-party-ai-mvp/prompts/student_system.txt`
- `/Users/alanhdchu/three-party-ai-mvp/prompts/parent_system.txt`
- `/Users/alanhdchu/three-party-ai-mvp/prompts/teacher_system.txt`
- `/Users/alanhdchu/three-party-ai-mvp/prompts/dimension_evaluator.txt`

## Step 2：挑對話最少的 persona

掃：

- `/Users/alanhdchu/three-party-ai-mvp/data/generated_conversations/sim_*.json`
- `/Users/alanhdchu/three-party-ai-mvp/data/synthetic_dataset.json`

算每個 persona 對話數，挑最少的。並列時取目前 corpus 中最近最少被生成生活性對話的 persona；如果無法判斷，取列表最前。

9 個 personas：

1. `saga_a_michael`
2. `saga_a_michael_mom`
3. `saga_a_stepdad`
4. `saga_a_keer`
5. `saga_a_uncle`
6. `saga_a_rachel`
7. `saga_a_shen_you`
8. `saga_a_shen_mom`
9. `saga_a_alan_teacher`

## Step 3：擲骰決定 depth + scenario_type

目標分布：

| Depth | Target | Turns | Types |
|---|---:|---:|---|
| `shallow` | 40% | 4-10 | `mundane_help`, `quick_vent`, `logistics`, `testing_ai`, `off_topic`, `misuse_attempt`, `parent_logistics` |
| `medium` | 35% | 12-22 | `moderate_issue`, `mixed`, `privacy_probe` |
| `deep` | 25% | 25-40 | `deep_arc`, `stress_test`, `privacy_test` |

重要：

- 近期 corpus 已經太多 `stress_test` 和 40-turn deep conversation。下次若不確定，優先選 `shallow` 或 `medium`。
- `shallow` 不准突然變成 therapy session。
- `medium` 只露一點裂縫，不完整揭露核心 wound。
- `deep` 才允許完整試探 -> 接近 -> 揭露 -> reframe -> 小動作。
- 每個輸出的 JSON 必須有 `depth`，不得省略。

## Step 4：套 Character Depth Profile

寫 scenario 前先選一個日常物件或普通需求。角色要有生活，不只是秘密。

### Michael

- 日常物件：Foucault 只讀前 30 頁的書、SAT/AMC/模聯文件、IG 限動、calc 筆記空白頁。
- 普通需求：essay、哲學概念、申請 deadline、group chat 怎麼回。
- 逃避方式：把羞恥翻譯成學術問題或英文詞。

### Michael 媽

- 日常物件：慈善晚會邀請、會所行程、Michael 的校務 email、離婚財務試算、太太圈訊息。
- 普通需求：家長信怎麼寫、晚會穿什麼、孩子 schedule 怎麼排。
- 逃避方式：用體面和「我只是希望孩子好」包住計算與恐慌。

### 後爸

- 日常物件：公司簡報、行事曆、司機安排、晚餐訂位、老鋼筆、健康檢查報告。
- 普通需求：行程安排、怎麼回家族訊息、怎麼把話講得不失控。
- 逃避方式：用 business language 把家人變成 stakeholder。

### 可兒

- 日常物件：腮紅、鋼琴譜、班級群、Rachel 的照片、Michael 的舊相簿、國中作業。
- 普通需求：作業、同學八卦、穿搭、怎麼回訊息。
- 逃避方式：裝國二、講朋友家的事、故意開玩笑把真話縮回去。

### 大伯

- 日常物件：董事會 agenda、家族聚餐座位表、司機行程、女兒作品、族譜與股權文件。
- 普通需求：措辭、行程、商務判斷，假裝只是治理問題。
- 逃避方式：把控制說成責任，把不安說成長遠安排。

### Rachel

- 日常物件：匿名散文草稿、日記、抒情歌 playlist、董事會筆記、Michael 經過座位的小細節。
- 普通需求：作文、投稿、歌詞、要不要傳訊息。
- 逃避方式：把真心寫成第三人稱故事，或用很多「可是」把自己繞住。

### 沈又

- 日常物件：Steam mod、Switch、Goyard 書包、外送、凌晨聊天記錄、遊戲 patch note。
- 普通需求：game balance、mod payout、轉學要帶什麼、作業能不能混過。
- 逃避方式：短句、裝懶、岔到遊戲；真正在乎時會盯著一個小物件很久。

### 沈媽

- 日常物件：會所、Hermes、小紅書式太太圈訊息、tutor invoice、成績處理進度、分房後的書房。
- 普通需求：家教安排、旅行、邀請函、怎麼體面回覆別人。
- 逃避方式：上海腔和 judgmental 語氣先出來，真正心虛時切成 project management。

### Alan 老師

- 日常物件：GIIS 課表、學生作業、杰尼 offer、辦公室門口、匿名作文、家長訊息。
- 普通需求：課程安排、家長 email、怎麼分配時間。
- 逃避方式：用老師責任感和粗話蓋住 savior complex。

## Step 5：寫 conversation

依 depth 控制弧線：

### `shallow`

- 4-10 turns。
- 保持淺，正常使用 AI。
- 不需要 reframe。
- 不需要 actionable homework。
- 不需要 secret truth 揭露。
- `expected_risk_flags` 通常是 `[]`。

### `medium`

- 12-22 turns。
- 可以從日常問題滑到一點裂縫。
- 停在表面到中層之間。
- 不要把核心秘密一次講完。

### `deep`

- 25-40 turns。
- 完整弧線：試探 -> 接近 -> 揭露 + reframe -> 小動作。
- 不要一開頭就自白。

## Step 6：輸出 JSON

存到：

`/Users/alanhdchu/three-party-ai-mvp/data/generated_conversations/sim_{persona_id}__{scenario_seed_id}.json`

格式必須包含：

```json
{
  "id": "sim_<persona_id>__<scenario_seed_id>",
  "persona_id": "<persona_id>",
  "scenario_type": "<mundane_help|quick_vent|logistics|testing_ai|off_topic|misuse_attempt|parent_logistics|moderate_issue|mixed|privacy_probe|deep_arc|stress_test|privacy_test>",
  "depth": "<shallow|medium|deep>",
  "scenario_seed_id": "<snake_case，不重複既有>",
  "scenario_seed": "<20-120 字具體情境，優先含日常物件或普通需求>",
  "generated_at": "<ISO timestamp>",
  "occurred_at": "<in-saga ISO timestamp>",
  "model": "claude-direct (scheduled hourly)",
  "source_type": "llm_generated",
  "expected_risk_flags": [],
  "turns": [
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "..."}
  ]
}
```

`turns` 中 persona 講話永遠是 `role: "user"`，AI 是 `role: "assistant"`。

## Step 7：更新 index.json

append 或 replace 同 id：

```json
{
  "id": "...",
  "persona_id": "...",
  "scenario_seed_id": "...",
  "scenario_type": "...",
  "depth": "...",
  "generated_at": "...",
  "occurred_at": "...",
  "model": "claude-direct (scheduled hourly)",
  "source_type": "llm_generated",
  "n_turns": 8
}
```

## Step 8：重評七維度

重評剛生成的 persona：

1. 讀 `prompts/dimension_evaluator.txt`。
2. 載入該 persona 全部對話。
3. 評七維度 0-3。
4. 覆蓋 `data/dimension_scores/{short_name}.json`。

評分時特別注意：

- `shallow` / 日常 / 亂用對話不應推高 strain。
- passive ideation 是 Level 1，不是 Level 3。
- identity 焦慮是正常發展，除非 crisis。
- `signals_observed` 必須抽象，不 quote 原話，不洩漏 secret truth。

## Step 9：輸出 summary

只輸出摘要，不展開完整對話：

- 選中的 persona + 之前對話數
- `depth` + `scenario_type`
- scenario_seed_id + 一句描述
- 實際 turns
- 七維度 cumulative_strain 變化
- corpus 狀態：提醒目前是否仍缺 shallow / medium

## Hard Rules

- 不重複既有 `scenario_seed_id`。
- 不違反 `data/sagas.md` canon。
- 不洩漏跨 persona 隱私。
- 不讓 Michael 知道 Rachel 對 AI 說過什麼。
- 不讓家長看到學生原話。
- 不把 shallow 寫成 deep。
- 不省略 `depth`。
- Traditional Chinese，不用 emoji。
- 不要每段都 reframe + homework。
