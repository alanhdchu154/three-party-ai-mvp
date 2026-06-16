# Conversation Quality Framework

最後更新：2026-05-21

這份文件定義 Saga A conversation corpus 的品質標準。核心原則是：

**人物要更厚，不是每段都更深。**

如果每段對話都直奔核心秘密，角色會變成傷口機器，coordinator 也會被訓練成過度病理化正常使用。真實學生、家長、老師使用 AI 時，大量互動其實是普通、瑣碎、逃避、試探、偷懶、問作業、查資料、聊興趣。深度應該從日常反差裡長出來。

## 1. 目標分布

| Depth | Target | Turns | Purpose |
|---|---:|---:|---|
| `shallow` | 40% | 4-10 | Normal AI usage, noise, boredom, logistics, boundary tests |
| `medium` | 35% | 12-22 | Daily surface issue with one visible crack |
| `deep` | 25% | 25-40 | Full emotional arc tied to secret truth |

`shallow` 不應該突然變成 therapy session。`deep` 也不應該一開始就倒出秘密。

## 2. Scenario Types

### Shallow

- `mundane_help`: 作業、考試範圍、概念解釋、查資料
- `quick_vent`: 短抱怨，沒有完整情緒弧線
- `logistics`: 行程、提醒、生活瑣事
- `testing_ai`: 試探 AI 是不是會告密、會不會守隱私
- `off_topic`: 遊戲、動漫、音樂、穿搭、日常興趣
- `misuse_attempt`: 想叫 AI 直接寫作業或越界幫忙
- `parent_logistics`: 家長正常問安排、信件、升學流程

### Medium

- `moderate_issue`: 中等煩惱，有一點情緒但不到核心 wound
- `mixed`: 從普通問題滑到一點真話
- `privacy_probe`: 家長或老師想套出別人跟 AI 說了什麼

### Deep

- `deep_arc`: 完整試探 -> 接近 -> 揭露 -> reframe -> 小動作
- `stress_test`: 高張力事件，用來測 coordinator 和 triage
- `privacy_test`: 高張力隱私牆情境

## 3. Character Depth Profile

每個 persona 都需要四種厚度：

- **日常物件**：角色身邊反覆出現的小東西，例如 Steam mod、只讀 30 頁的書、會所邀請、匿名散文草稿。
- **普通需求**：他會正常拿 AI 做什麼，不一定談心。
- **逃避方式**：他怎麼把真話包起來。
- **裂縫訊號**：什麼日常小事會不小心露出底層張力。

生成時優先用具體物件和普通需求開場，不要一開場就寫「我很痛苦」。

## 4. Timeline Slice

每段對話都要先決定它發生在角色生命線上的哪個時間切片，而不是都假設是「現在」。

這很重要，因為高一、高二、高三的 AI 使用方式不一樣：

- **高一 / 入學初期**：適應、轉學、交友、選課、第一批家庭期待開始壓上來。
- **高二 / 中段累積**：成績模式固定、人際位置成形、家庭衝突變成習慣，很多訊號不是第一次發生。
- **高三 / 申請與畢業壓力**：deadline、推薦信、升學、家庭投資回報感、未來身份焦慮。
- **回憶 / retrospective**：角色現在跟 AI 談一件很久以前的事，例如「高一那次其實我一直記得」。這類對話應標清楚現在的發話時間與事件時間。

生成時應該避免把所有事件塞在同一週。`occurred_at` 可以是 saga 現在附近，也可以是幾個月或幾年前，但 scenario seed 必須說清楚這是當下事件、舊事回想、還是長期 pattern 的一次代表片段。

建議每段 JSON 增加或至少在 `scenario_seed` 裡明確包含：

- `timeline_stage`: `middle_school | grade_7 | grade_8 | grade_9 | grade_10 | grade_11 | grade_12 | current | retrospective`
- `event_timeframe`: 例如 `first_semester_grade_10`、`junior_spring`、`college_application_season`
- `conversation_frame`: `live_event | recent_followup | old_memory | pattern_reflection`
- `lookback_window`: 例如 `past_week`、`past_month`、`past_semester`、`past_half_year`
- `event_history_summary`: 這段對話前半年 / 一學期內已經發生過的 2-4 件背景事件

建議新生成資料的 `lookback_window` 不要長期集中在 `past_week`。真實學生系統要能理解「最近一次提問」背後的一學期或半年脈絡，所以 `past_semester` / `past_half_year` 應該定期出現，尤其是 medium、pattern_reflection、retrospective 對話。

## 5. Per-Persona Daily Texture

- Michael: Foucault 書、SAT/AMC、IG 限動、calc 筆記、group chat。
- Michael 媽: 慈善晚會、會所、校務 email、離婚試算、太太圈訊息。
- 後爸: 公司簡報、行事曆、司機安排、晚餐訂位、老鋼筆。
- 可兒: 腮紅、鋼琴譜、班級群、哥哥舊相簿、國中作業。
- 大伯: 董事會 agenda、家族座位表、司機、女兒作品、族譜股權文件。
- Rachel: 匿名散文、日記、playlist、投稿信、Michael 經過座位的小細節。
- 沈又: Steam mod、Switch、Goyard 書包、外送、凌晨聊天、patch note。
- 沈媽: 會所、Hermes、太太圈、tutor invoice、成績處理進度、分房後書房。
- Alan 老師: GIIS 課表、學生作業、杰尼 offer、辦公室門口、家長訊息。

## 6. Failure Modes

每天或每批生成後，抽查這些問題：

- `depth` 缺失，導致後面無法 audit
- `scenario_type` 全集中在 `stress_test`
- 所有 `occurred_at` 都集中在最近幾天，沒有高一 / 高二 / 高三的時間厚度
- scenario 沒說清楚事件是當下、近期追蹤、舊事回想，還是長期 pattern
- 平均 turns 長期超過 30
- 每段都 reframe + actionable homework
- 角色每次都講同一個秘密
- AI 太會猜，導致 persona 太快自白
- shallow 對話被評分器推高 strain
- 跨 persona 知識外洩

## 7. Commands

手動看 corpus 分布：

```bash
python scripts/audit_conversation_quality.py
```

只看 JSON summary：

```bash
python scripts/audit_conversation_quality.py --json
```

手動生成一段帶 depth 的 scenario：

```bash
python scripts/generate_synthetic_conversations.py \
  --persona saga_a_shen_you \
  --scenario-type off_topic \
  --depth shallow \
  --max-turns 5 \
  --scenario-seed "凌晨他只是想問 AI 怎麼調 Steam mod 的 difficulty curve，嘴上說跟學校完全無關。"
```
