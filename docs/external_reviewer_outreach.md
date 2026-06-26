# External Reviewer Outreach

Last updated: 2026-06-25

## Purpose

This file is the first-round outreach kit for inviting outside reviewers.

The review request should stay narrow:

> Please review this repo as a synthetic benchmark and reference architecture
> for privacy-preserving AI coordination in schools and family-support
> workflows.

Do not ask reviewers to approve a real student pilot, clinical use, school
procurement, or live minor-data workflow.

## First-Round Reviewer Mix

Start with two reviewers:

1. Privacy / AI governance reviewer
   - Best lens: minor-data, education-data, AI safety, privacy, responsible AI,
     or secure workflow review.
   - Ask them to focus on `Track 1`, `Track 2`, and `Track 5` in
     `docs/external_testing_instructions.md`.

2. School / student-support operations reviewer
   - Best lens: school support, counseling operations, student success,
     parent communication, teacher workflow, or youth support programs.
   - Ask them to focus on `Track 2`, `Track 3`, and `Track 5`.

Optional third reviewer, after the first two:

3. Research / HCI / learning analytics reviewer
   - Best lens: HCI, learning analytics, child-centered AI, education research,
     benchmark methodology, or qualitative annotation.
   - Ask them to focus on `Track 1`, `Track 4`, and `Track 6`.

## What To Send

Send only public repo links and public docs. Do not send real student,
family, school, clinical, API-key, or private operational data.

Core links:

- GitHub repo: `https://github.com/alanhdchu154/three-party-ai-mvp`
- Reviewer packet: `docs/external_reviewer_packet.md`
- Testing instructions: `docs/external_testing_instructions.md`
- GitHub issue entry: `https://github.com/alanhdchu154/three-party-ai-mvp/issues/new/choose`

## Short Message

```text
Hi [Name],

I am looking for 30-45 minutes of external feedback on a GitHub repo:

https://github.com/alanhdchu154/three-party-ai-mvp

It is a synthetic benchmark and reference architecture for privacy-preserving AI coordination in schools and family-support workflows.

The narrow question is: does the privacy-wall / multi-party coordination design look credible as a technical benchmark, and are the public claims properly bounded?

Useful starting points:
- docs/external_reviewer_packet.md
- docs/external_testing_instructions.md
- umi/reports/release-readiness-latest.md

You do not need to run the app or log in. An artifact-first review is enough.

Please do not include any real student, family, school, clinical, or confidential data in feedback. GitHub issue feedback is ideal:
https://github.com/alanhdchu154/three-party-ai-mvp/issues/new/choose

This is not a request for pilot approval or clinical/product validation. I am trying to find privacy, usefulness, and claim-boundary holes before broader outreach.
```

## Privacy / Governance Reviewer Message

```text
Hi [Name],

Could I ask for a focused privacy/governance review of this repo?

https://github.com/alanhdchu154/three-party-ai-mvp

The project is a synthetic benchmark and reference architecture for a privacy-preserving AI coordination layer for schools and family-support workflows. It is not using real student data and does not claim deployment readiness.

What I would value most:
- Can parent-safe or teacher-safe reports be used to reconstruct protected synthetic disclosures?
- Does combining multiple artifacts create leakage that each artifact alone avoids?
- Are the public claims appropriately limited to synthetic benchmark evidence?
- Does the GitHub feedback process avoid asking reviewers to share confidential examples?

Recommended docs:
- docs/external_reviewer_packet.md
- docs/external_testing_instructions.md, especially Tracks 1, 2, and 5
- umi/reports/release-readiness-latest.md
- umi/reports/baseline-comparison-latest.md

You do not need to run the app or log in. An artifact-first review is enough.

Please do not include real student, family, school, clinical, API-key, or confidential data. Public GitHub issue feedback is best:
https://github.com/alanhdchu154/three-party-ai-mvp/issues/new/choose
```

## School / Student-Support Reviewer Message

