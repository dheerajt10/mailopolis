import { Connection, PublicKey, Keypair, Transaction, SystemProgram, LAMPORTS_PER_SOL } from '@solana/web3.js';
import { ChatMessage, AgentType, MessageType, Intentions } from './types';
import { getWalletKeypair } from './config';

export class MailLedger {
    private connection: Connection;
    private mailAccount: Keypair;
    private wallet: Keypair;
    private agentAccounts: Map<AgentType, Keypair>;
    private messageHistory: ChatMessage[] = [];

    constructor() {
        this.connection = new Connection('https://api.devnet.solana.com', 'confirmed');
        this.wallet = getWalletKeypair();
        this.mailAccount = Keypair.generate();
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


    async initializeMailSystem(): Promise<string> {
        try {
            const createAccountIx = SystemProgram.createAccount({
                fromPubkey: this.wallet.publicKey,
                newAccountPubkey: this.mailAccount.publicKey,
                lamports: LAMPORTS_PER_SOL * 0.01,
                space: 8 + 1024, // 8 bytes discriminator + 1KB for mail data
                programId: SystemProgram.programId,
            });

            const transaction = new Transaction();
            transaction.add(createAccountIx);
            const latestBlockhash = await this.connection.getLatestBlockhash();
            transaction.recentBlockhash = latestBlockhash.blockhash;
            transaction.feePayer = this.wallet.publicKey;

            transaction.sign(this.wallet, this.mailAccount);
            const rawTransaction = transaction.serialize();
            const signature = await this.connection.sendRawTransaction(rawTransaction);
            await this.connection.confirmTransaction({
                signature,
                blockhash: latestBlockhash.blockhash,
                lastValidBlockHeight: latestBlockhash.lastValidBlockHeight
            }, 'confirmed');

            console.log(`Mail system initialized`);
            console.log(`Mail Account: ${this.mailAccount.publicKey.toString()}`);
            console.log(`Transaction: ${signature}`);

            // Log all agent accounts
            console.log(`\nAgent Accounts Generated:`);
            this.agentAccounts.forEach((keypair, agentType) => {
                console.log(`${agentType}: ${keypair.publicKey.toString()}`);
            });

            return signature;
        } catch (error) {
            console.error('Error initializing mail system:', error);
            throw error;
        }
    }

    async recordMessage(message: ChatMessage): Promise<string> {
        try {
            console.log(`Recording message: ${message.sender} -> ${message.recipient}`);
            console.log(`Message ID: ${message.id}`);
            console.log(`Content: ${message.content}`);
            console.log(`Type: ${message.messageType}`);
            console.log(`Intention: ${message.intention || 'not specified'}`);
            console.log(`Timestamp: ${new Date(message.timestamp).toISOString()}`);
            
            // Store message in local history (in real implementation, this would be on-chain)
            this.messageHistory.push(message);
            
            // Get the agent accounts involved
            const senderAccount = this.agentAccounts.get(message.sender);
            const recipientAccount = this.agentAccounts.get(message.recipient);
            
            if (senderAccount && recipientAccount) {
                console.log(`Sender Account: ${senderAccount.publicKey.toString()}`);
                console.log(`Recipient Account: ${recipientAccount.publicKey.toString()}`);
            }
            
            // Return a mock transaction signature for now
            return `mail_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
        } catch (error) {
            console.error('Error recording message:', error);
            throw error;
        }
    }


    async getMessageHistory(sender?: AgentType, recipient?: AgentType): Promise<ChatMessage[]> {
        try {
            console.log(`Getting message history for ${sender || 'all'} -> ${recipient || 'all'}`);
            
            let filteredMessages = this.messageHistory;
            
            if (sender) {
                filteredMessages = filteredMessages.filter(msg => msg.sender === sender);
            }
            
            if (recipient) {
                filteredMessages = filteredMessages.filter(msg => msg.recipient === recipient);
            }
            
            return filteredMessages;
        } catch (error) {
            console.error('Error getting message history:', error);
            throw error;
        }
    }


    getMailAccount(): PublicKey {
        return this.mailAccount.publicKey;
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

    // Helper method to create a message with proper typing
    createMessage(
        sender: AgentType,
        recipient: AgentType,
        content: string,
        messageType: MessageType,
        intention?: Intentions
    ): ChatMessage {
        return {
            id: `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
            sender,
            recipient,
            content,
            timestamp: Date.now(),
            messageType,
            intention
        };
    }
}