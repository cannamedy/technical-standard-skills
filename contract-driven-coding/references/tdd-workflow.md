# TDD and Deterministic Verification

For runtime behavior:

1. reread the authoritative requirement;
2. write the smallest failing test;
3. confirm the failure represents the missing Contract behavior;
4. implement the minimum change;
5. confirm the test passes;
6. refactor without changing behavior;
7. rerun focused and relevant broader tests;
8. record evidence in the tracker.

For schemas, static artifacts, generated configuration, documentation-only changes, or environment
changes, select a deterministic check such as schema validation, static inspection, generation
reproducibility, or an environment probe. Record why that method matches the requirement's
verification class.