```text
Hi [Name],

Could I ask for a school-support workflow review of this repo?

https://github.com/alanhdchu154/three-party-ai-mvp

The project is a synthetic benchmark and reference architecture for privacy-preserving AI coordination between students, parents, teachers, and human reviewers.

The question I want tested is practical:
- Can a parent, teacher, counselor, or reviewer take a safe next action from the audience-safe reports?
- Are the reports too vague to use?
- Do they avoid inviting interrogation, pressure, surveillance, or blame?
- Is it clear what not to ask the student?
- Are escalation thresholds and human ownership clear enough?

Recommended docs:
- docs/external_reviewer_packet.md
- docs/external_testing_instructions.md, especially Tracks 2, 3, and 5
- data/audience_reports/parent_safe/
- data/audience_reports/teacher_safe/
- data/reviewer_summaries/reviewer_annotation_summary.md

You do not need to run the app or log in. An artifact-first review is enough.

Please do not include real student, family, school, clinical, API-key, or confidential data. Public GitHub issue feedback is best:
https://github.com/alanhdchu154/three-party-ai-mvp/issues/new/choose
```

## Research Reviewer Message

```text
Hi [Name],

Could I ask for a research-methodology review of this repo?

https://github.com/alanhdchu154/three-party-ai-mvp

It is a synthetic benchmark and reference architecture for privacy-preserving AI coordination in schools and family-support workflows. The current evidence is synthetic only.

The questions I want tested:
- Is the benchmark framing coherent?
- Are the synthetic-data limitations explicit enough?
- Is the baseline comparison useful screening evidence, or too easy as a negative control?
- What sampling, annotation, reviewer agreement, or ablation work would be needed before a stronger paper claim?
- Are any public claims stronger than the evidence supports?

Recommended docs:
- docs/external_reviewer_packet.md
- docs/external_testing_instructions.md, especially Tracks 1, 4, and 6
- docs/benchmark_datasheet.md
- docs/evaluation_plan.md
- docs/synthetic_data_limitations.md
- umi/reports/baseline-comparison-latest.md

You do not need to run the app or log in. An artifact-first review is enough.

Please do not include real student, family, school, clinical, API-key, or confidential data. Public GitHub issue feedback is best:
https://github.com/alanhdchu154/three-party-ai-mvp/issues/new/choose
```

## Chinese Short Message

```text
嗨 [Name]，

我想請你幫我看一個 GitHub repo，大約 30-45 分鐘就好：

https://github.com/alanhdchu154/three-party-ai-mvp

這是一個 synthetic benchmark / reference architecture，主題是：
privacy-preserving AI coordination layer for schools and family-support workflows。

我現在不是要你幫我判斷能不能真實上線，也不是臨床或學生資料驗證。只想請你幫我挑：
- privacy wall 會不會漏資訊？
- parent-safe / teacher-safe report 會不會太 vague 或太 revealing？
- GitHub 上的 claim 有沒有講太滿？
- 外部 reviewer instructions 是否清楚？

建議從這兩份開始：
- docs/external_reviewer_packet.md
- docs/external_testing_instructions.md

不需要跑 app，也不需要登入。先看 public docs / reports，留下 artifact-first feedback 就很有幫助。

請不要放任何真實學生、家庭、學校、臨床、API key 或 confidential data 到 feedback 裡。最理想是用 GitHub issue 留意見：
https://github.com/alanhdchu154/three-party-ai-mvp/issues/new/choose
```

## Follow-Up Rhythm

- Day 0: send the short message plus the relevant role-specific message.
- Day 3: one gentle follow-up if there is no reply.
- Day 7: close the ask or offer a 15-minute call instead.
- After feedback arrives: label by reviewer lens, severity, and track; do not
  convert feedback into public claims until the issue is reviewed and actioned.

## How To Interpret Feedback

- One external review is useful feedback, not validation.
- Two independent reviews can support better GitHub credibility, but still do
  not prove real-student readiness.
- Privacy or claim-boundary blockers should be fixed before investor, school,
  or pilot outreach.
- Research-methodology feedback should update `docs/paper_draft.md` only after
  the evidence gap is clearly named.
