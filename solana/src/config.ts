import { Connection, Keypair } from "@solana/web3.js"
import * as dotenv from 'dotenv';

dotenv.config();

export const SOLANA_NETWORK = process.env.SOLANA_NETWORK || 'devnet';
export const SOLANA_RPC_URL = process.env.SOLANA_RPC_URL || 'https://api.devnet.solana.com';

export const connection = new Connection(SOLANA_RPC_URL, 'confirmed');

export function getWalletKeypair(): Keypair {
    const privateKey = process.env.PRIVATE_KEY;
    if (!privateKey) {
        throw new Error('PRIVATE_KEY environment variable is not set');
    }
    return Keypair.fromSecretKey(
        Uint8Array.from(JSON.parse(privateKey))
    );
}

export const PROGRAM_IDS = {
    CITY_STATE: process.env.CITY_STATE_PROGRAM_ID || '',
    AGENT_MAIL: process.env.AGENT_MAIL_PROGRAM_ID || '',
    FINANCE: process.env.FINANCE_PROGRAM_ID || '',
}