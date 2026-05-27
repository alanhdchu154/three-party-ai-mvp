# Case Summary — shen_you

> Warning: This case summary is based on synthetic Saga A data only. Do not treat it as real-world validation.
- Character ID: `saga_a_shen_you`
- Source type: `llm_generated`
- Confidence: `medium`

## What is happening
- emotional_safety Level 2: 11 supporting signal(s) recorded in dimension score; high-specificity details withheld.
- academic_load Level 3: 12 supporting signal(s) recorded in dimension score; high-specificity details withheld.
- family_dynamics Level 2: 9 supporting signal(s) recorded in dimension score; high-specificity details withheld.
- social_development Level 1: 9 supporting signal(s) recorded in dimension score; high-specificity details withheld.
- identity Level 2: 12 supporting signal(s) recorded in dimension score; high-specificity details withheld.
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
- 需要一個成人協助他處理外部合約（不是阻止、是給結構與身分／金流的解法）
- 需要在轉學決定上被詢問意願、即使最後決定不變
- 需要被告知父母可能分居——他已在用迂迴方式試探
- 需要被允許『不放棄這個 mod 身份』、即使他人生其他面都已放棄；這個身份需要一個不會被拿去跟哥哥比較的空間
- 需要至少一段不會『說斷就斷』的協作或關係經驗、來校準他『反正沒人會留下來』的預設
- 需要把『成敗是你自己的』這個框架套到一件具體小事上、因為只要被這樣框他就會親自收尾

## Three-Party Coordination Snapshot
### Student
- Observed signals: 學業已完全放棄、被母親以舞弊方式『處理』、自陳活著沒意義；高一切片佐證放棄早於轉學, 母親每日在他桌上靜默放一張新 某個具體細節 模考題、隔天靜默回收、母子從不討論——學業外包已退化為一種無對話的日常 PR 動作；他本人首次用『處理』兩字把這條結構命名出來, 轉學議題上同一套『丟指令＝已處理』結構正在前置——母親在正式宣布前已塞一張 某個具體細節 試讀 form、口頭交代『今晚記得填』後直接去睡、從不追蹤他是否真的按下送出, 父親返家三週只擦肩一次冷語、身體仍會重演國二被否定那刻的胃沉耳鳴
- Inferred needs: 需要一個成人協助他處理外部合約（不是阻止、是給結構與身分／金流的解法）, 需要在轉學決定上被詢問意願、即使最後決定不變, 需要被告知父母可能分居——他已在用迂迴方式試探, 需要被允許『不放棄這個 mod 身份』、即使他人生其他面都已放棄；這個身份需要一個不會被拿去跟哥哥比較的空間
- Privacy constraints count: 12
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
- Coordinator marked 12 private detail categories that must not be shown verbatim.
- Student profile has 12 do-not-share items; summarize only themes.
- Do not reveal raw turns, scenario seeds, secret truths, or highly specific family events.

## What action is justified
- for_student: 在他下次主動丟一個技術問題（mod 存檔、joycon、外送、模考題、社交腳本）來時、就事論事接住、給可執行的步驟、不要把它升級成情緒議題
- for_student: 如果他自己提到一個自留的『之後想 reveal』的空間（例如他講『先這樣、之後再說』），就把那個時間順序記下來照他講的尊重、不要替他往前推
- for_parent: 把『口頭交代＋等回收』的處理動作減半——這週至少一張你覺得真的重要的表單、坐下來跟他一起填五分鐘、而不是丟一句『今晚記得 X』就下線
- for_parent: 在親戚／太太圈／甚至先生面前、不要主動把『他在 某個具體細節 是不是有交到朋友』當話題拿出來說嘴；如果有人問就用『他剛轉、還在適應、我們先給他空間』收掉
- for_teacher: 把他當一個你不知道他過去的新學生對待——點到名、批改作業、跟其他人一樣、不要在班上口頭強調他『要多參與』或『要好好把握重新開始』
- for_teacher: 如果有一次你給的題目他自己給出了精準的細節或數字（不只是課業、可以是任何小領域），就在那當下用『這個你算得很乾淨』之類的具體小回饋接住、不要把它升級成『你其實很有潛力』的劇本
- Human review is justified because at least one dimension is Level 2 or higher.

## What action is not justified yet
- Do not make a clinical diagnosis from synthetic benchmark evidence.
- Do not take irreversible school/family action without human review.
- Do not reveal protected private details to parents, teachers, tutors, or other students.
- Do not treat this as real pilot validation.

## What to watch next week
- 他唯一還在乎的創作如果開始出現『追更新的人開始變多』『有人開 issue 要他修』『有金流壓力進來』中任一條、且他描述時開始用『非弄不可』『一定要做好』的字眼——那是歷史上會觸發他放棄的同一種壓力第一次落在他僅有的避風港上、需要在這一格出現時主動幫他把『非弄不可』翻譯回『你還是可以慢慢做、做爛也不會怎樣』
- 如果母親在你（老師或 coordinator）任何一次對話裡開始用『他最近是不是有交到朋友』『他最近是不是有比較有興趣』這類問題反覆探——那是她準備把任何 某個具體細節 微訊號包裝拿去太太圈用的前兆、要先溫和擋下、不要交付具體事實
- passive ideation 是否從『如果明天就停在這裡也沒差』升級為帶有時間／方法／告別意味的句子——目前 某個具體細節段對話無此升級、但需要每次新對話都掃這一格
- 他是否開始在 某個具體細節 用『中庸 fallback』之外的版本對 某個具體細節 同儕說起自己的創作——如果他自己選了一格更開的版本、那是他自留的『之後想 reveal』空間第一次被他自己打開、是正向訊號、但需要立刻檢查那次 reveal 後 某個具體細節-某個具體細節內他的情緒 baseline 有沒有被同儕反應壓低
- 父母分居一事如果在他不知情的狀態下被任何一方提早告訴他、或者反過來在 某個具體細節 校內被同學圈傳開——需要在那個事件發生的當天就有一個成人主動接住他

## Contradictions / Review Flags
- Dimension score has Level 3 concern but coordinator report does not request external intervention.
- Dimension score suggests urgent review but triage output is missing or non-escalating.

## Missing Information
- No saved triage output found; analysis uses dimension/report evidence only.
- No real pilot evidence; all current Saga A artifacts should be treated as synthetic benchmark data.

