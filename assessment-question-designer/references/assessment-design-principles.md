# Assessment Design Principles

## Source-grounded design

Start with the source concept, not with a clever question. The answer must be entailed by the source
in SOURCE-GROUNDED mode. A distractor may model a plausible reading error, but must not require an
unstated external fact to be rejected. If outside knowledge is intentional, label the item accordingly.

## Internal question blueprint

Before drafting options, record as much of this as the item needs:

```yaml
id: Q-001
source_concept: "the boundary being tested"
learning_objective: "what the learner should demonstrate"
cognitive_level: 3
difficulty_level: 3
question_type: MCQ4
stem: "the question"
correct_proposition: "the proposition that answers it"
correct_option: B
options:
  - label: A
    text: "..."
    is_correct: false
    misconception: "..."
source_evidence: "source section or quotation reference"
rationale: "why the correct proposition follows"
ambiguity_check: pass
```

The blueprint is an authoring control, not automatically student-facing output. Keep one primary
construct per item so a wrong answer is diagnostically meaningful. A scenario may combine principles
only when the requested difficulty and learning objective require that reasoning.

## Cognitive target and diversity

Use a mix appropriate to the source: recognition, application, boundary analysis, competing plausible
interpretations, failure analysis, counterfactuals, replacement tests, lifecycle, authority,
guarantee boundaries, tradeoffs, edge cases, and cross-concept conflicts. Avoid turning every item
into recall with different nouns. Prefer a realistic scenario when the source supports one.

Bloom language can help describe the cognitive target, but it is a planning aid, not a quota requiring
every question set to contain a particular distribution.

## Source entailment review

For every item, ask:

1. Which source concept is being tested?
2. Which source evidence supports the correct proposition?
3. Can a learner derive it without an outside assumption?
4. Does each distractor fail for a distinct, source-relevant reason?
5. Is there one best answer under the stem's stated conditions?

Do not correct, modernize, or silently reinterpret source material in a source-grounded assessment.

## Explanations and answer-key depth

When explanations are requested, connect the answer to source evidence and diagnose each distractor.
Simple recognition items may need only a concise rationale; high-level scenario items may need the
violated boundary and engineering consequence. Do not expose answer-key material in a questions-only
response.
