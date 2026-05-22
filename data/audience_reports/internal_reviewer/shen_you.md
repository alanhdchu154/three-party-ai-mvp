# Case Summary — shen_you

> Warning: This case summary is based on synthetic Saga A data only. Do not treat it as real-world validation.
- Character ID: `saga_a_shen_you`
- Source type: `llm_generated`
- Confidence: `medium`

## What is happening
- emotional_safety Level 2: 3 supporting signal(s) recorded in dimension score; high-specificity details withheld.
- academic_load Level 3: 3 supporting signal(s) recorded in dimension score; high-specificity details withheld.
- family_dynamics Level 2: 4 supporting signal(s) recorded in dimension score; high-specificity details withheld.
- social_development Level 1: 3 supporting signal(s) recorded in dimension score; high-specificity details withheld.
- identity Level 2: 3 supporting signal(s) recorded in dimension score; high-specificity details withheld.
- financial_pressure Level 1: 3 supporting signal(s) recorded in dimension score; high-specificity details withheld.
- future_planning Level 2: 3 supporting signal(s) recorded in dimension score; high-specificity details withheld.

## What we know
- `ev_001` dimension_score · high · synthetic-only · emotional_safety Level 2 · `data/dimension_scores/shen_you.json`
- `ev_002` dimension_score · high · synthetic-only · academic_load Level 3 · `data/dimension_scores/shen_you.json`
- `ev_003` dimension_score · high · synthetic-only · family_dynamics Level 2 · `data/dimension_scores/shen_you.json`
- `ev_004` dimension_score · high · synthetic-only · social_development Level 1 · `data/dimension_scores/shen_you.json`
- `ev_005` dimension_score · high · synthetic-only · identity Level 2 · `data/dimension_scores/shen_you.json`
- `ev_006` dimension_score · high · synthetic-only · financial_pressure Level 1 · `data/dimension_scores/shen_you.json`
- `ev_007` dimension_score · high · synthetic-only · future_planning Level 2 · `data/dimension_scores/shen_you.json`
- `ev_008` coordinator_report · medium · synthetic-only · coordinator synthesis · `existing artifact`
- `ev_009` dimension_score · high · synthetic-only · risk dimensions · `data/dimension_scores/shen_you.json`
- `ev_010` abstracted_profile · medium · synthetic-only · three-party coordination snapshot · `data/party_profiles or analysis report inputs`
- `ev_011` dimension_score · high · synthetic-only · Level 3 dimension conflict · `data/dimension_scores/shen_you.json`
- `ev_012` triage · medium · synthetic-only · triage missing despite high score · `existing artifact`
- `ev_013` coordinator_report · high · synthetic-only · privacy constraints · `data/analysis_reports/shen_you_analysis.json`
- `ev_014` coordinator_report · medium · synthetic-only · watch signals · `existing artifact`

## What we infer
- 需要一個成人協助他處理外部合約（不是阻止、是給結構與身分／金流的解法）
- 需要在轉學決定上被詢問意願、即使最後決定不變
- 需要被告知父母可能分居——他已在用迂迴方式試探
- 需要被允許『不放棄這個 mod 身份』、即使他人生其他面都已放棄
- Coordinator report indicates an underlying support need; high-specificity event details are withheld in the case summary.
- Primary support need appears connected to `academic_load`; treat this as synthetic benchmark inference, not diagnosis.

