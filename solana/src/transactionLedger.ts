import { Connection, PublicKey, Keypair, Transaction, SystemProgram, LAMPORTS_PER_SOL } from '@solana/web3.js';
import { FinancialTransaction, AgentType, TransactionType, Intentions } from './types';
import { getWalletKeypair } from './config';

export class TransactionLedger {
    private connection: Connection;
    private transactionAccount: Keypair;
    private wallet: Keypair;
    private agentAccounts: Map<AgentType, Keypair>;
    private transactionHistory: FinancialTransaction[] = [];

    constructor() {
        this.connection = new Connection('https://api.devnet.solana.com', 'confirmed');
        this.wallet = getWalletKeypair();
        this.transactionAccount = Keypair.generate();
        this.agentAccounts = new Map();
        
        // Generate unique keypairs for each agent type
        this.initializeAgentAccounts();
    }

    private initializeAgentAccounts(): void {
        const agentTypes: AgentType[] = [
            'mayor',
            'power_grid_chief', 
            'hospital_chief',
            'transit_chief',
            'finance_chief',
            'citizen_representative'
        ];

        agentTypes.forEach(agentType => {
            this.agentAccounts.set(agentType, Keypair.generate());
        });
    }

    async initializeTransactionLedger(): Promise<string> {
        try {
            const createAccountIx = SystemProgram.createAccount({
                fromPubkey: this.wallet.publicKey,
                newAccountPubkey: this.transactionAccount.publicKey,
                lamports: LAMPORTS_PER_SOL * 0.01,
                space: 8 + 2048, // 8 bytes discriminator + 2KB for transaction data
                programId: SystemProgram.programId,
            });

            const transaction = new Transaction();
            transaction.add(createAccountIx);
            const latestBlockhash = await this.connection.getLatestBlockhash();
            transaction.recentBlockhash = latestBlockhash.blockhash;
            transaction.feePayer = this.wallet.publicKey;

            transaction.sign(this.wallet, this.transactionAccount);
            const rawTransaction = transaction.serialize();
            const signature = await this.connection.sendRawTransaction(rawTransaction);
            await this.connection.confirmTransaction({
                signature,
                blockhash: latestBlockhash.blockhash,
                lastValidBlockHeight: latestBlockhash.lastValidBlockHeight
            }, 'confirmed');

            console.log(`Transaction ledger initialized`);
            console.log(`Transaction Account: ${this.transactionAccount.publicKey.toString()}`);
            console.log(`Transaction: ${signature}`);

            // Log all agent accounts
            console.log(`\nAgent Accounts Generated:`);
            this.agentAccounts.forEach((keypair, agentType) => {
                console.log(`${agentType}: ${keypair.publicKey.toString()}`);
            });

            return signature;
        } catch (error) {
            console.error('Error initializing transaction ledger:', error);
            throw error;
        }
    }

    async recordTransaction(transaction: FinancialTransaction): Promise<string> {
        try {
            console.log(`Recording transaction: ${transaction.from} -> ${transaction.to}`);
            console.log(`Transaction ID: ${transaction.id}`);
            console.log(`Amount: ${transaction.amount} SOL`);
            console.log(`Type: ${transaction.transactionType}`);
            console.log(`Description: ${transaction.description}`);
            console.log(`Intention: ${transaction.intention || 'not specified'}`);
            console.log(`Timestamp: ${new Date(transaction.timestamp).toISOString()}`);
            
            // Store transaction in local history (in real implementation, this would be on-chain)
            this.transactionHistory.push(transaction);
            
            // Get the agent accounts involved
            const fromAccount = this.agentAccounts.get(transaction.from);
            const toAccount = this.agentAccounts.get(transaction.to);
            
            if (fromAccount && toAccount) {
                console.log(`From Account: ${fromAccount.publicKey.toString()}`);
                console.log(`To Account: ${toAccount.publicKey.toString()}`);
            }
            
            // Return a mock transaction signature for now
            return `tx_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
        } catch (error) {
            console.error('Error recording transaction:', error);
            throw error;
        }
    }

    async getTransactionHistory(from?: AgentType, to?: AgentType): Promise<FinancialTransaction[]> {
        try {
            console.log(`Getting transaction history for ${from || 'all'} -> ${to || 'all'}`);
            
            let filteredTransactions = this.transactionHistory;
            
            if (from) {
                filteredTransactions = filteredTransactions.filter(tx => tx.from === from);
            }
            
            if (to) {
                filteredTransactions = filteredTransactions.filter(tx => tx.to === to);
            }
            
            return filteredTransactions;
        } catch (error) {
            console.error('Error getting transaction history:', error);
            throw error;
        }
    }

    getTransactionAccount(): PublicKey {
        return this.transactionAccount.publicKey;
    }

    getAgentAccount(agentType: AgentType): PublicKey | undefined {
        const keypair = this.agentAccounts.get(agentType);
        return keypair?.publicKey;
    }

    getAllAgentAccounts(): Map<AgentType, PublicKey> {
        const accounts = new Map<AgentType, PublicKey>();
        this.agentAccounts.forEach((keypair, agentType) => {
            accounts.set(agentType, keypair.publicKey);
        });
        return accounts;
    }

    // Helper method to create a transaction with proper typing
    createTransaction(
        from: AgentType,
        to: AgentType,
        amount: number,
        transactionType: TransactionType,
        description: string,
        intention?: Intentions
    ): FinancialTransaction {
        return {
            id: `tx_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
            from,
            to,
            amount,
            transactionType,
            timestamp: Date.now(),
            description,
            intention
        };
    }
}
