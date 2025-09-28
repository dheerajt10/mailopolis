import { Keypair } from "@solana/web3.js";

console.log(`Generating new keypair...`);

const keypair = Keypair.generate();
console.log(`Copy the following generated keys to your .env file:`);
console.log(`PRIVATE_KEY=${JSON.stringify(Array.from(keypair.secretKey))}`);
console.log(`PUBLIC_KEY=${keypair.publicKey.toString()}`);

console.log(`You can also run this command to load the keypair:`);
console.log(`tsx src/index.ts`);