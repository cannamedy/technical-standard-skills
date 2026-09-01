# Safety Contract Review

## Layered authority

For physical systems, distinguish:
1. higher-level task/orchestration safety;
2. contract/runtime validation;
3. native device/controller safety.

Each layer may reject.
Lower-level native safety remains non-bypassable unless the architecture explicitly defines otherwise.

## Formal checks

Review:
- permission;
- schema/type/unit/frame validation;
- preconditions;
- soft limits;
- hard limits;
- stale state;
- unknown constraints;
- fail-safe/default-deny behavior;
- validation order;
- TOCTOU;
- revalidation before dispatch;
- cancel;
- stop;
- emergency stop;
- validator failure;
- audit linkage.

Never rely only on natural-language safety descriptions when deterministic enforcement is required.
