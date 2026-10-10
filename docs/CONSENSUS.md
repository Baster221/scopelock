# Consensus specification

Let `C` be the immutable owner-authored clause array, `O` the canonical exact operation, and `V` the complete decision vector. Each node calls the model on `(C, O)`. The validator does not feed the leader answer into this prompt. It validates the leader vector structurally, independently derives its own vector, and compares every decision and exact confidence bucket.

```text
equivalent(L,V) := canonical(L) == canonical(V)
permit(V) := for every clause i: decision[i] == ALLOW and confidence[i] == high
```

Consequently `equivalent(L,V)` implies `permit(L) == permit(V)`. The complete stored vector is also invariant under accepted equivalence. Comparing confidence approximately would violate this property. Comparing only the final Boolean would hide substantive disagreements and would weaken the audit record; neither is done here.

Clause IDs must be exact integers, unique, and cover `[0, len(C))`. Boolean IDs, unexpected fields, confidence coercions, extra categories and omitted clauses fail parsing. Row order is normalized. There are no free-form rationales whose wording could accidentally change an authorization tier.

The actual model judgment is whether the submitted operation itself satisfies each clause, including prohibitions, exceptions and missing facts. An owner-created clause about an externally verified identity cannot be proven from this operation and should return UNKNOWN. Confidence is an epistemic bucket, not a calibrated probability.

No state is modified inside the nondeterministic closures. Both capture ordinary bounded values. State writes follow successful consensus and deterministic parsing. A malformed or failing leader result is rejected by validators; a failing validator returns False. This can reduce liveness when a model/provider is unreliable. There is deliberately no fallback that upgrades uncertainty to authority.

The network supplies validator selection, transaction appeals, and finality. ScopeLock does not invent a second challenge registry. A semantic rejection can be retried with a corrected operation and a fresh nonce; an owner can revoke the underlying grant. Corrections to deployed code require a new address and a verified new source manifest.
