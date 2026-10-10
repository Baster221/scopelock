# Security and integration boundary

## Trust boundary

The owner is trusted to choose a reasonable mandate and consumer. The delegate is adversarial. The consumer is trusted to implement the exact action interface and cost accounting. GenLayer consensus is trusted to execute the protocol; model agreement is useful semantic evidence but does not mathematically prove natural-language truth.

ScopeLock authorizes the content and fields it actually sees. It cannot guarantee an agent's hidden intent, factual honesty, external identity, or subsequent behavior. Do not use a promise such as “I am certified” as a substitute for independently verified certification. Clauses depending on missing external facts are fail-closed by the model rubric. This contract is particularly useful for authorizing exact text publication, because the submitted body is the action artifact itself.

## Controls

| Attack | Enforced control | Residual limitation |
|---|---|---|
| Substitute body after approval | Exact canonical operation comparison at consume | Consumer must use returned fields, not raw duplicate-key JSON or its own transformed text. |
| Reuse permit or nonce | Persistent nonce index and terminal CONSUMED state | An external consumer must deduplicate finalized consume transaction IDs too. |
| Spend concurrent reservations twice | Reserved and spent counters checked before grant | Units are adapter-defined; consumer must independently enforce cost mapping. |
| Steal authority | Delegate-only request and consumer-only consumption | Compromised owner/consumer keys remain trusted authority. |
| Medium confidence passes promotion | Exact bucket comparison; only high ALLOW grants | Exact comparison can reduce liveness on ambiguous inputs. |
| Keyword/negation trick | Independent substantive evaluation of every clause | Correlated LLM mistakes and prompt injection remain possible. |
| Abandoned reservations | Permissionless release after expiry or revocation | Cleanup requires someone to send a transaction. |
| Unbounded work | Input bounds; at most six clauses; no grant-wide permit scan | Persistent histories grow with paid successful calls. |

## Adapter protocol

1. Fix the operation schema and allowed actions. Interpret `resource` consistently; do not resolve it to a different target after approval.
2. Define and verify what one unit means. For publication, require one unit per publication. Do not trust a user-selected unit count to reflect monetary spend.
3. The delegate obtains a READY permit. The adapter calls `consume` with the exact operation.
4. Wait for a successful **FINALIZED** execution receipt. ACCEPTED alone is not finality, and lifecycle status alone is not proof of execution success.
5. Deduplicate the consume transaction and execute the returned action/resource/body exactly once. External delivery failure is an adapter concern; on-chain consumption remains spent. There is no automatic delivery refund or retry promise.

No payable method, escrow, refund, confidential storage, or external transfer is implemented or claimed. All mandate text, operations and verdicts are public. The SHA-256 digest is a domain-separated integrity commitment, not encryption and not a signature.

The digest covers protocol version, chain, deployed contract, grant ID, nonce, consumer, units, and the canonical operation. Expiry/revocation are enforced from stored state, not inferred from this digest.
