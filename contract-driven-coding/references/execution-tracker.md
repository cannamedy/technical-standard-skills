# Persistent Execution Tracker

Keep one durable tracker per implementation effort, normally at `implementation/traceability.md`
or the project's designated equivalent.

```markdown
# Implementation Traceability

| Requirement | Task | Status | Implementation | Test | Verification |
|---|---|---|---|---|---|
| REQ-001 | TASK-001 | PENDING | — | — | — |
```

Update status at meaningful boundaries: task start, implementation complete, test result, compliance
review, and final verification. Record evidence paths or commands instead of vague notes.

The tracker is a recovery artifact. After interruption or context compaction, reconcile it with Git
status and the authoritative Contract before continuing. Do not treat a chat summary or raw log as
the source of truth.
