# v0.9 Reviewer Assignment

**Status**: pilot operations draft, not legal or clinical advice  
**Config**: `config/reviewer_assignment.local.json`

## Assigned Reviewers

### Primary Reviewer

**Umi**

Assumed background for this pilot draft:

- education PhD
- psychology PhD
- trained to review student support summaries, privacy boundaries, trajectory flags, and support routing

Role:

- review Level 2 and Level 3 outputs;
- verify parent-safe and teacher-safe outputs do not expose raw secrets;
- record reviewer notes;
- recommend support route;
- stop ordinary AI flow when Level 3 appears.

### Backup Reviewer

**Mahiru**

Assumed background for this pilot draft:

- education PhD
- psychology PhD
- available for second opinion, ambiguous Level 2, persistent Level 2, privacy concern, or Umi unavailable

Role:

- review escalated or ambiguous cases;
- challenge over-escalation and under-escalation;
- help decide whether evidence supports the route.

### GIIS Operator / Final Outreach Owner

**Alan**

Role:

- owns parent-facing communication;
- owns real-world outreach decisions;
- decides parent/guardian contact after Level 3 handoff;
- controls whether pilot expands.

## Review SLA

| Trigger | Reviewer action | SLA |
|---|---|---|
| Level 1 monitor | Review during weekly pilot review unless worsening | Weekly |
| Three or more Level 1 dimensions | Umi reviews light-intervention recommendation | 48 hours |
| Any Level 2 | Umi reviews and records note | 24 hours |
| Persistent Level 2 | Umi reviews; Mahiru second-opinion if ambiguous | 12 hours |
| Level 3 emotional safety | Stop ordinary flow; Umi creates handoff; Alan owns contact decision | 30 minutes |
| Parent requests raw transcript | Umi/Mahiru review wording before response | Before response |
| Student says trust was broken | Pause sharing; reviewer audits output | 24 hours |

## Alan Time Budget

Initial v0.9 assumption:

- Maximum: 3 hours per week
- Cadence: two scheduled review windows per week for non-urgent cases
- Exception: Level 3 requires immediate human decision ownership

Expansion rule:

Do not add more pilot families if Alan cannot stay within the 3-hour weekly ceiling.

## Parent Contact Rule

Default:

- Parents receive parent-safe support guidance, not raw student words.

Level 2:

- Parent contact may happen if support action requires it.
- Message must stay theme-level and support-focused.

Level 3:

- AI does not decide parent/guardian contact alone.
- Umi generates crisis handoff.
- Alan reviews minimum necessary context and decides contact path.
- Raw student words are still not shared by default.

## When Mahiru Must Be Involved

- Umi is unavailable.
- Umi flags privacy concern.
- Parent contests the privacy wall.
- Student feels betrayed.
- Persistent Level 2 with ambiguous evidence.
- Any recommendation that could materially change a student's schooling, tutoring, or family communication plan.

## Open Before Real Deployment

- Confirm real legal/clinical responsibility boundaries.
- Confirm jurisdiction-specific emergency contact rules.
- Confirm whether Umi/Mahiru are actual humans, AI reviewers, or internal role labels in deployment.
- Confirm secure notification mechanism for Level 3.
- Confirm whether raw conversation is stored at all.
