# ScopeLock — Single-use semantic capabilities for autonomous agents

**Category:** Intelligent Contracts

**Repository:** https://github.com/Baster221/scopelock

**Live contract (GenLayer StudioNet):** https://explorer-studio.genlayer.com/address/0x4a38a7183bCFB23843362DC02FE69c26Cb4C91af

## Purpose

ScopeLock turns a human-readable agent mandate into bounded, consumable authorization. An owner fixes a delegate, consuming adapter, independent scope clauses, action allowlist, unit budget, use limit and expiry. The delegate submits the exact operation artifact. Successful semantic consensus creates a reservation-backed, single-use permit; only the fixed consumer can consume it, and only for the same operation.

This is useful for publishing agents and constrained agent tools: an API key alone cannot distinguish a permitted workshop announcement from a message soliciting credentials. The semantic decision is tied to persistent authorization and accounting, rather than returned as an advisory model response.

## GenLayer consensus

Each validator independently evaluates every immutable scope clause against the complete operation. The complete canonical vector of clause ID, decision and confidence must match exactly. High confidence never matches medium confidence. Every clause must be ALLOW/high before authority is granted; ambiguity and unverifiable external assertions fail closed. Missing/duplicate clauses, malformed outputs and leader errors cannot grant a permit.

Authority, reservations, nonces, revocation, expiration and consumption are deterministic. A domain-separated SHA-256 commitment binds chain, deployment, grant, consumer, nonce, units and canonical operation. Revocation immediately disables outstanding permits; anyone can release expired or revoked reservations without an unbounded scan.

## Review evidence

- One readable, independently deployable source file with a pinned GenVM runner.
- 23 passing direct tests, including explicit execution of captured validators with conflicting outputs.
- Real StudioNet positive authorization, exact consumption, credential/payment solicitation rejection and UNKNOWN/low rejection of self-asserted certification, with finalized successful execution receipts in `evidence/network.json` and resulting state in `evidence/state.json`.
- `deployment.json` records matching local/deployed source hashes. `npm run verify` re-fetches source and receipts without a wallet.
- Consensus specification, threat model, adapter protocol, MIT license, locked verification dependencies and GitHub CI.

The contract stores public operation data and moves no money. Consumers must enforce real cost mapping and wait for finality before external side effects. ScopeLock does not certify external identity or facts. These boundaries are explicit in the documentation.
