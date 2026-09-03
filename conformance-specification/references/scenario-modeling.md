# Scenario Modeling

Use structured scenario semantics rather than binding the artifact to BDD or a test
framework.

## Scenario record

```text
conformance_id
scenario_id
scenario_kind
preconditions
stimulus
observation_point
expected_observation
forbidden_observation
normative_window
cleanup_isolation
evidence_type
verdict_rule
applicability
source_refs
```

`Given / When / Then` is an optional rendering of these fields. An omitted field is
acceptable only when it does not leave the proof condition ambiguous.

## Minimum sufficient set

Select positive, negative, boundary, transition, and interoperability scenarios only
when the requirement needs them. MUST NOT and rejection requirements need evidence
that the forbidden outcome does not occur. A valid-input scenario alone cannot prove
negative behavior.

Do not make a scenario stronger than its source. If the source says “reject” but does
not specify a code, the scenario's expected observation is rejection, not a guessed
code. If a temporal bound is absent, do not add one merely for test convenience.
