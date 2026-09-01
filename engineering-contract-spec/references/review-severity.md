# Review Severity

First classify:
- Incorrect
- Ambiguous
- Incomplete for current scope
- Intentionally deferred
- Optional improvement

Then severity:

## Critical
Unsafe execution, invalid conformance claim, fundamental contradiction, or current-scope incompatibility.

## High
Blocks independent implementation, interoperability, deterministic testing, or a core boundary promised by the release.

## Medium
Direction is sound but contract needs clarification or additional semantics.

## Low
Editorial or non-blocking improvement.

Working Draft incompleteness is not automatically High/Critical.
