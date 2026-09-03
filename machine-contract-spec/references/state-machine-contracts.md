# State-Machine Contracts

Use this reference for lifecycle and transition requirements. Apply the companion
`engineering-contract-spec` state-machine reference for general contract rules.

## Required projection content

When the source defines a state machine, preserve the source vocabulary and record:

- states and their meanings;
- initial state, if defined;
- terminal states, if defined;
- allowed transitions;
- transition triggers and preconditions;
- observable effects/events;
- invalid transition behavior;
- requirement and specification anchors.

Do not fill in an omitted initial state, terminal state, recovery transition, retry
policy, or invalid-transition error. Those are `OPEN_SPEC_ISSUE` candidates if they
are necessary to implement the claimed scope.

## Closure audit

Check that every referenced state exists, every transition has a source and target,
the initial state is valid, terminal semantics are not contradicted, and every
required transition has a machine or conformance landing point. Check reachability
only when the source claims it; an intentionally unreachable reserved state is not
automatically an error.

State machines describe externally observable lifecycle semantics. Internal worker
states, queues, retries, and scheduling steps belong in an Implementation Design
unless the specification makes them observable.
