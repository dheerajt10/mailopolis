import { CityStateProgram } from './cityState';
import { MailLedger } from './mailLedger';
import { TransactionLedger } from './transactionLedger';
import { ChatMessage, FinancialTransaction, AgentType } from './types';

/**
 * MCP Server for Mailopolis Solana Ledger
 * 
 * This server exposes the Solana ledger functionality to the Python backend.
 * Solana is used ONLY for immutable proof of record - no behavior tracking.
 */
export class MailopolisMCPServer {
    private cityState: CityStateProgram;
    private mailLedger: MailLedger;
    private transactionLedger: TransactionLedger;

    constructor() {
        this.cityState = new CityStateProgram();
        this.mailLedger = new MailLedger();
        this.transactionLedger = new TransactionLedger();
    }

    // ===== CITY STATE METHODS =====
    async initializeCity(initialBudget: number): Promise<string> {
        return await this.cityState.initializeCity(initialBudget);
    }

    async updateCityBudget(newBudget: number): Promise<string> {
        return await this.cityState.updateBudget(newBudget);
    }

    async getCityBudget(): Promise<number> {
        const state = await this.cityState.getCityState();
        return state.cityBudget;
    }

    async getWalletBalance(): Promise<number> {
        return await this.cityState.getWalletBalance();
    }

    // ===== MAIL SYSTEM METHODS =====
    async initializeMailSystem(): Promise<string> {
        return await this.mailLedger.initializeMailSystem();
    }

    async sendMessage(message: ChatMessage): Promise<string> {
        return await this.mailLedger.recordMessage(message);
    }

    async getMessageHistory(sender?: AgentType, recipient?: AgentType): Promise<ChatMessage[]> {
        return await this.mailLedger.getMessageHistory(sender, recipient);
    }

    // ===== TRANSACTION LEDGER METHODS =====
    async initializeTransactionLedger(): Promise<string> {
        return await this.transactionLedger.initializeTransactionLedger();
    }

    async recordFinancialTransaction(transaction: FinancialTransaction): Promise<string> {
        return await this.transactionLedger.recordTransaction(transaction);
    }

    async getTransactionHistory(from?: AgentType, to?: AgentType): Promise<FinancialTransaction[]> {
        return await this.transactionLedger.getTransactionHistory(from, to);
    }

    // ===== ACCOUNT GETTERS =====
    getCityAccount(): string {
        return this.cityState.getCityAccount().toString();
    }

    getMailAccount(): string {
        return this.mailLedger.getMailAccount().toString();
    }

    getTransactionAccount(): string {
        return this.transactionLedger.getTransactionAccount().toString();
    }

    // ===== HELPER METHODS =====
    
    // Create a message with proper typing
    createMessage(
        sender: AgentType,
        recipient: AgentType,
        content: string,
        messageType: 'policy_recommendation' | 'counter_argument' | 'department_update' | 'mayor_decision' | 'bad_actor_lobbying' | 'coalition_building',
        intention?: 'corruption' | 'sustainability' | 'political_gain' | 'public_service' | 'personal_benefit'
    ): ChatMessage {
        return this.mailLedger.createMessage(sender, recipient, content, messageType, intention);
    }

    // Create a transaction with proper typing
    createTransaction(
        from: AgentType,
        to: AgentType,
        amount: number,
        transactionType: 'bribe' | 'campaign_contribution' | 'policy_payment' | 'department_funding' | 'development_approval',
        description: string,
        intention?: 'corruption' | 'sustainability' | 'political_gain' | 'public_service' | 'personal_benefit'
    ): FinancialTransaction {
        return this.transactionLedger.createTransaction(from, to, amount, transactionType, description, intention);
    }

    // ===== LEDGER STATUS =====
    async getLedgerStatus(): Promise<{
        cityBudget: number;
        totalMessages: number;
        totalTransactions: number;
        accounts: {
            city: string;
            mail: string;
            transactions: string;
        };
    }> {
        const cityBudget = await this.getCityBudget();
        const messages = await this.getMessageHistory();
        const transactions = await this.getTransactionHistory();
        
        return {
            cityBudget,
            totalMessages: messages.length,
            totalTransactions: transactions.length,
            accounts: {
                city: this.getCityAccount(),
                mail: this.getMailAccount(),
                transactions: this.getTransactionAccount()
            }
        };
    }
}
