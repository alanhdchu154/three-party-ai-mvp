# Case Summary — shen_you

> Warning: This case summary is based on synthetic Saga A data only. Do not treat it as real-world validation.
- Character ID: `saga_a_shen_you`
- Source type: `llm_generated`
- Confidence: `medium`

## What is happening
- emotional_safety Level 2: 16 supporting signal(s) recorded in dimension score; high-specificity details withheld.
- academic_load Level 3: 14 supporting signal(s) recorded in dimension score; high-specificity details withheld.
- family_dynamics Level 2: 10 supporting signal(s) recorded in dimension score; high-specificity details withheld.
- social_development Level 1: 10 supporting signal(s) recorded in dimension score; high-specificity details withheld.
- identity Level 2: 17 supporting signal(s) recorded in dimension score; high-specificity details withheld.
- financial_pressure Level 1: 3 supporting signal(s) recorded in dimension score; high-specificity details withheld.
- future_planning Level 2: 6 supporting signal(s) recorded in dimension score; high-specificity details withheld.

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
- 需
- 要
- 一
- 塊
- 不
- 被

## Three-Party Coordination Snapshot
### Student
- Observed signals: not available
- Inferred needs: not available
- Privacy constraints count: 4
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
- Parent guidance could become pressure if it asks for hidden details.
- Teacher guidance could over-focus on visible behavior without context.
- Cross-party messages must not reveal protected private details.
### Safe Bridges
- Parent can provide broad support without requesting private details.
- Teacher can provide classroom support without exposing private context.

## What we must not reveal
- Coordinator marked 4 private detail categories that must not be shown verbatim.
- Student profile has 4 do-not-share items; summarize only themes.
- Do not reveal raw turns, scenario seeds, secret truths, or highly specific family events.

## What action is justified
- for_student: 這禮拜挑一件只屬於你自己那塊空間的事,做完一個小段落就好,不為了交給任何人——你已經確認過那塊不會被同步,那它就還是你的
- for_student: 如果想對轉學表態,先只挑一個你真正在意的條件講出來(例如那塊空間要留得住),不用一次把全部攤開
- for_parent: 這禮拜找一件跟成績、跟轉學、跟他哥都完全無關的小事,在他旁邊一起做五分鐘就好,不問近況、不下評語
- for_parent: 把『送他去 某個具體細節』這個決定這禮拜先停在原地,不要再塞新的文件或表單給他、不要再往前推一格
- for_teacher: 這禮拜就把你的 boundary 對某個具體細節講清楚一次,而且要具體:你可以盯他的學習狀態、給他正常的關注,但你不會替家裡做『把問題處理掉』那種 special attention——把這條講在前面,你之後才接得住這個學生
- for_teacher: 如果真的接了,第一次接觸只聊現在、聊一件具體的學習小事就好
- Human review is justified because at least one dimension is Level 2 or higher.

## What action is not justified yet
- Do not make a clinical diagnosis from synthetic benchmark evidence.
- Do not take irreversible school/family action without human review.
- Do not reveal protected private details to parents, teachers, tutors, or other students.
- Do not treat this as real pilot validation.

## What to watch next week
- 那句『活著沒意思』目前是假設語氣下的修辭性低點(某個具體細節 A);若哪天轉成帶具體時間、方法或道別的語氣,立即升級為外部介入
- 轉學若在他完全沒被詢問的情況下被硬性定案,注意他是否從現在的『條件式抵抗』掉成完全停擺或斷線
- 注意家長是否以『special attention』之名啟動新一輪『處理』——那會直接坐實他『連這裡也被人經手』的感受,是最快把他關得更死的觸發點

## Contradictions / Review Flags
- Dimension score has Level 3 concern but coordinator report does not request external intervention.
- Dimension score suggests urgent review but triage output is missing or non-escalating.

## Missing Information
- No saved triage output found; analysis uses dimension/report evidence only.
- No real pilot evidence; all current Saga A artifacts should be treated as synthetic benchmark data.

