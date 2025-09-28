import { MailopolisLedger } from '../src/index';

/**
 * Test integrated ledger functionality
 */
export async function testLedgerIntegration() {
    console.log('Testing Mailopolis Ledger Integration');
    console.log('=====================================');
    
    try {
        // Test 1: Create main ledger instance
        console.log('\nTest 1: Creating MailopolisLedger instance...');
        const ledger = new MailopolisLedger();
        console.log('✓ MailopolisLedger created successfully');
        
        // Test 2: Get individual components
        console.log('\nTest 2: Getting individual components...');
        const cityState = ledger.getCityState();
        const mailLedger = ledger.getMailLedger();
        const transactionLedger = ledger.getTransactionLedger();
        const mcpServer = ledger.getMCPServer();
        
        console.log('✓ CityState component retrieved');
        console.log('✓ MailLedger component retrieved');
        console.log('✓ TransactionLedger component retrieved');
        console.log('✓ MCPServer component retrieved');
        
        // Test 3: Get wallet information
        console.log('\nTest 3: Getting wallet information...');
        const walletInfo = ledger.getWalletInfo();
        console.log(`✓ Wallet public key: ${walletInfo.publicKey}`);
        console.log(`✓ Wallet configured: ${walletInfo.isConfigured}`);
        
        // Test 4: Get connection information
        console.log('\nTest 4: Getting connection information...');
        const connectionInfo = ledger.getConnectionInfo();
        console.log(`✓ Network: ${connectionInfo.network}`);
        console.log(`✓ RPC URL: ${connectionInfo.rpcUrl}`);
        
        // Test 5: Test MCP Server functionality
        console.log('\nTest 5: Testing MCP Server functionality...');
        
        // Test creating a message through MCP
        const testMessage = mcpServer.createMessage(
            'mayor',
            'finance_chief',
            'Integration test message',
            'policy_recommendation',
            'public_service'
        );
        console.log(`✓ MCP message created: ${testMessage.id}`);
        
        // Test creating a transaction through MCP
        const testTransaction = mcpServer.createTransaction(
            'mayor',
            'finance_chief',
            50.0,
            'department_funding',
            'Integration test transaction',
            'public_service'
        );
        console.log(`✓ MCP transaction created: ${testTransaction.id}`);
        
        // Test 6: Test ledger status
        console.log('\nTest 6: Getting ledger status...');
        const status = await mcpServer.getLedgerStatus();
        console.log(`✓ City budget: ${status.cityBudget} SOL`);
        console.log(`✓ Total messages: ${status.totalMessages}`);
        console.log(`✓ Total transactions: ${status.totalTransactions}`);
        console.log(`✓ City account: ${status.accounts.city}`);
        console.log(`✓ Mail account: ${status.accounts.mail}`);
        console.log(`✓ Transaction account: ${status.accounts.transactions}`);
        
        console.log('\n✓ All integration tests completed successfully!');
        
    } catch (error) {
        console.error('✗ Integration test failed:', error);
        throw error;
    }
}

// Run the test
testLedgerIntegration().catch((error) => {
    console.error('Test failed:', error);
    process.exit(1);
});
