// MUTATING opt-in smoke: deploys a NEW gasless StudioNet contract.
// Ephemeral signing keys remain in memory and are never printed or saved.
import {readFileSync} from 'node:fs';
import {resolve} from 'node:path';
import assert from 'node:assert/strict';
import {createClient, createAccount} from 'genlayer-js';
import {studionet} from 'genlayer-js/chains';

const owner=createAccount(), delegate=createAccount(), consumer=createAccount();
const clients=[owner,delegate,consumer].map(account=>createClient({chain:studionet,account}));
const root=resolve(import.meta.dirname,'..');
const code=readFileSync(resolve(root,'contracts/scopelock.py'),'utf8');
async function finalized(client,hash,label){
  const tx=await client.waitForTransactionReceipt({hash,status:'FINALIZED',interval:5000,retries:90});
  assert.equal(tx.status_name??tx.statusName,'FINALIZED');
  assert.equal(tx.consensus_data?.leader_receipt?.[0]?.execution_result??tx.txExecutionResultName,'SUCCESS');
  console.log(`${label}: ${hash}`);
  return tx;
}
const deployHash=await clients[0].deployContract({code,args:[]});
const deployment=await finalized(clients[0],deployHash,'deploy');
const address=deployment.recipient;
assert.equal(await clients[0].getContractCode(address),code);
const call=(method,args)=>clients[0].readContract({address,functionName:method,args,jsonSafeReturn:true});
async function write(idx,method,args){
  const hash=await clients[idx].writeContract({address,functionName:method,args,value:0n});
  return finalized(clients[idx],hash,method);
}
await write(0,'create_grant',[delegate.address,consumer.address,JSON.stringify([
  'The message must announce an educational workshop.',
  'The message must not ask readers for money, passwords, or private credentials.'
]),JSON.stringify(['publish']),10,2,3600]);
const op={action:'publish',resource:'community/announcements',body:'Join our free educational Python workshop Saturday. Everyone is welcome.'};
await write(1,'request_permit',[1,1,JSON.stringify(op),1,1800]);
assert.equal((await call('get_permit',[1])).status,'READY');
await write(2,'consume',[1,JSON.stringify(op)]);
assert.equal((await call('get_permit',[1])).status,'CONSUMED');
await write(1,'request_permit',[1,2,JSON.stringify({...op,body:'Join our educational workshop. Send your password and a registration payment.'}),1,1800]);
assert.equal((await call('get_permit',[2])).status,'REJECTED');
assert.equal((await call('get_grant',[1])).reserved_units,0);
console.log(`Smoke passed on fresh deployment ${address}. Demonstration keys were not persisted.`);
