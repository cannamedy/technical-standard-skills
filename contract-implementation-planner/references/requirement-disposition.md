# Requirement Disposition and Repository Reality

Every current-scope Requirement needs an explicit disposition. Projects may use equivalent labels,
but the meaning must distinguish evidence, work, blockers, drift, and deferred scope.

| Disposition | Planning meaning |
|---|---|
| `IMPLEMENTED` | An implementation landing point exists; not yet verified. |
| `PARTIAL` | Some required behavior exists, but the Requirement is incomplete. |
| `PENDING` | Work is required and not yet started or classified further. |
| `DRIFT` | Existing implementation conflicts with the authoritative Contract. |
| `BLOCKED` | Work cannot proceed under a recorded dependency, approval, or issue. |
| `DEFERRED` | The authoritative Contract excludes the behavior from current mandatory scope. |

Classify repository reality as already implemented, partially implemented, implementation drift,
missing, or deferred. Existing code and passing tests are evidence, never behavior authority.

Reconcile declared gap counts and TODO counts against the current repository. Record whether each is
a confirmed gap, already resolved, additional drift, or newly discovered gap. Do not mechanically
inherit stale inventory.

No current-scope Requirement may remain `UNMAPPED`. A mandatory Requirement maps to existing
implementation evidence, an implementation Task, or an explicit `BLOCKED` disposition. Do not
create a duplicate Task solely because an implementation already exists.
