# Architecture

The node is discovered because consumers cannot assume a fixed device list. The consumer reads a Manifest, observes State, and sends a typed Action. The adapter translates only at the lower boundary.

## Runtime
Discovery supplies the node, State supplies current facts, and the Action creates an Operation. If the camera disappears, the dependent capability becomes unavailable and the upper layer decides recovery.

## Boundary
The counterexample is a vendor branch in the planner.

## Principles
### Discoverable
### Explicit physical facts
### Thin translation boundary
