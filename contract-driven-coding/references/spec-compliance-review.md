# Specification Compliance Review

This review precedes code-quality review. Start from the Requirement IDs and reread the authoritative
Contract, then inspect the actual diff and tests.

Check:

- required behavior is present;
- preconditions, postconditions, failures, and rejection behavior are covered;
- ownership, authority, mutability, lifecycle, safety, and compatibility are respected;
- no mandatory behavior was weakened or invented;
- no Task-forbidden area changed;
- tests and verification correspond to the Contract rather than only to existing implementation.

Record missing or extra behavior as a defect. If the Contract is insufficient, stop with an Open
Contract Issue instead of approving a guess.

After compliance passes, a separate quality review may examine maintainability, duplication,
readability, typing, performance, and repository conventions.
