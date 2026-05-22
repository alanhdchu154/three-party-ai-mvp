# v0.9 GIIS Micro-Pilot Protocol

**Status**: internal draft, not legal advice  
**Audience**: Alan / GIIS operator / Umi reviewer  
**Pilot size**: 1-2 families only

## Purpose

This pilot tests whether a privacy-preserving AI support layer can help GIIS understand what kind of support a student needs next.

The pilot is not testing whether AI can replace counselors, teachers, parents, or tutors.

## Product Thesis Being Tested

People may tell AI things they cannot yet tell another person.

If those private disclosures can be translated into safe patterns without exposing raw secrets, GIIS can support students earlier and more appropriately.

## Who Should Join First

Choose families where:

- student and parent already have some trust with GIIS;
- student is old enough to understand privacy boundaries;
- parent is not demanding access to raw student conversations;
- no known active crisis is already underway;
- Alan can personally monitor the first 1-2 weeks.

Do not start with:

- highly adversarial parent-child relationships;
- active self-harm or abuse concerns;
- parents who explicitly want to use AI to find out secrets;
- families who expect a clinical service;
- cases where GIIS cannot provide timely human review.

## Pilot Roles

### Student

Uses a private student AI space to talk about school, stress, goals, confusion, support needs, and anything they are comfortable exploring.

### Parent

Uses a parent AI space to share concerns, observations, questions, and hopes. The parent does not receive raw student statements.

### Teacher / GIIS Adult

Uses teacher/admin input to record academic signals, participation changes, support observations, and school-side concerns.

### Coordinator

Synthesizes the three perspectives into privacy-safe support patterns and possible next actions.

### Human Reviewer

Reviews higher-risk outputs, validates routing, and owns Level 2 / Level 3 decisions.

v0.9 draft assignment:

- Primary reviewer: Umi, assumed education + psychology PhD
- Backup reviewer: Mahiru, assumed education + psychology PhD
- GIIS operator / parent-facing owner: Alan

## What Data Enters The Pilot

- Student AI conversation, subject to privacy wall.
- Parent AI conversation or structured parent notes.
- Teacher/admin observations.
- GIIS learning data if available:
  - grades
  - assignment completion
  - attendance/login pattern
  - teacher comments

## What Outputs Are Allowed

### Internal Reviewer Output

May include more detailed evidence refs, but should still avoid unnecessary raw quotes.

### Parent-Safe Output

May include:

- broad support themes;
- what helps;
- what not to do;
- recommended next conversation style;
- whether human review is needed.

Must not include:

- raw student words;
- secret truths;
- reconstructable private events;
- scenario-level detail;
- do-not-share details.

### Teacher-Safe Output

May include:

- classroom-relevant support patterns;
- participation / workload / planning signals;
- low-pressure support suggestions;
- escalation flags when needed.

Must not include:

- private family details;
- raw student statements;
- parent-only disclosures unless explicitly allowed.

## Support Routing Options

The coordinator may recommend one or more:

- continue monitoring;
- student self-reflection prompt;
- parent communication coaching;
- teacher support adjustment;
- GIIS human review;
- external counseling/professional referral;
- 杰尼 1-on-1 academic support;
- crisis handoff.

杰尼 should only be recommended when the evidence points to an academic support, planning, confidence, or learning-gap need that 1-on-1 tutoring can reasonably address.

## Pilot Success Metrics

### Must Pass

- 0 raw quote / raw secret leaks in parent-safe and teacher-safe outputs.
- 100% Level 3 cases receive human review.
- Student reports no feeling of betrayal after safe summary is used.
- Alan can explain the system clearly to parent and student.

### Evidence To Collect

- Did student share something useful earlier than usual?
- Did parent/teacher receive actionable guidance?
- Did reviewer agree with support routing?
- Was the recommended support reversible and proportionate?
- Did the pilot reduce confusion without increasing surveillance feeling?

## Weekly Rhythm

### Week 0: Setup

- Confirm provider path.
- Confirm Umi as primary reviewer and Mahiru as backup reviewer.
- Confirm Alan's weekly pilot time budget remains under 3 hours.
- Confirm family understands boundaries.
- Confirm opt-out and deletion procedure.

### Week 1: First Use

- Student uses AI 2-3 times.
- Parent submits 1-2 check-ins or conversations.
- Teacher/admin adds one observation.
- Coordinator produces internal + parent-safe + teacher-safe summaries.
- Human reviewer reviews before anything sensitive is shared.

### Week 2: Support Action

- Choose one small reversible support action.
- Do not force disclosure.
- Check whether student still trusts the system.
- Record reviewer note.

### Week 3: Decision

- Continue, pause, or stop pilot for this family.
- Document what worked and what felt risky.
- Do not expand to more families until review is complete.

## Stop Conditions

Pause or stop the pilot if:

- parent demands raw student conversation;
- student feels exposed or tricked;
- Level 3 process is unclear;
- AI output contains raw/reconstructable private details;
- Alan cannot review within agreed time;
- provider/data boundary is violated.

## Open Decisions Before Real Pilot

- Confirm Umi/Mahiru reviewer roles are operationally valid for the actual pilot setting.
- Confirm secure Level 3 notification mechanism.
- External professional referral rule.
- Whether any raw student conversation is stored at all.
