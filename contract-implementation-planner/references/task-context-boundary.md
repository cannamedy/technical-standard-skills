# Task Context Boundary

An Atomic Task is a bounded implementation context, not a copy of the upstream specification.

Include:

- stable Architecture Constraint anchors needed by the Task;
- Requirement IDs or Section Anchors;
- relevant repository files and dependency outputs;
- allowed and forbidden change surfaces;
- a concrete Conformance Landing and evidence method.

Do not copy the complete Architecture Guide or Engineering Contract into each Task. A Coding Agent
should be able to reread the exact authoritative anchors and load only relevant files. An omitted
context item that is necessary for safe implementation is a planning defect, not permission to guess.
