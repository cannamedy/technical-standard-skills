# Skill Design Influences

This repository uses a conceptual clean-room reimplementation. The sources below were studied for
engineering mechanisms; their Skill instructions, source code, and directory conventions are not
vendored here.

| External Source | Mechanism Studied | Adopted | Adapted | Rejected / Not Adopted | Reason |
|---|---|---|---|---|---|
| [iurysza/agent-skills — tech-spec](https://github.com/iurysza/agent-skills/tree/main/skills/tech-spec) | Concrete boundary contracts; Input / Output / Expected Failure; end-to-end call/data flow; implementation-ready handoff; vertical red-green test slices; file mapping | Concrete boundary contract; input/output/failure semantics; end-to-end behavior flow | File mapping belongs to Planner; vertical test slices are mainly Planner/Coding concerns | Mandatory fixed document directory | Keep the Contract behavior-focused and repository-adaptable. |
| [Fission-AI/OpenSpec](https://github.com/Fission-AI/OpenSpec) | Requirement as behavior contract; Requirement → Scenario; spec / design / tasks separation; verification; change-oriented workflow | Verifiable scenarios where useful; testability classification; spec/implementation separation; unresolved load-bearing questions do not pass silently downstream | Not every protocol or schema requirement needs GIVEN/WHEN/THEN | Proposal-driven repository model; mandatory scenario for every requirement; OpenSpec directory format | Preserve a lighter, contract-centered workflow that supports existing repositories. |
| [GitHub Spec Kit](https://github.com/github/spec-kit) | Spec → Plan → Tasks → Implement; persistent artifacts between stages | Explicit Plan and Task layers; approved artifacts consumed downstream | Repository layout remains project-defined | Framework-specific directories and command names | Keep artifacts portable across repositories and Agents. |
| [obra/superpowers](https://github.com/obra/superpowers) | Fresh task context; spec compliance review; code quality review; worktree isolation; execution ledger; final branch review | Compliance review before code-quality review; bounded task context; persistent tracker; worktree discipline; final whole-change verification | Subagents are optional; without them, roles are logically separated in one Agent | Any required subagent feature or platform-specific worktree API | Core behavior must remain available on simple Agent runtimes. |
| [realworldtech/claude-implement-skill](https://github.com/realworldtech/claude-implement-skill) | Source section anchors; persistent requirement tracker; reread source before each task; resume after compaction; requirement-level verification | Requirement IDs / section anchors; reread authoritative Contract; persistent traceability; final gap verification | No platform-specific commands or permissions are required | Platform-specific commands and permission configuration | Preserve the mechanism while removing vendor coupling. |
| [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | Gated spec-driven workflow; planning/task breakdown; incremental implementation; context engineering; TDD composition | Bounded context; dependency-aware planning; incremental implementation; TDD when behavior is testable | No universal fixed file-count rule; command syntax is intentionally omitted | Arbitrary fixed file-count law and platform-specific commands | Match task size to bounded context without inventing repository policy. |

No substantial third-party Skill source text or code is copied into this repository. No third-party
attribution or license notice is required beyond the source links used as design references.

## Internal Workflow Learnings

The following rules were distilled from real Contract → Planning workflow practice. They are
general workflow controls, not product- or architecture-specific requirements:

- frozen source integrity before planning;
- complete Requirement dispositions;
- repository reality classified separately from Contract authority;
- declared gap counts reconciled against the current repository;
- bounded Task context with stable anchors and explicit conformance landing;
- deferred scope prevented from becoming mandatory work;
- implementation dispositions promoted to verification only after Contract-based evidence.
- scope-aware working-tree audit that distinguishes expected target artifacts from unrelated
  contamination;
- non-sticky post-patch Gate evaluation that recomputes current status after remediation.

These controls came from real Contract → Planning → Compatibility Audit workflow practice. They are
generic planner workflow learnings, not requirements or details of any one product repository.
