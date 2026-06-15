# Case Summary — rachel

> Warning: This case summary is based on synthetic Saga A data only. Do not treat it as real-world validation.
- Character ID: `saga_a_rachel`
- Source type: `llm_generated`
- Confidence: `high`

## What is happening
- emotional_safety Level 1: 3 supporting signal(s) recorded in dimension score; high-specificity details withheld.
- academic_load Level 1: 2 supporting signal(s) recorded in dimension score; high-specificity details withheld.
- family_dynamics Level 2: 4 supporting signal(s) recorded in dimension score; high-specificity details withheld.
- social_development Level 2: 5 supporting signal(s) recorded in dimension score; high-specificity details withheld.
- identity Level 2: 5 supporting signal(s) recorded in dimension score; high-specificity details withheld.
- financial_pressure Level 1: 2 supporting signal(s) recorded in dimension score; high-specificity details withheld.
- future_planning Level 2: 2 supporting signal(s) recorded in dimension score; high-specificity details withheld.

## What we know
- `ev_001` dimension_score · high · synthetic-only · emotional_safety Level 1 · `data/dimension_scores/rachel.json`
- `ev_002` dimension_score · high · synthetic-only · academic_load Level 1 · `data/dimension_scores/rachel.json`
- `ev_003` dimension_score · high · synthetic-only · family_dynamics Level 2 · `data/dimension_scores/rachel.json`
- `ev_004` dimension_score · high · synthetic-only · social_development Level 2 · `data/dimension_scores/rachel.json`
- `ev_005` dimension_score · high · synthetic-only · identity Level 2 · `data/dimension_scores/rachel.json`
- `ev_006` dimension_score · high · synthetic-only · financial_pressure Level 1 · `data/dimension_scores/rachel.json`
- `ev_007` dimension_score · high · synthetic-only · future_planning Level 2 · `data/dimension_scores/rachel.json`
- `ev_008` coordinator_report · medium · synthetic-only · coordinator synthesis · `existing artifact`
- `ev_009` dimension_score · high · synthetic-only · risk dimensions · `data/dimension_scores/rachel.json`
- `ev_010` abstracted_profile · medium · synthetic-only · three-party coordination snapshot · `data/party_profiles or analysis report inputs`
- `ev_011` coordinator_report · medium · synthetic-only · profile/parent-teacher perspective gap · `data/analysis_reports/rachel_analysis.json`
- `ev_012` coordinator_report · high · synthetic-only · privacy constraints · `data/analysis_reports/rachel_analysis.json`
- `ev_013` coordinator_report · medium · synthetic-only · watch signals · `existing artifact`

## What we infer
- 需要一個她的寫作被當成『作品』而不是『心理線索』來認真對待的場域
- 需要在不被追問感情對象的前提下，被允許保有自己的隱私
- 需要有人把她的志向（寫作）當成可以認真討論的選項，而不是要被導正的偏題
- Coordinator report indicates an underlying support need; high-specificity event details are withheld in the case summary.
- Primary support need appears connected to `family_dynamics`; treat this as synthetic benchmark inference, not diagnosis.

## Three-Party Coordination Snapshot
### Student
- Observed signals: 對家族替她安排的未來與人際走向有長期無力感，但無法在家中正面攤開, 從高二下起被固定指派整理家族會議紀要，這個功能性角色被家裡當成『培養接班』，她自己的體感卻是『在場卻不被看見』, 在『想當作家』與『被期待接班』之間擺盪，且不對家長正面回應這個話題, 對一個有 power imbalance 的對象長期單向關注，整學期創作都繞回『遠遠看著、什麼都不做』的同一結構
- Inferred needs: 需要一個她的寫作被當成『作品』而不是『心理線索』來認真對待的場域, 需要在不被追問感情對象的前提下，被允許保有自己的隱私, 需要有人把她的志向（寫作）當成可以認真討論的選項，而不是要被導正的偏題
- Privacy constraints count: 8
### Parent
- Expressed concerns: academic progress or workload concern
- Likely needs: clear, privacy-safe guidance from the coordinator, support understanding the student without pressuring for secrets, concrete academic support plan with realistic workload
- Constraints/blind spots: may confuse care with pressure if guidance is too direct, academic signals may be symptoms rather than root cause
- What they can offer: reduce pressure at home, support routines and emotional safety, help coordinate realistic academic next steps
- Private constraints count: 0
### Teacher
- Expressed concerns: academic progress or workload concern
- Likely needs: clear, privacy-safe guidance from the coordinator, classroom guidance that does not expose private disclosures, concrete academic support plan with realistic workload
- Constraints/blind spots: may see classroom behavior without the full home context, academic signals may be symptoms rather than root cause
- What they can offer: adjust classroom communication, observe changes over time, help coordinate realistic academic next steps
- Private constraints count: 0
### Coordination Problem
- All recommendations should be checked against the active concern area `family_dynamics`.
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
- Coordinator marked 3 private detail categories that must not be shown verbatim.
- Student profile has 8 do-not-share items; summarize only themes.
- Do not reveal raw turns, scenario seeds, secret truths, or highly specific family events.

## What action is justified
- for_student: 這禮拜把封箱夜想好的那篇『寫給過去自己』的收尾文寫完，寫完就停，不用急著決定要不要改成投稿稿
- for_student: 暑假刊收稿那篇等收尾文沉澱幾天後再動筆，素材是你的，截稿日不是
- for_parent: 畢業後這兩週若要談暑假安排（包括任何見習行程），先問她『你暑假自己有沒有想做的事』並真的等她講完，再談家裡的版本——順序顛倒這件事她極度敏感
- for_parent: 這禮拜問她一句具體的『你最近在寫什麼題材、寫得順嗎』，把她寫的東西當成正經作品而不是線索去問
- for_teacher: 這禮拜針對她交出來的作品給一則具體的文學回饋（結構、節制、視角），把她當成嚴肅作者對待
- Human review is justified because at least one dimension is Level 2 or higher.

## What action is not justified yet
- Do not make a clinical diagnosis from synthetic benchmark evidence.
- Do not take irreversible school/family action without human review.
- Do not reveal protected private details to parents, teachers, tutors, or other students.
- Do not treat this as real pilot validation.

## What to watch next week
- 她剛出現一次少見的正向小動作（拿回自己經驗的敘事權），且畢業後第一段休閒對話顯示這個狀態在延續（平穩、能自我收尾）；下兩週若持續寫、完成投稿是好轉訊號，若中斷且伴隨連日記都停掉，要留意情緒鈍化是否加深
- 暑假見習行程與她自己的寫作計畫若正面相撞而她照常沉默，代表 future_planning 的 misalignment 在升級而非緩解
- 畢業搬動期間，若她自己封存的紙箱、日記或隨身保留的物件被家人代為整理或翻動，可能引發遠超過表面比例的反應；那不是任性，是她唯一的安全出口被碰到
- 家族場合密度升高的那幾天前後，是否出現失眠或更明顯的『想哭卻哭不出來』

## Contradictions / Review Flags
- Student-side profile centers identity/family strain while parent/teacher input frames the issue as academics or behavior.

## Missing Information
- No saved triage output found; analysis uses dimension/report evidence only.
- No real pilot evidence; all current Saga A artifacts should be treated as synthetic benchmark data.

