# Implementation Design Review Checklist

Review the design against approved normative inputs and implementation constraints,
not against code convenience alone.

## Closure and fidelity

- every required responsibility has one owner;
- Machine Contract objects have realization mappings;
- executable Conformance obligations have observable surfaces and evidence hooks;
- no design choice narrows or changes normative semantics;
- public, project-public, internal, and test-only boundaries are labeled;
- code/spec mismatches are reported rather than normalized.

## Architecture quality

- dependency direction is understandable and free of accidental cycles;
- duplicated ownership and hidden coupling are resolved;
- lifecycle, errors, persistence, concurrency, security, and recovery are addressed
  when applicable;
- evidence hooks are non-invasive;
- alternatives and tradeoffs exist for material decisions;
- architecture is proportional and not added for fashion.

## Handoff verdict

- affected repository surfaces are identified;
- incremental preservation is demonstrated;
- no blocking design issue remains for the claimed scope;
- Planner can decompose work without inventing architecture.

Use `APPROVED`, `REQUIRES_PATCH`, `OPEN_SPEC_ISSUE`, or
`ARCHITECTURE_DECISION_REQUIRED`. The last verdict is only for multiple legitimate
architecture choices whose selection changes an important outcome; ordinary design
defects use `REQUIRES_PATCH`.
