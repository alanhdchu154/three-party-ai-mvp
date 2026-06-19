# Privacy Walls for Multi-Party Educational AI: A Synthetic Benchmark and Reference Architecture

Draft version: 2026-06-14 v0.1
Recommended framing: HCI/CSCW or responsible-AI workshop paper
Status: complete initial draft, not submission-ready

## Abstract

Students, parents, and teachers often hold different, incomplete, or conflicting
information about a student's needs. LLM-based educational support tools may
help coordinate these perspectives, but they also create privacy risks when raw
disclosures or reconstructable details flow between parties. We present a
synthetic benchmark and reference architecture for privacy-preserving
multi-party student support coordination. The benchmark contains synthetic
student, parent, and teacher conversations across shallow, medium, and deep
disclosure depths, including daily-life requests, misuse attempts, privacy
probes, and support-risk scenarios. The reference architecture separates private
dialogue, abstraction, privacy-wall auditing, coordinator synthesis, triage
guardrails, audience-safe reporting, and human review. In a preliminary
348-conversation snapshot, the corpus reached 40.8% shallow, 34.8% medium, and
24.4% deep conversations; generated parent-safe and teacher-safe reports passed
a deterministic leak audit with 18/18 reports passing and 0 failures. A fixed
11-case raw-coordinator baseline comparison found reconstructability risk in
11/11 raw-baseline cases and 0/11 privacy-wall cases under deterministic
checks. A reviewer annotation pass covers 37 notes over 22 artifacts. We do not claim
that synthetic dialogues represent real student behavior. Instead, we use them
as a controlled testbed for identifying privacy and coordination failures before
any real-world deployment involving minors.

## 1. Introduction

Educational support is rarely a single-user problem. A student may privately
express uncertainty, stress, or distrust; a parent may interpret the same
pattern as discipline, motivation, or academic performance; a teacher may only
observe classroom behavior. When support systems use AI to coordinate these
perspectives, they face a difficult privacy problem: the system may need to
translate support-relevant patterns across parties without exposing the raw
words, private constraints, or reconstructable events that made those patterns
visible.

This problem is not well captured by standard AI tutoring or learning analytics
systems. Many student-success systems focus on grades, attendance, engagement,
or early-warning signals. These are important, but they do not directly model
the privacy boundary between a student's private disclosure, a parent's concern,
and a teacher's classroom observation. Nor do they define what an AI coordinator
should be allowed to say to each party when it has access to asymmetric
information.

We frame this as a contextual privacy and coordination problem. Privacy does not
mean that no information can move. It means that information must move in a way
that is appropriate for its context, recipient, purpose, and transmission
principle. In student support, a raw disclosure may be inappropriate to share
with a parent or teacher, while an abstract support need may be appropriate to
share if it helps adults respond safely.

Studying this directly with real minors would be ethically and operationally
risky. We therefore build a synthetic benchmark and reference architecture. The
benchmark is not intended to represent real student behavior. It is a stress
test for system behavior: whether a pipeline leaks raw disclosures, makes
reconstructable reports, over-escalates ordinary conversations, under-escalates
high-risk synthetic cases, or produces recommendations without evidence.

This paper makes four contributions:

1. We formulate multi-party student support coordination as a privacy-preserving
   information-flow problem.
2. We introduce a synthetic benchmark with student, parent, and teacher
   perspectives across shallow, medium, and deep conversation depths.
3. We present a reference architecture separating private chats, abstraction,
   privacy-wall auditing, coordinator synthesis, triage guardrails,
   party-aware reporting, and human review.
4. We define an evaluation protocol for leakage, reconstructability,
   over-escalation, under-escalation, evidence discipline, and reviewer
   actionability.

## 2. Related Work

### 2.1 Contextual Privacy

The theoretical basis for this project is contextual privacy. Nissenbaum's
Contextual Integrity framework argues that privacy is not merely secrecy or
control, but the appropriateness of information flows within a social context
and its governing norms. This is a natural fit for multi-party student support:
the core question is not whether support-relevant information can ever move,
but what should move, to whom, at what level of abstraction, and for what
purpose.

Children's privacy literacy research has also used contextual integrity to show
that children reason about information disclosure differently across contexts.
This supports the idea that educational AI systems should not treat all student
information as equally shareable simply because it exists in a system.

### 2.2 LLM Privacy and Multi-Agent Leakage

Recent work on LLM privacy leakage, including multi-agent benchmarks such as
AgentLeak, shows that privacy risks do not occur only in final user-facing
outputs. Sensitive information may leak through inter-agent messages, shared
memory, tool arguments, or intermediate traces. Our setting differs in domain
and purpose, but shares the same concern: a coordinator architecture can reduce
some final-output leakage while creating new internal pathways for sensitive
information to move.

