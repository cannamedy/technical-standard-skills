# Profile Applicability

Use this reference when requirements depend on profiles, declared capabilities,
features, or negotiation results. Profile names are project-defined.

## Applicability states

| State | Meaning |
| --- | --- |
| `MANDATORY_FOR_PROFILE` | The selected profile requires the obligation. |
| `CONDITIONAL_IF_CAPABILITY_DECLARED` | A declaration activates the obligation. |
| `OPTIONAL_FEATURE` | The feature may be absent; if offered, linked rules apply. |
| `NOT_APPLICABLE` | The source conditions exclude the obligation. |

Record the condition that selects the state. Do not treat an undeclared optional
feature as a failure and do not let a declaration count as proof of behavior.

## Capability claims

For a claim, create at least two linked concerns when the source requires both:

```text
declaration is syntactically/semantically valid
→ declared surface is available
→ declared behavior satisfies its obligations
```

Only the applicable obligations are evaluated. MAY means non-use is allowed; it does
not erase requirements attached to a feature that the implementation offers.