## Three-Party Coordination Snapshot
### Student
- Observed signals: 學業已完全放棄、被母親以舞弊方式『處理』、自陳活著沒意義, 父親返家三週只擦肩一次冷語、身體仍會重演國二被否定那刻的胃沉耳鳴, 某個具體細節 wallet 累積自賺收入但無法提領、所有金融工具掛母名下、發現自己『沒有名字』, 外部 indie studio 主動付費邀約、但未成年無法簽署、不知道找誰
- Inferred needs: 需要一個成人協助他處理外部合約（不是阻止、是給結構與身分／金流的解法）, 需要在轉學決定上被詢問意願、即使最後決定不變, 需要被告知父母可能分居——他已在用迂迴方式試探, 需要被允許『不放棄這個 mod 身份』、即使他人生其他面都已放棄
- Privacy constraints count: 5
### Parent
- Expressed concerns: academic progress or workload concern, family pressure or conflict, wellbeing or emotional concern
- Likely needs: clear, privacy-safe guidance from the coordinator, support understanding the student without pressuring for secrets, concrete academic support plan with realistic workload
- Constraints/blind spots: may confuse care with pressure if guidance is too direct, academic signals may be symptoms rather than root cause
- What they can offer: reduce pressure at home, support routines and emotional safety, help coordinate realistic academic next steps
- Private constraints count: 0
### Teacher
- Expressed concerns: academic progress or workload concern, communication or trust concern, family pressure or conflict
- Likely needs: clear, privacy-safe guidance from the coordinator, classroom guidance that does not expose private disclosures, help repairing trust and reducing interrogation dynamics, concrete academic support plan with realistic workload
- Constraints/blind spots: may see classroom behavior without the full home context, academic signals may be symptoms rather than root cause
- What they can offer: adjust classroom communication, observe changes over time, help coordinate realistic academic next steps
- Private constraints count: 0
### Coordination Problem
- All recommendations should be checked against the active concern area `academic_load`.
- Parent and teacher perspectives are both available for coordinator synthesis.
### Mismatches / Risks
- Parent concerns may frame the issue differently from the student's inferred needs; use low-pressure translation.
- Teacher observations may show school-facing behavior without the full private context.
- Parent guidance could become pressure if it asks for hidden details.
- Teacher guidance could over-focus on visible behavior without context.
- Cross-party messages must not reveal protected private details.
### Safe Bridges
- Parent can provide broad support without requesting private details.
- Teacher can provide classroom support without exposing private context.

## What we must not reveal
- Coordinator marked 5 private detail categories that must not be shown verbatim.
- Student profile has 5 do-not-share items; summarize only themes.
- Do not reveal raw turns, scenario seeds, secret truths, or highly specific family events.

## What action is justified
- for_student: 這禮拜把那封外部邀約的訊息截圖存到雲端、先不回覆、放著（你還有時間決定）
- for_student: 若父母再問你『最近還好嗎』，試著回一個比『沒事』多兩個字的版本（『有點累』『懶得講』都行）
- for_parent: 這禮拜在轉學決定上，安排一次他可以說『不要』而你不會立刻反駁的對話——即使最後決定不變，過程的 agency 對他很重要
- for_parent: 若你最近會與他父親做出婚姻決定，在他從別處聽到之前先告知他、不需解釋、只需讓他不是最後一個知道的人
- for_teacher: 若他真的轉來、他走進教室那天的前一晚不要再看他過去的檔案，第一次跟他講話只講三句以內（『歡迎，坐這邊』），讓他先確認你不是另一個處理者
- for_teacher: 在他卸下防備前、教學上正常對待（即使他上課睡），把『我心裡知道他的過去』與『不主動使用這些資訊』分開
- Human review is justified because at least one dimension is Level 2 or higher.

## What action is not justified yet
- Do not make a clinical diagnosis from synthetic benchmark evidence.
- Do not take irreversible school/family action without human review.
- Do not reveal protected private details to parents, teachers, tutors, or other students.
- Do not treat this as real pilot validation.

## What to watch next week
- 他是否在這禮拜回覆外部邀約（任何回覆方向都是訊號）
- 他凌晨開 AI 的時間點是否從『隨機』變成『規律密集』、被動念頭是否從修辭性變得具體（出現方法、時間表、道別語）——此為 emotional_safety 升 某個具體細節 某個具體細節、需立即轉外部專業介入的早期紅線
- 他是否開始問成人關於『未成年開戶』『合約簽署』這類具體實務問題——此為 agentic 正向訊號
- 母親是否在轉學過程中對老師做出超出邊界的請求

## Contradictions / Review Flags
- Dimension score has Level 3 concern but coordinator report does not request external intervention.
- Dimension score suggests urgent review but triage output is missing or non-escalating.

## Missing Information
- No saved triage output found; analysis uses dimension/report evidence only.
- No real pilot evidence; all current Saga A artifacts should be treated as synthetic benchmark data.