This motivates privacy-wall evaluation across the full pipeline: raw
conversations, abstracted profiles, protected terms, coordinator outputs, and
audience-specific reports.

### 2.3 Learning Analytics and Student Support

Learning analytics and early-warning systems have long sought to identify
students who may need support. However, these systems often rely on behavioral
or academic traces such as engagement, grades, attendance, and learning
management system activity. Privacy scholarship in learning analytics has
argued that these systems blur boundaries between educational assessment and
broader information about students' lives.

Our project is adjacent but distinct. It does not aim to predict learning
outcomes from institutional data. Instead, it tests whether a coordination
pipeline can turn private, multi-party dialogue into safe, evidence-grounded,
human-reviewable support guidance.

### 2.4 Synthetic Dialogue Benchmarks

Synthetic dialogue generation is increasingly used to create controlled test
sets for language systems. The benefit is coverage: designers can construct
rare, sensitive, adversarial, or high-risk cases that would be costly or
unethical to collect from real users. The limitation is validity: generated
dialogue may reflect model biases, author assumptions, and over-coherent
narrative structure.

We treat synthetic data as a wind tunnel, not as a population sample. It can
test how the system behaves under designed privacy and coordination pressures.
It cannot show how real students, parents, or teachers would behave.

## 3. Benchmark Design

The benchmark models a multi-party educational support setting with private
student, parent, and teacher conversations. Each party may reveal information
that is useful for coordination but unsafe or inappropriate to transmit
verbatim to another party.

### 3.1 Roles

The benchmark includes:

- Student personas, who may discuss ordinary tasks, academic concerns, family
  pressure, social dynamics, identity concerns, or private distress.
- Parent personas, who may express concern, confusion, pressure, guilt, or
  logistical needs.
- Teacher personas, who may observe classroom changes, academic performance,
  participation, or coordination issues.
- A coordinator, which consumes abstracted profiles rather than raw
  conversations.
- A reviewer role, which evaluates privacy, escalation, and recommendation
  quality.

### 3.2 Conversation Depth

Each conversation is labeled with one of three depth levels:

- `shallow`: ordinary daily-life or task-oriented interaction, such as homework
  help, logistics, off-topic chat, testing AI boundaries, or misuse attempts.
- `medium`: moderate concern or partial disclosure, such as academic stress,
  friend conflict, family friction, or a small crack in coping.
- `deep`: high-salience disclosure, privacy probe, or multi-turn emotional arc.

Depth balance matters because a corpus dominated by deep conversations rewards
systems that treat every interaction as a crisis. The current snapshot contains
348 conversations: 142 shallow (40.8%), 121 medium (34.8%), and 85 deep
(24.4%).

### 3.3 Scenario Types

Scenario types include mundane help, quick venting, logistics, parent
logistics, off-topic conversation, testing whether the AI will disclose
information, misuse attempts, moderate issues, mixed cases, privacy probes,
privacy tests, stress tests, and deep arcs. This diversity is intended to test
whether the pipeline can distinguish routine support from escalation-worthy
signals.

### 3.4 Derived Artifacts

The benchmark produces derived artifacts:

- dimension scores,
- analysis reports,
- case summaries,
- internal reviewer reports,
- parent-safe reports,
- teacher-safe reports,
- trajectory reports.

These artifacts are not ground truth about real people. They are structured
synthetic evidence for evaluating pipeline behavior.

## 4. Reference Architecture

The system is organized around a privacy wall.

1. **Private party conversation**: each party interacts with its own AI surface.
2. **Abstraction**: raw turns are converted into abstract profiles.
3. **Privacy audit**: profiles and outputs are checked for raw quote, entity,
   event, numeric, paraphrase, and reconstructability leakage.
4. **Party profiles**: student, parent, and teacher profiles represent needs,
   concerns, constraints, blind spots, and shareable support signals.
5. **Coordinator**: synthesizes profiles into a support plan without seeing or
   exposing raw conversations.
6. **Triage guardrails**: deterministic rules prevent high-risk synthetic
   safety flags from being downgraded by the LLM.
7. **Party-aware reports**: internal, parent-safe, and teacher-safe reports
   expose different levels of detail according to privacy boundaries.
8. **Human reviewer gate**: reviewer workflows are intended to decide whether
   system outputs are safe, useful, over-escalated, under-escalated, or
   under-evidenced.

The design treats AI as decision support, not as an autonomous counselor or
crisis responder.

