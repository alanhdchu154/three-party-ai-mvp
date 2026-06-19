# Literature Review: Privacy-Preserving AI Coordination for Schools and Family-Support Workflows

Last updated: 2026-06-19

## Purpose

This review grounds the Three-Party AI direction in existing research. The
project thesis is:

> Privacy-preserving AI coordination layer for schools and family-support
> workflows.

The literature supports the direction, but with an important boundary: the
current repo can claim a synthetic benchmark and reference architecture for
privacy-aware coordination. It cannot yet claim real-student disclosure behavior,
clinical validity, outcome improvement, or deployment readiness.

## Search Strategy

Searches were run across Google/web scholarly indexes and primary publisher or
institutional pages. Priority was given to peer-reviewed papers, official
reports, and framework documents from ACM, SAGE, Springer, Journal of Learning
Analytics, UNESCO, UNICEF, NIST, and U.S. Department of Education sources.

Search themes:

- contextual integrity, child privacy, and privacy literacy;
- learning analytics ethics, student privacy, and data protection;
- conversational AI / computer-mediated sensitive self-disclosure;
- multi-agent LLM privacy leakage and full-stack privacy benchmarks;
- human-AI decision support, human review, and overreliance;
- benchmark documentation, dataset documentation, and AI governance.

## Research Question

How can LLM-based systems support multi-party educational coordination while
preserving contextual privacy boundaries between students, parents, teachers,
and human reviewers?

## Synthesis

### 1. Privacy should be modeled as appropriate information flow, not simple secrecy

Nissenbaum's Contextual Integrity theory argues that privacy depends on whether
information flows fit the norms of a specific context, including sender,
recipient, information type, and transmission principle. This maps directly to
Three-Party's design: student raw disclosures may be inappropriate for parents
or teachers, while abstracted support needs may be appropriate for a human
reviewer or audience-safe report.

This literature supports the privacy-wall architecture:

```text
private chats -> abstraction -> privacy wall -> coordinator -> audience-safe reports
```

The system is not trying to block all information movement. It is trying to
make information movement context-appropriate.

**Key support**

