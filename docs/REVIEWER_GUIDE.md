# Reviewer guide

Start with `request_permit` and its validator in `contracts/scopelock.py`, then inspect `consume` and `release`. The consensus-sensitive boundary is deliberately small: the model decides whether an exact operation satisfies immutable clauses. Deterministic code owns every consequence of that judgment.

## Five questions to verify

| Question | Where the answer is enforced |
|---|---|
| Can high and medium compare as equivalent despite changing permission? | No. `_verdict` preserves the exact bucket and the validator compares the complete vector; tests flip both buckets. |
| Is this an evidence-adjudication registry with a renamed software domain? | No. There are no source URL registries, challenger lifecycles or adjudication thresholds. Its state is a capability ledger with reservations and exact consumption. |
| Can one unverified category change an authorization tier? | Every owner clause must be independently re-evaluated; no leader-selected clause subset or model-created categories exist. |
| Does the supplied deployment implement the source in GitHub? | `deployment.json` records both hashes; `npm run verify` re-fetches raw source and finalized execution receipts. CI rejects changes inconsistent with that manifest. |
| Does an applicant claim establish external identity? | No identity benefit or payout exists. Clauses requiring absent external facts must be UNKNOWN; the primitive constrains the exact operation artifact. |

## Concrete reuse

For a public-message adapter, fix `action=publish`, define the channel/resource syntax, require exactly one unit per message, and execute the returned canonical body after a finalized successful consume transaction. The mandate can express “announce technical workshops without soliciting payment or private credentials.” Owner-defined deterministic allowlists and quotas remain in force even if a semantic judgment is erroneous.

This composition is useful beyond the example message: the same capability ledger can constrain exact help-center edits, document-workflow artifacts or agent tool calls whose consumer understands the operation schema. It is not a universal certification oracle or an atomic bridge to external execution.

## Evidence boundaries

The direct suite checks code-level adversarial results and explicitly exercises the validator. Live receipts demonstrate real consensus for clear positive and negative examples. Agreement is not a proof of LLM correctness for every adversarial payload. Inspect SECURITY.md for residual trust and adapter obligations.
