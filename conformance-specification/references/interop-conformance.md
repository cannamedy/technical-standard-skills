# Interoperability Conformance

Use this reference when a requirement concerns behavior across an external boundary.

## Evidence levels

Distinguish:

```text
SINGLE_IMPLEMENTATION
BOUNDARY_INTEGRATION
INTEROPERABILITY
```

Single-implementation evidence can prove local observable behavior. It cannot by
itself prove producer/consumer, client/server, controller/device, or negotiated
interoperability. Use two independently bounded roles or an allowed external peer
when the source requires cross-party behavior.

Label mocks, simulators, reference peers, and real peers accurately. A mock may prove
schema or local rejection, but it must not be silently reported as interoperability.
Negotiation obligations must record the offered inputs, selected result, and behavior
when no compatible selection exists.
