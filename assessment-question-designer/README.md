# assessment-question-designer v0.1.0

Design and audit source-grounded technical assessment questions, especially four-option MCQs.

The Skill combines:

- source entailment and one-concept blueprints;
- five levels of reasoning difficulty;
- misconception-based distractors;
- balanced but non-obvious answer positions;
- option-length, grammar, ambiguity, and anti-gaming audits;
- whole-batch and tail-quality checks;
- a deterministic JSON validator with hard errors and warnings.

Examples:

> 根据这份架构文档出 20 道 Level 4-5 选择题，只输出题目，不要答案。

> 审计下面 30 道选择题，检查 distractor quality、答案位置偏差和 option-length leakage。

The Skill is independent of any particular technical domain. Use a source-aware model review for
meaning, and `scripts/validate_assessment_questions.py` for mechanical invariants.
