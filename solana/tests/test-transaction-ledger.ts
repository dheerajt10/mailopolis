import { TransactionLedger } from '../src/transactionLedger';

/**
 * Test Transaction Ledger functionality
 */
export async function testTransactionLedger() {
    console.log('Testing Transaction Ledger');
    console.log('==========================');
    
    try {
        // Test 1: Create TransactionLedger instance
        console.log('\nTest 1: Creating TransactionLedger instance...');
        const transactionLedger = new TransactionLedger();
        console.log('✓ TransactionLedger created successfully');
        
        // Test 2: Get transaction account public key
        console.log('\nTest 2: Getting transaction account public key...');
        const transactionAccount = transactionLedger.getTransactionAccount();
        console.log(`✓ Transaction account: ${transactionAccount.toString()}`);
        
        // Test 3: Test agent accounts
        console.log('\nTest 3: Getting agent accounts...');
        const allAccounts = transactionLedger.getAllAgentAccounts();
        console.log(`✓ Generated ${allAccounts.size} agent accounts`);
        allAccounts.forEach((account, agentType) => {
            console.log(`  ${agentType}: ${account.toString()}`);
        });
        
        // Test 4: Create a test transaction
        console.log('\nTest 4: Creating test transaction...');
        const testTransaction = transactionLedger.createTransaction(
            'mayor',
            'finance_chief',
            100.0,
            'department_funding',
            'Test transaction for ledger functionality',
            'public_service'
        );
        console.log(`✓ Transaction created with ID: ${testTransaction.id}`);
        console.log(`  From: ${testTransaction.from}`);
        console.log(`  To: ${testTransaction.to}`);
        console.log(`  Amount: ${testTransaction.amount} SOL`);
        console.log(`  Type: ${testTransaction.transactionType}`);
        console.log(`  Description: ${testTransaction.description}`);
        console.log(`  Intention: ${testTransaction.intention}`);
        
        // Test 5: Record transaction (local only, no blockchain transaction)
        console.log('\nTest 5: Recording transaction...');
        const transactionSignature = await transactionLedger.recordTransaction(testTransaction);
        console.log(`✓ Transaction recorded with signature: ${transactionSignature}`);
        
        // Test 6: Get transaction history
        console.log('\nTest 6: Getting transaction history...');
        const transactionHistory = await transactionLedger.getTransactionHistory();
        console.log(`✓ Retrieved ${transactionHistory.length} transactions from history`);
        
        // Test 7: Filter transactions by sender
        console.log('\nTest 7: Filtering transactions by sender...');
        const mayorTransactions = await transactionLedger.getTransactionHistory('mayor');
        console.log(`✓ Mayor has made ${mayorTransactions.length} transactions`);
        
        // Test 8: Filter transactions by recipient
        console.log('\nTest 8: Filtering transactions by recipient...');
        const financeTransactions = await transactionLedger.getTransactionHistory(undefined, 'finance_chief');
        console.log(`✓ Finance chief has received ${financeTransactions.length} transactions`);
        
        console.log('\n✓ All transaction ledger tests completed successfully!');
        
    } catch (error) {
        console.error('✗ Transaction ledger test failed:', error);
        throw error;
    }
}

// Run the test
testTransactionLedger().catch((error) => {
    console.error('Test failed:', error);
    process.exit(1);
});
