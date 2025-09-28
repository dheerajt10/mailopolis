import { getWalletKeypair, connection } from "./config";
import { CityStateProgram } from "./cityState";
import { MailLedger } from "./mailLedger";
import { TransactionLedger } from "./transactionLedger";
import { MailopolisMCPServer } from "./mcpServer";

/**
 * Mailopolis Solana Ledger Entry Point
 * 
 * This is the main entry point for the Mailopolis Solana ledger system.
 * It provides access to all ledger functionality including city state,
 * mail system, and transaction tracking.
 */

export class MailopolisLedger {
    private cityState: CityStateProgram;
    private mailLedger: MailLedger;
    private transactionLedger: TransactionLedger;
    private mcpServer: MailopolisMCPServer;

    constructor() {
        this.cityState = new CityStateProgram();
        this.mailLedger = new MailLedger();
        this.transactionLedger = new TransactionLedger();
        this.mcpServer = new MailopolisMCPServer();
    }

    // Get individual ledger components
    getCityState(): CityStateProgram {
        return this.cityState;
    }

    getMailLedger(): MailLedger {
        return this.mailLedger;
    }

    getTransactionLedger(): TransactionLedger {
        return this.transactionLedger;
    }

    getMCPServer(): MailopolisMCPServer {
        return this.mcpServer;
    }

    // Get wallet information
    getWalletInfo() {
        const wallet = getWalletKeypair();
        return {
            publicKey: wallet.publicKey.toString(),
            isConfigured: true
        };
    }

    // Get connection info
    getConnectionInfo() {
        return {
            network: 'devnet',
            rpcUrl: 'https://api.devnet.solana.com'
        };
    }
}

// Export the main ledger class
export default MailopolisLedger;

// Export individual components for direct access
export { CityStateProgram } from "./cityState";
export { MailLedger } from "./mailLedger";
export { TransactionLedger } from "./transactionLedger";
export { MailopolisMCPServer } from "./mcpServer";
export { getWalletKeypair, connection } from "./config";
export * from "./types";