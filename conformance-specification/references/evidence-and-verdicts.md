# Evidence and Verdicts

Use this reference to define what a reviewer or validator can actually inspect.

## Evidence types

```text
SCHEMA_VALIDATION
RUNTIME_ASSERTION
PROTOCOL_TRACE
STATE_TRACE
API_RESPONSE
EVENT_SEQUENCE
SERIALIZED_BYTES
HASH_RESULT
ERROR_RESULT
INTEROP_RESULT
MANUAL_AUDIT
STATIC_ANALYSIS
TEST_EXECUTION
```

The type describes evidence, not a required tool. A `PROTOCOL_TRACE` may come from
any conforming trace capture mechanism allowed by the project.

## Verdict record

Each executable scenario defines:

```text
PASS: exact observed condition
FAIL: exact violation or missing condition
INAPPLICABLE: applicability rule is false
BLOCKED: required source/evidence/environment is unavailable
UNTESTABLE: no deterministic proof is possible under current semantics
```

`INAPPLICABLE` is not a failure for an optional undeclared feature. `BLOCKED` is not
PASS. `UNTESTABLE` must identify whether the specification needs clarification or
manual assurance. “Looks correct” and “generally works” are not verdict rules.

## Evidence sufficiency

Evidence must support the required boundary and observation point. Internal mocks do
not prove interoperability unless the artifact explicitly labels their evidence
level. A test result without source and scenario linkage is not conformance evidence.
