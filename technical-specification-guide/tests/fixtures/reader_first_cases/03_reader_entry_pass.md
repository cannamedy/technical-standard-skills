# Physical Interface

PAIS is a standard contract for a Physical Node. It solves the gap left by an Adapter: a new consumer can discover and understand a node, while planning remains outside the boundary.

## One-page Mental Map

Consumer → Physical Node Contract → Adapter → vendor hardware.

## Design Spine

Discovery, explicit facts, typed physical actions, capability boundaries, and a thin adapter.

## Concepts
The consumer reads the Manifest, then observes State before sending an Action.

## Runtime
The same node is discovered, described, observed, and executed; a failure leads to recovery.

## Principles
The boundary is visible in the runtime and counterexample.
The principles preserve Discovery, Manifest, State, Action, and Adapter.
