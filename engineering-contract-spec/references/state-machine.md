# State Machine Contract

For every lifecycle-bearing object, define a transition matrix:

| From | Trigger | Guard | To | Observable output | Invalid transition |
|---|---|---|---|---|---|

Also define:
- initial state;
- terminal states;
- timeout semantics;
- cancellation semantics;
- idempotency/duplicate request behavior;
- disconnect behavior;
- restart behavior;
- recovery/reconciliation behavior.

Do not invent states merely to look complete.
The state machine should reflect the architecture and declared release scope.