- Nissenbaum frames privacy as contextual integrity and appropriate information
  flow rather than secrecy alone ([Privacy as Contextual Integrity](https://digitalcommons.law.uw.edu/wlr/vol79/iss1/10/)).
- Kumar et al. apply contextual integrity to children's privacy literacy and
  show that children's judgments about disclosure vary across family,
  friendship, and education contexts ([Kumar et al., 2020](https://www.cogitatiopress.com/mediaandcommunication/article/view/3236)).

**Implication for this repo**

The strongest academic framing is not "we hide everything." It is:

> We test whether an AI coordination pipeline can preserve appropriate
> information flows across student, parent, teacher, coordinator, and reviewer
> contexts.

### 2. Learning analytics already recognizes the same ethical tension, but usually lacks private-dialogue coordination

Learning analytics and early-warning systems aim to identify students needing
support. The ethical literature repeatedly raises surveillance, transparency,
power, consent, data protection, and harm-risk concerns. Three-Party sits next
to this field but addresses a different data source: private multi-party
dialogue rather than only grades, attendance, LMS logs, or engagement signals.

**Key support**

- Slade and Prinsloo argue that learning analytics ethics must account for
  power, surveillance, transparency, and context-bound student identity
  ([Slade & Prinsloo, 2013](https://journals.sagepub.com/doi/10.1177/0002764213479366)).
- Pardo and Siemens propose ethical and privacy principles for learning
  analytics, including pragmatic design principles for educational data use
  ([Pardo & Siemens, 2014](https://bera-journals.onlinelibrary.wiley.com/doi/10.1111/bjet.12152)).
- Cormack argues that ordinary consent models give institutions limited
  guidance for routine learning analytics, and proposes a data-protection
  framework focused on legitimate purpose and harm risk ([Cormack, 2016](https://learning-analytics.info/index.php/JLA/article/view/4554)).

**Implication for this repo**

Three-Party should position itself as a privacy-aware student-support
coordination benchmark, not a generic learning analytics predictor. Its novelty
is modeling what can safely move between parties when evidence comes from
private dialogue.

### 3. "AI can hear the truth" has partial support, but must be stated carefully

There is evidence that people disclose more sensitive information in
computer-mediated or virtual-agent settings than in face-to-face settings,
partly because computer-administered interactions can reduce interviewer
presence and social desirability pressure. Recent conversational AI review work
also finds that many studies report greater self-disclosure to virtual or
conversational agents than to humans or web surveys.

But the evidence is not specific enough to claim that students in real schools
will disclose to AI at high rates. The defensible claim is narrower:

> Prior research makes private AI disclosure a plausible mechanism worth
> testing, especially for sensitive or socially costly disclosures.

**Key support**

- Weisband and Kiesler's CHI meta-analysis found increased self-disclosure on
  computer forms across many measures ([Weisband & Kiesler, 1996](https://dl.acm.org/doi/10.1145/238386.238387)).
- Gnambs and Kaspar's meta-analysis found computerized self-administered surveys
  increased reporting of socially undesirable behaviors compared with comparable
  paper modes ([Gnambs & Kaspar, 2015](https://pubmed.ncbi.nlm.nih.gov/25410404/)).
- Lucas et al. found virtual humans can increase willingness to disclose and
  reduce evaluation concerns in sensitive interviews ([Lucas et al., 2014](https://dl.acm.org/doi/abs/10.1016/J.CHB.2014.04.043)).
- Lucas et al. later found active-duty service members reported more mental
  health symptoms to a virtual human interviewer than in official post-deployment
  health assessment settings ([Lucas et al., 2017](https://www.frontiersin.org/journals/robotics-and-ai/articles/10.3389/frobt.2017.00051/full)).
- Papneja and Yadav review self-disclosure to conversational AI and report that
  most evidence suggests more disclosure to virtual/conversational agents than
  to humans or web surveys, while also calling for more research
  ([Papneja & Yadav, 2025](https://link.springer.com/article/10.1007/s00779-024-01823-7)).

**Implication for this repo**

Do not write:

> Students will tell AI the truth.

Write:

> Prior self-disclosure literature suggests AI/private computer interfaces may
> reduce some social desirability barriers, making privacy-aware disclosure and
> coordination worth testing.

嗯，這個比較硬，也比較不會被 reviewer 打爆。

### 4. Multi-agent LLM systems create internal privacy channels that output-only audits miss

Three-Party is not just a chatbot. It is a multi-surface coordination system:
student AI, parent AI/input, teacher AI/input, coordinator, reports, and human
review. Recent LLM privacy work argues that multi-agent systems create privacy
risk through internal messages, shared memory, tool calls, and intermediate
traces, not only final outputs.

**Key support**

- AgentLeak introduces a full-stack benchmark for privacy leakage in
  multi-agent LLM systems and reports that internal channels can account for
  substantial leakage missed by output-only audits ([AgentLeak, 2026](https://arxiv.org/abs/2602.11510)).
- MAGPIE evaluates contextual privacy in collaborative multi-agent tasks and
  finds that agents can leak sensitive information even when explicitly
  instructed not to ([MAGPIE, 2025](https://arxiv.org/abs/2510.15186)).

**Implication for this repo**

Three-Party should evaluate more than final parent-safe / teacher-safe reports.
The baseline comparison should eventually inspect:

- raw private turns;
- abstracted profiles;
- coordinator input/output;
- audience reports;
- reviewer notes;
- logs and traces, if any exist.

The current deterministic baseline script is a first scaffold, not the complete
privacy evaluation.

### 5. Human review is necessary, but not sufficient by itself

The AIED and human-AI decision support literature supports keeping humans in the
loop for high-stakes or sensitive decisions, but it also warns against
automation bias and rubber-stamp review. Human review must be designed as an
actual decision workflow, not a decorative checkbox.

**Key support**

- UNESCO's generative AI guidance emphasizes a human-centred vision for AI in
  education and research ([UNESCO, 2023/2026 update](https://www.unesco.org/en/articles/guidance-generative-ai-education-and-research)).
- Holmes et al. argue that AIED ethics cannot be reduced to technical data
  questions; it must address social, ethical, and educational consequences
  ([Holmes et al., 2022](https://link.springer.com/article/10.1007/s40593-021-00239-1)).
- Amershi et al. provide validated human-AI interaction guidelines, including
  setting expectations, supporting correction, and designing for appropriate
  reliance ([Amershi et al., 2019](https://dl.acm.org/doi/10.1145/3290605.3300233)).
- Automation-bias literature shows that people may over-rely on decision support
  systems, especially in high-stakes settings, so reviewer workflows need
  evidence, uncertainty, and override affordances ([Goddard et al., 2012](https://pmc.ncbi.nlm.nih.gov/articles/PMC3240751/)).

**Implication for this repo**

The human reviewer annotation protocol should not only ask "is this safe?" It
should ask:

- What decision does the human own?
- What evidence supports the recommendation?
- What uncertainty remains?
- What should be withheld from parent/teacher audiences?
- Would the reviewer know when to escalate, defer, or reject the AI output?

### 6. Child-centred AI and student privacy guidance support conservative claim boundaries

Because the target domain involves minors or youth-support workflows, the
project needs stronger claim discipline than a normal productivity-agent demo.
UNICEF guidance emphasizes child rights, data privacy, safety, accountability,
and child well-being. FERPA and student privacy guidance also frame education
data as regulated and trust-sensitive.

**Key support**

- UNICEF's AI guidance for children provides requirements and recommendations
  for child-centred AI systems, including privacy, safety, transparency, and
  accountability ([UNICEF AI for Children](https://www.unicef.org/innocenti/reports/policy-guidance-ai-children)).
- UNESCO warns that AI in education brings risks that have outpaced policy and
  regulation, requiring human capacity, policy, and safeguards ([UNESCO AI in Education](https://www.unesco.org/en/digital-education/artificial-intelligence)).
- FERPA regulations set formal privacy requirements for parents and students in
  U.S. education records contexts ([U.S. Department of Education FERPA](https://studentprivacy.ed.gov/ferpa)).

**Implication for this repo**

The README and paper must continue saying:

- synthetic-only;
- no real-student validation;
- no clinical tool;
- not autonomous counseling;
- not pilot-ready without consent, deletion, reviewer ownership, and crisis
  handoff.

### 7. Benchmark documentation norms support datasheets, model cards, and explicit limitations

If this repo becomes public, the benchmark should include provenance,
composition, intended use, non-use, known limitations, and evaluation conditions.
This is directly aligned with dataset/model documentation literature and AI
governance frameworks.

**Key support**

- Datasheets for Datasets argues that datasets should be documented with
  motivation, composition, collection process, intended uses, and maintenance
  information ([Gebru et al., 2021](https://dl.acm.org/doi/10.1145/3458723)).
- Model Cards propose transparent reporting of intended uses, limitations, and
  performance characteristics ([Mitchell et al., 2019](https://dl.acm.org/doi/10.1145/3287560.3287596)).
- NIST AI RMF 1.0 frames trustworthy AI around valid/reliable, safe, secure,
  accountable, transparent, explainable/interpretable, privacy-enhanced, and
  fair systems ([NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework)).

**Implication for this repo**

Next academic support artifact should be a `docs/benchmark_datasheet.md` or
equivalent section covering:

- motivation;
- corpus composition;
- synthetic generation process;
- intended uses;
- non-uses;
- privacy risks;
- evaluation scripts;
- human-review requirements;
- known gaps.

## Evidence Matrix

| Project claim | Literature support | Strength | Safe wording |
| --- | --- | --- | --- |
| Privacy is about appropriate flows, not total secrecy | Contextual Integrity; child privacy literacy | Strong theoretical support | The system operationalizes contextual privacy through abstraction and audience-safe reports. |
| Student/parent/teacher coordination is an information-flow problem | Learning analytics ethics; student privacy; family-school communication practice | Moderate support | The project models asymmetric information and role-specific privacy boundaries. |
| AI may elicit sensitive disclosure | Computer-mediated disclosure; virtual interviewer studies; conversational AI review | Moderate, not student-specific | AI/private interfaces may reduce some social-desirability barriers and should be studied carefully. |
| Multi-agent systems need full-stack privacy audits | AgentLeak; MAGPIE; emerging agent privacy benchmarks | Emerging but directly relevant | Output-only leak audits are insufficient; coordination pipelines need internal-channel checks. |
| Human reviewer gate is necessary | AIED ethics; human-AI interaction; automation bias literature | Strong cautionary support | AI should support, not replace, accountable human review. Reviewer workflows need evidence and override paths. |
| Synthetic benchmark is legitimate but limited | Dataset documentation and benchmark governance literature | Strong support for transparency, not validity | Synthetic data is a controlled stress test, not evidence of real student behavior. |

## Gap Analysis

### Gap 1: Real-student disclosure behavior

The self-disclosure literature supports the mechanism, but not the exact school
setting. Three-Party needs real pilot evidence, or at minimum human expert
annotation, before claiming that students would disclose in this product.

### Gap 2: Multi-party educational privacy benchmarks

Agent privacy benchmarks exist, and learning analytics ethics exists, but there
appears to be a gap around synthetic benchmarks specifically for
student-parent-teacher privacy-preserving coordination. This is a possible
research contribution.

### Gap 3: Human reviewer annotation design

The field supports human oversight, but human review can become rubber-stamping.
Three-Party should make reviewer annotation a first-class artifact with verdicts,
evidence references, uncertainty, and escalation ownership.

### Gap 4: Cultural and family-system specificity

The current synthetic corpus includes Chinese-family cultural dynamics, but the
literature review here is mostly Western/English-language. If the paper leans
into Chinese family/school contexts, it needs additional bilingual literature on
family communication, academic pressure, filial norms, and youth mental health.

## Recommended Paper Framing

Use this as the academically grounded contribution:

> We formulate multi-party student support as a contextual privacy problem:
> support-relevant information should sometimes move across parties, but raw
> disclosures and reconstructable private details should not. We introduce a
> synthetic benchmark and reference architecture for testing whether LLM-based
> coordination systems can abstract private dialogue into audience-safe,
> human-reviewable support reports.

Avoid:

> AI hears the truth from students and solves school-family communication.

Better:

> Prior self-disclosure research suggests private AI interfaces may reduce some
> barriers to sensitive disclosure. This motivates a privacy-preserving
> coordination benchmark, but does not establish real-world disclosure rates.

## Working Bibliography

- Amershi, S., Weld, D., Vorvoreanu, M., Fourney, A., Nushi, B., Collisson, P.,
  Suh, J., Iqbal, S., Bennett, P. N., Inkpen, K., Teevan, J., Kikin-Gil, R., &
  Horvitz, E. (2019). Guidelines for human-AI interaction. *CHI 2019*.
  https://doi.org/10.1145/3290605.3300233
- Cormack, A. N. (2016). A data protection framework for learning analytics.
  *Journal of Learning Analytics, 3*(1), 91-106.
  https://doi.org/10.18608/jla.2016.31.6
- Gebru, T., Morgenstern, J., Vecchione, B., Vaughan, J. W., Wallach, H.,
  Daume III, H., & Crawford, K. (2021). Datasheets for datasets.
  *Communications of the ACM, 64*(12), 86-92.
  https://doi.org/10.1145/3458723
- Gnambs, T., & Kaspar, K. (2015). Disclosure of sensitive behaviors across
  self-administered survey modes: A meta-analysis. *Behavior Research Methods,
  47*, 1237-1259. https://doi.org/10.3758/s13428-014-0533-4
- Goddard, K., Roudsari, A., & Wyatt, J. C. (2012). Automation bias: A
  systematic review of frequency, effect mediators, and mitigators. *Journal of
  the American Medical Informatics Association, 19*(1), 121-127.
  https://pmc.ncbi.nlm.nih.gov/articles/PMC3240751/
- Holmes, W., Porayska-Pomsta, K., Holstein, K., Sutherland, E., Baker, T.,
  Shum, S. B., Santos, O. C., Rodrigo, M. T., Cukurova, M., Bittencourt, I. I.,
  & Koedinger, K. R. (2022). Ethics of AI in education: Towards a
  community-wide framework. *International Journal of Artificial Intelligence in
  Education, 32*, 504-526. https://doi.org/10.1007/s40593-021-00239-1
- Kumar, P. C., Subramaniam, M., Vitak, J., Clegg, T. L., & Chetty, M. (2020).
  Strengthening children's privacy literacy through contextual integrity.
  *Media and Communication, 8*(4), 175-184.
  https://doi.org/10.17645/mac.v8i4.3236
- Lucas, G. M., Gratch, J., King, A., & Morency, L.-P. (2014). It's only a
  computer: Virtual humans increase willingness to disclose. *Computers in
  Human Behavior, 37*, 94-100. https://doi.org/10.1016/j.chb.2014.04.043
- Lucas, G. M., Rizzo, A., Gratch, J., Scherer, S., Stratou, G., Boberg, J., &
  Morency, L.-P. (2017). Reporting mental health symptoms: Breaking down
  barriers to care with virtual human interviewers. *Frontiers in Robotics and
  AI, 4*, 51. https://doi.org/10.3389/frobt.2017.00051
- Mitchell, M., Wu, S., Zaldivar, A., Barnes, P., Vasserman, L., Hutchinson, B.,
  Spitzer, E., Raji, I. D., & Gebru, T. (2019). Model cards for model
  reporting. *FAT* 2019*. https://doi.org/10.1145/3287560.3287596
- Nissenbaum, H. (2004). Privacy as contextual integrity. *Washington Law
  Review, 79*(1), 119-157.
  https://digitalcommons.law.uw.edu/wlr/vol79/iss1/10/
- Papneja, H., & Yadav, N. (2025). Self-disclosure to conversational AI: A
  literature review, emergent framework, and directions for future research.
  *Personal and Ubiquitous Computing, 29*, 119-151.
  https://doi.org/10.1007/s00779-024-01823-7
- Pardo, A., & Siemens, G. (2014). Ethical and privacy principles for learning
  analytics. *British Journal of Educational Technology, 45*(3), 438-450.
  https://doi.org/10.1111/bjet.12152
- Slade, S., & Prinsloo, P. (2013). Learning analytics: Ethical issues and
  dilemmas. *American Behavioral Scientist, 57*(10), 1509-1528.
  https://doi.org/10.1177/0002764213479366
- UNESCO. (2023, updated 2026). *Guidance for generative AI in education and
  research*. https://www.unesco.org/en/articles/guidance-generative-ai-education-and-research
- UNICEF Innocenti. (2025). *Guidance on AI and children*.
  https://www.unicef.org/innocenti/reports/policy-guidance-ai-children
- U.S. Department of Education. (n.d.). *Family Educational Rights and Privacy
  Act (FERPA)*. https://studentprivacy.ed.gov/ferpa
- NIST. (2023). *Artificial Intelligence Risk Management Framework (AI RMF
  1.0)*. https://www.nist.gov/itl/ai-risk-management-framework
- El Yagoubi, F., Al Mallah, R., & Badu-Marfo, G. (2026). AgentLeak: A
  full-stack benchmark for privacy leakage in multi-agent LLM systems.
  *arXiv*. https://arxiv.org/abs/2602.11510
- Juneja, G., Pasupulati, J. N. S., Albalak, A., Hua, W., & Wang, W. Y. (2025).
  MAGPIE: A benchmark for multi-agent contextual privacy evaluation. *arXiv*.
  https://arxiv.org/abs/2510.15186

## Limitations of This Review

- This is a targeted narrative literature review, not a PRISMA systematic
  review.
- Search was English-first. Chinese-language education/family literature is not
  yet covered.
- Some agent-privacy sources are recent preprints and should be treated as
  emerging evidence.
- The review supports the research direction and claim boundaries; it does not
  validate this implementation's real-world performance.
