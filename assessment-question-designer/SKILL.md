---
name: assessment-question-designer
description: >
  Design, audit, and improve source-grounded technical assessment questions, especially multiple-choice
  questions, with diagnostic distractors, calibrated difficulty, balanced answer positions, and
  anti-gaming checks. Use for quizzes, exams, knowledge checks, architecture understanding, and
  technical training questions. Do not use for surveys, personality tests, clinical assessments, or
  essay grading.
metadata:
  version: "0.1.0"
  role: "source-grounded-assessment-question-designer"
---

# Assessment Question Designer

Design assessments that measure understanding rather than test-taking skill. A distractor is not
filler: it should represent a plausible misconception, partial understanding, wrong scope, layer,
timing, authority, abstraction, or another believable reasoning failure.

## Scope and activation

Use this Skill for generating, reviewing, or improving quizzes, exams, MCQs, knowledge checks,
architecture understanding questions, technical training questions, and diagnostic questions. It can
run independently of any architecture-writing Skill and should activate for equivalent Chinese
requests such as 出选择题、出测试题、出考题、出培训题、出架构理解题、优化干扰项、提高题目难度、检查题目质量.

Do not use it as the primary Skill for opinion surveys, personality or clinical psychometrics, essay
grading rubrics, or unrelated lesson planning.

## Source-grounded assessment

When the user supplies source material, enter SOURCE-GROUNDED ASSESSMENT mode:

- the correct answer MUST be supported by the source;
- distractors MAY derive from plausible misunderstandings of the source;
- do not silently introduce external technical facts;
- label items that intentionally use outside knowledge;
- preserve source terminology when terminology is part of what is being tested;
- do not “correct” the source while writing a source-grounded quiz unless asked.

For each item, internally answer: what source concept is tested, what evidence supports the answer,
and whether the answer is derivable without outside assumptions.

## Design pipeline

Build a complete blueprint before writing the option text:

1. identify the assessment goal and one primary conceptual target;
2. extract concepts, boundaries, constraints, and likely misconceptions from the source;
3. assign cognitive target and difficulty;
4. write the correct proposition;
5. create distinct, plausible distractors from diagnosed reasoning failures;
6. normalize option grammar, granularity, specificity, and practical length;
7. assign a balanced but non-obvious answer-position sequence at question-set level;
8. audit ambiguity, source entailment, and answer leakage;
9. separate student-facing questions from answer key and rationale;
10. run `scripts/validate_assessment_questions.py` and review its warnings;
11. audit the complete batch, including the final 25% of items.

Read [references/assessment-design-principles.md](references/assessment-design-principles.md) for
blueprints, source grounding, cognitive targets, and question diversity. Read
[references/difficulty-model.md](references/difficulty-model.md) for the five-level model and
[references/distractor-design.md](references/distractor-design.md) for the distractor taxonomy.

## Question and batch invariants

For a standard MCQ4 item, use exactly four parallel options and one best answer. If a well-informed
reader can reasonably defend two answers, rewrite the stem first; do not fix ambiguity by making one
option longer. A Level 5 item is difficult because it requires deeper reasoning, not because it is
long, obscure, double-negative, or tricky.

For a 20-question four-option set, target A/B/C/D = 5/5/5/5. When the count is not divisible by
four, position counts SHOULD differ by no more than one. A same-answer streak MUST NOT exceed two
unless the user explicitly requests an unbalanced or preserved sequence. Balanced does not mean a
predictable ABCD cycle.

Read [references/anti-gaming-rules.md](references/anti-gaming-rules.md) for option symmetry,
position balance, leakage, ambiguity, and tail-quality checks. Read
[references/external-influences.md](references/external-influences.md) for independent methodology
provenance and license boundaries. Read [references/generic-examples.md](references/generic-examples.md)
when a domain-neutral bad-versus-good item example is useful.

## Modes and output boundary

In design mode, keep an internal blueprint with item ID, source concept, objective, cognitive level,
difficulty, stem, correct proposition, three misconception labels, answer position, source evidence,
rationale, and ambiguity result. Expose it only when useful or requested.

In audit mode, report actionable findings with severity, question ID, evidence, why it is a problem,
the likely guessing cue or misconception issue, and a recommended rewrite. Deterministic checks belong
to the validator; judgments about conceptual validity, misconception plausibility, and one-best-answer
quality require source-aware reasoning.

If the user asks for “questions only” or says not to show answers, output only the student-facing
questions: no answer key, hints, rationale, metadata, answer positions, or blueprint. Generate and
validate the hidden answer key internally, then withhold it. Reveal explanations only when requested
or when grading submitted answers.

For answer-key or grading mode, scale explanation depth to the item and request. Useful fields include
Correct Answer, Why Correct, Why Each Distractor Is Wrong, Misconception, Violated Principle or
Boundary, Engineering Consequence, and Source Evidence; do not inflate simple explanations.

Quality MUST NOT DEGRADE WITH ITEM INDEX. For large batches, blueprint first, write in bounded
batches, run a whole-set audit, and inspect the final 25% for difficulty and distractor quality.

Read [references/assessment-design-principles.md](references/assessment-design-principles.md) for the
data shape used by the independent validator. Use the validator as a quality signal, not as proof
that a question is pedagogically or technically correct.
