// Read-only: source equality AND successful finalized execution, no wallet.
import {readFileSync} from 'node:fs';
import {resolve} from 'node:path';
import {createHash} from 'node:crypto';
import assert from 'node:assert/strict';
import {createClient} from 'genlayer-js';
import {studionet} from 'genlayer-js/chains';

const root = resolve(import.meta.dirname, '..');
const manifest = JSON.parse(readFileSync(resolve(root, 'deployment.json')));
const evidence = JSON.parse(readFileSync(resolve(root, 'evidence/network.json')));
const client = createClient({chain:studionet});
const sha256 = data => createHash('sha256').update(data).digest('hex');
const local = readFileSync(resolve(root, manifest.source_path));
const remote = Buffer.from(await client.getContractCode(manifest.address));
assert(local.equals(remote), 'Source differs byte-for-byte: redeploy before submitting');
assert.equal(sha256(local), manifest.source_sha256);
assert.equal(sha256(remote), manifest.deployed_source_sha256);
for (const item of evidence) {
  const tx = await client.getTransaction({hash:item.hash});
  const status = tx.status_name ?? tx.statusName;
  const execution = tx.consensus_data?.leader_receipt?.[0]?.execution_result ?? tx.txExecutionResultName;
  assert.equal(status, 'FINALIZED', `${item.label} has not finalized`);
  assert.equal(execution, 'SUCCESS', `${item.label} execution failed`);
  console.log(`${item.label}: FINALIZED / SUCCESS ${item.hash}`);
}
console.log(`Verified ${manifest.address}; SHA-256 ${sha256(local)}; ${evidence.length} successful transactions.`);