## 5. Evaluation Method

We evaluate the benchmark and pipeline using five research questions.

**RQ1: Privacy leakage.** Does the privacy-wall pipeline avoid raw quote,
entity, event, numeric, paraphrase, and reconstructability leakage in
audience-safe reports?

**RQ2: Over-escalation.** Does the system avoid treating shallow daily-life
conversations as high-risk support cases?

**RQ3: Under-escalation.** Does the system preserve high-risk synthetic
escalation signals rather than allowing coordinator outputs to downgrade them?

**RQ4: Evidence discipline.** Are recommendations linked to evidence
references, or do reports make recommendations stronger than the available
evidence supports?

**RQ5: Human-reviewability.** Can a reviewer inspect the generated artifacts and
understand what is known, inferred, protected, justified, not yet justified, and
missing?

### 5.1 Metrics

Privacy metrics include raw quote leakage rate, entity leakage rate, event
leakage rate, numeric leakage, paraphrase leakage, reconstructability score,
and cross-party forbidden-field leakage.

Triage metrics include shallow false escalation, medium monitor/review routing,
deep under-escalation, Level 3 urgent-review recall, and deterministic
guardrail downgrade rate.

Reporting metrics include evidence-reference completeness, recommendation
without evidence, audience-safe leak rate, actionability, and reviewer
usefulness.

Corpus metrics include depth distribution, scenario diversity, average turns,
missing labels, duplicate IDs, and per-persona coverage.

### 5.2 Current Snapshot Procedure

For the current preliminary snapshot, we ran:

```bash
python3 scripts/audit_conversation_quality.py
.venv/bin/python scripts/generate_case_summaries.py
.venv/bin/python scripts/generate_audience_reports.py
.venv/bin/python scripts/generate_trajectory_reports.py
.venv/bin/python scripts/audit_audience_report_leaks.py --json umi/reports/audience-report-leak-audit-latest.json
.venv/bin/python scripts/run_baseline_comparison.py
.venv/bin/python scripts/generate_reviewer_summary.py
.venv/bin/python -m pytest -q
```

## 6. Preliminary Results

The current snapshot contains 348 synthetic conversations across 9 personas.
The corpus has no missing depth labels, no missing scenario type labels, and no
duplicate conversation IDs. It contains 142 shallow conversations (40.8%), 121
medium conversations (34.8%), and 85 deep conversations (24.4%), with an average
of 19.5 turns per conversation.

| Depth | Count | Share |
|---|---:|---:|
| shallow | 142 | 40.8% |
| medium | 121 | 34.8% |
| deep | 85 | 24.4% |

The report pipeline generated 9 case summaries, 27 audience reports, and 9
trajectory reports. The audience-safe leak audit checked 18 parent-safe and
teacher-safe reports and found 0 deterministic failures.

| Surface | Reports checked | Failures |
|---|---:|---:|
| parent_safe | 9 | 0 |
| teacher_safe | 9 | 0 |
| total | 18 | 0 |

The raw-coordinator baseline comparison sampled 11 fixed cases: 3 shallow, 3
medium, 3 deep, 1 privacy probe, and 1 misuse/boundary case. The raw baseline
showed reconstructability risk in 11/11 cases. The privacy-wall pipeline showed
0/11 reconstructability-risk cases, 0 over-escalation flags, 0
under-escalation flags, and 0 recommendation-without-evidence flags under the
current deterministic heuristic.

| Metric | Raw baseline | Privacy-wall pipeline |
|---|---:|---:|
| reconstructability risk cases | 11 | 0 |
| over-escalation flags | 0 | 0 |
| under-escalation flags | 3 | 0 |
| recommendation without evidence flags | 2 | 0 |

The reviewer annotation pass covers 37 notes over 22 reviewed artifacts: 12
baseline artifacts, 3 audience-report artifacts, and 7 legacy calibration
artifacts. Current new-style reviewer verdicts include 26 `safe`, 3
`privacy_concern`, and 2 `minor_issue`, alongside legacy calibration verdicts.
The raw baseline is marked as a privacy concern; parent-safe and teacher-safe
reports for the sampled Michael case are marked safe; the internal reviewer
report is marked minor issue because restricted reviewer content should not be
reused as parent-safe or teacher-safe output.

Reviewer identity boundary: `Umi` is an AI-assisted internal reviewer label,
and `ReviewerB` is a local second-reviewer label seeded for screening coverage.
These labels do not represent external independent human validation. This
reviewer evidence should be treated as internal screening until external
reviewers complete and record review.

