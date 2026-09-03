# Coverage Closure

Use this reference to expose missing proof obligations and unsupported tests.

## Coverage chain

```text
Requirement
→ Conformance Obligation
→ Scenario / Assertion
→ Evidence Requirement
→ Deterministic Verdict
```

Each record includes:

```text
requirement_id
engineering_spec_anchor
conformance_ids
machine_contract_refs
normative_strength
disposition
unmapped_reason
```

Use these dispositions:

- `EXECUTABLE_CONFORMANCE`
- `MACHINE_CONTRACT_SUFFICIENT`
- `MANUAL_AUDIT`
- `NON_OBSERVABLE`
- `NOT_APPLICABLE`
- `OPEN_SPEC_ISSUE`

Every MUST and MUST NOT needs a disposition. `UNMAPPED MUST = 0` is the closure gate;
an explicit, scoped open issue is not a silent omission. A test that has no normative
source is an unsupported conformance check, even if it improves code coverage.
