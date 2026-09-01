# Final Requirement-level Verification

Do not infer completeness from aggregate test status. For every current-scope requirement, record:

| Status | Meaning |
|---|---|
| implemented | Code or artifact exists for the requirement. |
| verified | Evidence confirms the required behavior or invariant. |
| unimplemented | No implementation landing point exists. |
| partially implemented | Some required behavior exists, but the requirement is incomplete. |
| blocked | Work cannot proceed under an explicit dependency or approval boundary. |
| contract issue | The Contract is ambiguous or contradictory. |

The final report should link each status to the Task, implementation surface, test, and verification
evidence. A planning-stage `IMPLEMENTED` disposition is evidence of a landing point only. Promote it
to `VERIFIED` only after rereading the authoritative Requirement, inspecting the implementation and
diff, running required tests or deterministic checks, and inspecting the conformance evidence. A
Contract conflict remains `DRIFT`, `BLOCKED`, `CONTRACT_ISSUE`, or `PLAN / TASK DEFECT` as applicable;
it must not be promoted. A gap remains a gap even when all currently executed tests pass.
