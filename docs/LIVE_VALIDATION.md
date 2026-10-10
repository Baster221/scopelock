# Live StudioNet validation

Contract: [0x4a38a7183bCFB23843362DC02FE69c26Cb4C91af](https://explorer-studio.genlayer.com/address/0x4a38a7183bCFB23843362DC02FE69c26Cb4C91af)

Network: GenLayer StudioNet, chain ID 61999. This is a hosted GenVM network, not a local simulator or a Bradbury deployment.

The deployment, grant creation, positive permit, consumption and negative permit all executed successfully and finalized. See the exact transaction hashes, leader execution outcome, consensus result and vote names in [network.json](../evidence/network.json). IDLE votes record validators canceled after quorum; they are not claimed as five unanimous votes. The run used normal validator consensus, not leader-only execution.

| Step | Expected and observed state |
|---|---|
| Create grant | 10 units / 2 uses, two immutable clauses, fixed delegate and consumer. |
| Free educational workshop announcement | Both clauses ALLOW/high; permit 1 READY. |
| Consume exact announcement | Permit 1 CONSUMED; spent units 1; no remaining reservation. |
| Workshop message requesting password and payment | Permit 2 REJECTED; no quota reserved. |

The live example uses one demonstration address for owner, delegate and consumer; the direct suite separately tests distinct addresses and unauthorized callers. Final state is recorded in [state.json](../evidence/state.json). Source SHA-256 is `bfefeb19be3cfcde0ac928d5309a2f56765876470281b8725a0542068644d5e3`, matching the source fetched from the supplied address byte-for-byte.

## Independent verification

```bash
npm ci --ignore-scripts
npm run verify
python scripts/check_manifest.py
```

`npm run verify` needs Node.js 22+ and internet access, but no wallet or signing key. It compares remote source bytes with the local file and validates FINALIZED plus SUCCESS for every evidence transaction. The Python command only checks local consistency with the recorded manifest and is not presented as a fresh network check.

Real model behavior here is demonstrated by two clear examples. This is not a broad adversarial-model benchmark or a guarantee that every natural-language policy will converge. Direct tests exercise malformed and disagreeing responses independently of model accuracy.
