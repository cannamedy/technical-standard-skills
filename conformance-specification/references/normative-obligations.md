# Normative Obligations

Use this reference to extract obligations before writing scenarios. The companion
`engineering-contract-spec` owns normative keyword meaning and stable clause
discipline; this reference specializes the analysis for proof planning.

## Classification

| Class | Proof question |
| --- | --- |
| `STRUCTURAL_VALIDATION` | Is the required shape present? |
| `VALUE_CONSTRAINT` | Is a value within the explicitly stated domain? |
| `CROSS_FIELD` | Do values relate as specified? |
| `STATE_TRANSITION` | Is the transition legal and observable? |
| `LIFECYCLE` | Is behavior correct across creation, use, and termination? |
| `TEMPORAL` | Is ordering, freshness, duration, or eventuality proven? |
| `IDENTITY` | Is identity stable or correctly related? |
| `REFERENCE` | Is a reference resolved with the stated semantics? |
| `SERIALIZATION` | Are the required bytes or encoding produced? |
| `INTEGRITY` | Does content identity or integrity validate? |
| `ERROR_BEHAVIOR` | Is required rejection or recovery observable? |
| `CAPABILITY_DECLARATION` | Does a claim activate and match obligations? |
| `NEGOTIATION` | Do parties select compatible behavior? |
| `INTEROPERABILITY` | Does the external boundary work between conforming parties? |
| `OBSERVABLE_SIDE_EFFECT` | Is the externally visible result correct? |
| `SECURITY_BOUNDARY` | Are allowed and forbidden accesses observable? |
| `PROFILE_REQUIREMENT` | When does the obligation apply? |
| `NON_OBSERVABLE` | Can the requirement be observed only indirectly or by review? |
| `NON_TESTABLE_DIRECTLY` | What evidence can support it without inventing behavior? |

Multiple classes may apply. Classification must preserve the source's normative
strength and scope; it must not convert a recommendation into a mandatory test.

## Source-first extraction

For every MUST/MUST NOT, retain the exact Requirement ID, anchor, subject, condition,
expected behavior, forbidden behavior, and failure semantics. If any load-bearing
part is absent, use `OPEN_SPEC_ISSUE`. Do not infer a timeout, status code, enum,
fixture, retry, or cleanup obligation from current code.
