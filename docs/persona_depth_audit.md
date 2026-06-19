# Persona Depth Audit

Last updated: 2026-06-19

## Question

Are the current personas and family relationships deep enough for a public
GitHub-facing synthetic benchmark?

Short answer: yes for Evidence v1, with a clear boundary. The corpus has enough
persona and relationship depth to support a synthetic benchmark and reference
architecture. It is not enough to claim real-student validity, clinical
validity, or deployment readiness.

## Fresh Corpus Check

Command:

```bash
python3 scripts/audit_conversation_quality.py --json
```

Current corpus snapshot:

- conversations: 348
- deep: 85
- medium: 121
- shallow: 142
- personas:
  - alan_teacher: 38
  - keer: 38
  - michael: 37
  - michael_mom: 39
  - rachel: 39
  - shen_mom: 39
  - shen_you: 39
  - stepdad: 40
  - uncle: 39
- audit warnings: none

## Audit Dimensions

| Dimension | What It Checks | Current Status |
|---|---|---|
| Distinct voice | Does the persona sound different across cases? | Mostly yes. Student and family personas have recognizable surfaces. Alan Teacher is intentionally more functional. |
| Cross-scenario continuity | Does the same inner motive recur across shallow, medium, and deep cases? | Yes for Michael, Keer, Shen You, Rachel, Shen Mom, Uncle. Adequate for Michael Mom and Stepdad. Utility-level for Alan Teacher. |
| Relational motive | Is the problem relational, not just a symptom tag? | Yes. Strongest in Rachel-Uncle, Shen You-Shen Mom, and the Michael-Keer-Mom-Stepdad blended family. |
| Misread risk | Can another party plausibly misunderstand the case? | Yes. The corpus includes cheerful-child, lazy-student, high-achiever, practical-parent, and protective-elder traps. |
| Privacy-probe surface | Could an adult misuse the system to infer raw private disclosure? | Yes, especially through Shen Mom, Michael Mom, and Uncle-style authority pressure. |
| Safe-report risk | Could a report be useful but unsafe? | Yes. This is the core reason the benchmark needs parent-safe, teacher-safe, and internal-reviewer surfaces. |

## Per-Persona Depth Table

| Persona | Current Depth | Main Risk | Next Improvement |
|---|---|---|---|
| Michael | Strong enough for benchmark. Conditional belonging and fairness-as-distance recur across cases. | Reports may flatten him into academic pressure. | Keep examples that show school issues are downstream of family belonging, not separate from it. |
| Keer | Strong enough for benchmark. Warmth, performance, sibling ambiguity, and atmosphere-management are visible. | May be misread as simply cheerful or low-risk. | Add future cases only if they stress guilt, comparison, or being the "easy" child. |
| Shen You | Strong enough for benchmark. Private space, indirect monitoring, and adult-script resistance are clear. | May be reduced to laziness or game avoidance. | Preserve unsynced-private-space as the core motive in future reports and samples. |
| Rachel | Strong enough for benchmark. Quiet autonomy conflict and writing-as-inner-life are consistent. | Authority pressure may be over-normalized as family care. | Use Rachel cases for privacy-probe and governance-pressure evaluation. |
| Michael Mom | Adequate. Ranking anxiety and loss of access to child are visible. | Can become a generic anxious parent if detached from face/status context. | Future cases should tie monitoring requests to social face and maternal access. |
| Shen Mom | Strong. Parent need for control, proof, and mediated knowledge creates Level 3 privacy risk. | Parent support can turn into surveillance if outputs are too revealing. | Keep her as a primary misuse/boundary-test persona. |
| Stepdad | Adequate. Fairness-as-distance and business-like care are visible. | Could be flattened into responsible adult or cold stepfather. | Future cases should keep both positive pockets and emotional distance. |
| Uncle | Strong. Governance, authority, family planning, and autonomy pressure create Level 3 risk. | Protective language can conceal privacy probing. | Use Uncle cases for authority-framed privacy probes. |
| Alan Teacher | Utility-level by design. Useful for school reports and coordination context. | Too thin if the benchmark later claims teacher-persona realism. | Add distinct teacher archetypes only if teacher-side evaluation becomes a core claim. |

## Conclusion

The current persona layer is deep enough for the repo's present public claim:

> a synthetic benchmark and reference architecture for privacy-preserving
> multi-party AI coordination.

It is not enough for claims about real families, school deployment, clinical
validity, or measured outcomes. That boundary is healthy. The technical asset is
the coordination and privacy-wall evaluation, not a claim that the synthetic
families are representative.

## Recommendation

Do not restart synthetic generation just to add more persona depth.

The better next step is to use `docs/persona_bible.md` and
`docs/relationship_graph.md` as constraints:

- every future generated case should name the persona motive and relationship
  edge it stresses;
- fixed benchmark samples should include at least one Level 3 relationship
  system and one subtle Level 2 blended-family case;
- reviewer annotations should flag not only raw quote leaks, but also
  reconstructable relationship leaks;
- future public writeups should treat persona depth as benchmark design, not
  real-world validation.
