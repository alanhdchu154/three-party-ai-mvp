# Data Rights, Opt-Out, and Deletion Procedure

**Status**: v0.9 operational draft, not legal advice

## Principles

- Participation is voluntary.
- Raw private disclosures should be minimized.
- Parent-safe and teacher-safe outputs must not reveal raw secrets.
- Families can stop participating.
- Deletion must be operationally possible before pilot begins.

## Consent Baseline

Before a family joins, Alan/GIIS should confirm that:

- parent understands the purpose and limits of the pilot;
- student understands that raw words are protected from ordinary parent/teacher views;
- both understand that serious safety concerns may trigger human review;
- both know how to pause or stop participation;
- both know what data may be stored.

## Data Categories

### Raw Conversation

Highest sensitivity.

Default pilot posture:

- avoid long-term storage if possible;
- if stored, restrict to authorized reviewer only;
- never show raw conversation to parent/teacher/tutor by default.

### Abstracted Profile

Medium to high sensitivity.

Contains:

- support needs;
- risk dimensions;
- do-not-share boundaries;
- privacy-safe summaries.

### Audience-Safe Reports

Lower sensitivity but still confidential.

Types:

- internal reviewer;
- parent-safe;
- teacher-safe.

### Audit Metadata

Operational metadata.

Contains:

- timestamps;
- run ids;
- artifact paths;
- event types.

Should not contain raw secrets.

## Opt-Out Procedure

If a student or parent opts out:

1. Pause new AI collection for that family.
2. Confirm whether they want:
   - stop only;
   - delete pilot artifacts;
   - preserve minimal audit metadata;
   - export parent-safe summary before deletion.
3. Mark family as opted out in pilot notes.
4. Do not use their data in demo or external examples.
5. Do not include their case in future benchmark material without separate explicit consent.

## Deletion Procedure

For file-based v0.9:

1. Identify student/family id.
2. Locate related files:
   - `data/student_profiles/`
   - `data/pilot_runs/`
   - `data/reviewer_notes/`
   - `data/reviewer_summaries/`
   - future raw conversation storage, if any
3. Archive minimal deletion log:
   - deletion request timestamp;
   - operator;
   - categories deleted;
   - categories retained and why.
4. Delete or archive according to family request and safety/legal requirements.
5. Confirm deletion completion to the family.

## Retention Defaults

Recommended for first pilot:

- raw conversation: no long-term storage unless explicitly needed for safety review;
- profile: retain during active pilot only;
- parent/teacher safe report: retain during active pilot only;
- audit metadata: retain minimal metadata without raw contents;
- reviewer notes: retain sanitized notes only.

## Special Case: Safety Concern

If Level 3 or crisis handoff is triggered, do not immediately delete data needed for human safety review.

Instead:

- pause ordinary processing;
- restrict access;
- generate handoff packet;
- let human reviewer decide minimum necessary retention.

## What Families Can Be Promised

Safe promises:

- You can stop participating.
- We will not show raw student words to parent/teacher outputs.
- We will minimize stored sensitive data.
- We can delete pilot artifacts unless safety/legal review requires limited retention.

Unsafe promises:

- Everything is always confidential.
- Nothing will ever be reviewed by a human.
- We can delete all records in every circumstance.
- Parents can access all child conversations.