The full test suite passed with 89 tests passing and 7 skipped. These results
support a preliminary claim that the current privacy-wall reporting pipeline
passed deterministic screening checks and internal reviewer annotation on the
frozen synthetic snapshot.

They do not support claims about real-world validity, clinical validity,
deployment readiness, outcome improvement, or behavior by real students,
parents, or teachers.

## 7. Discussion

The benchmark highlights a useful distinction between disclosure and
translation. A system can preserve privacy not by refusing to move all
information, but by translating raw disclosures into abstract support needs
with audience-specific constraints. This is especially important in educational
contexts involving minors, where parents and teachers may have legitimate
support roles but not unlimited entitlement to raw private disclosures.

The current corpus balance also matters. Earlier versions of the corpus were
deep-heavy, which risked over-pathologizing ordinary interactions. The current
snapshot is closer to the target depth distribution, enabling tests for shallow
false escalation and medium-case ambiguity.

The architecture also shows why final-output audits are insufficient. Sensitive
information can appear in intermediate profiles, coordinator prompts, reviewer
notes, or internal summaries. A privacy-wall evaluation must therefore inspect
multiple stages of the pipeline, not only the final parent-facing or
teacher-facing report.

## 8. Limitations

This work is synthetic-only. The conversations are generated or authored, not
collected from real students, parents, or teachers. We therefore cannot infer
real disclosure rates, real family dynamics, real teacher behavior, or real
student outcomes.

There is also a risk of circularity. LLMs and prompts may be involved in
generation, abstraction, and evaluation. Deterministic audits and first-pass
reviewer annotation reduce this risk but do not eliminate it. Future work should
include a second independent reviewer pass, stronger semantic privacy checks,
runtime trace audits, and, if ethically approved, carefully scoped real-world
usability work.

Finally, this system is not a clinical tool. It should not be used for
autonomous counseling, diagnosis, or crisis response. Any real deployment with
minors would require consent, deletion rights, reviewer ownership, provider/data
controls, and crisis handoff procedures.

## 9. Ethics and Safety

The benchmark intentionally avoids real minors' data. This lowers immediate
privacy risk while allowing adversarial privacy and coordination tests. However,
synthetic data can still encode stereotypes and misleading assumptions, so the
paper must not present synthetic behavior as real-world evidence.

The system's intended role is human-led decision support. Parent-safe and
teacher-safe reports are designed to prevent surveillance framing: they should
not let adults ask the AI for hidden details, interrogate the student, or infer
specific private events. Internal reviewer reports may include more structure,
but should still avoid unnecessary raw-detail reproduction.

## 10. Conclusion

We presented a synthetic benchmark and reference architecture for
privacy-preserving multi-party student support coordination. The work frames
educational AI not as autonomous counseling, but as a privacy-sensitive
coordination problem involving asymmetric information across students, parents,
teachers, and human reviewers. Preliminary results on a 348-conversation
synthetic snapshot show that the current privacy-wall reporting pipeline
generates audience-safe reports with no deterministic leak-audit failures and
improves over a raw-coordinator baseline on deterministic reconstructability
checks. An internal reviewer annotation pass adds reviewer judgment over baseline and
report artifacts. The main contribution is a testbed and evaluation protocol
for identifying privacy, triage, and coordination failures before real-world
deployment.

## References and Anchors

- Helen Nissenbaum, "Privacy as Contextual Integrity." Washington Law Review,
  2004. https://digitalcommons.law.uw.edu/wlr/vol79/iss1/10/
- Helen Nissenbaum et al., "Privacy and Contextual Integrity: Framework and
  Applications." https://nissenbaum.tech.cornell.edu/papers/Privacy%20and%20Contextual%20Integrity%20-%20Frameworks%20and%20Applications.pdf
- Priya Kumar et al., "Strengthening Children's Privacy Literacy through
  Contextual Integrity." https://www.cogitatiopress.com/mediaandcommunication/article/view/3236
- El Yagoubi et al., "AgentLeak: A Full-Stack Benchmark for Privacy Leakage in
  Multi-Agent LLM Systems." https://arxiv.org/abs/2602.11510
- Rubel and Jones, "Student Privacy in Learning Analytics." https://philarchive.org/rec/RUBSPI-3
- "Synthetic Dialogue Data Generation: A Comprehensive Survey." https://www.cfilt.iitb.ac.in/resources/surveys/2025/synthetic-dialog-data-generation-survey-anshul.pdf
- "Evaluating Synthetic Data Generation from User Generated Text." Computational
  Linguistics. https://direct.mit.edu/coli/article/51/1/191/124625/Evaluating-Synthetic-Data-Generation-from-User
