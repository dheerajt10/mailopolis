import { MailLedger } from '../src/mailLedger';

/**
 * Test Mail Ledger functionality
 */
export async function testMailLedger() {
    console.log('Testing Mail Ledger');
    console.log('===================');
    
    try {
        // Test 1: Create MailLedger instance
        console.log('\nTest 1: Creating MailLedger instance...');
        const mailLedger = new MailLedger();
        console.log('✓ MailLedger created successfully');
        
        // Test 2: Get mail account public key
        console.log('\nTest 2: Getting mail account public key...');
        const mailAccount = mailLedger.getMailAccount();
        console.log(`✓ Mail account: ${mailAccount.toString()}`);
        
        // Test 3: Test agent accounts
        console.log('\nTest 3: Getting agent accounts...');
        const allAccounts = mailLedger.getAllAgentAccounts();
        console.log(`✓ Generated ${allAccounts.size} agent accounts`);
        allAccounts.forEach((account, agentType) => {
            console.log(`  ${agentType}: ${account.toString()}`);
        });
        
        // Test 4: Create a test message
        console.log('\nTest 4: Creating test message...');
        const testMessage = mailLedger.createMessage(
            'mayor',
            'finance_chief',
            'Test message for ledger functionality',
            'policy_recommendation',
            'public_service'
        );
        console.log(`✓ Message created with ID: ${testMessage.id}`);
        console.log(`  From: ${testMessage.sender}`);
        console.log(`  To: ${testMessage.recipient}`);
        console.log(`  Content: ${testMessage.content}`);
        console.log(`  Type: ${testMessage.messageType}`);
        console.log(`  Intention: ${testMessage.intention}`);
        
        // Test 5: Record message (local only, no blockchain transaction)
        console.log('\nTest 5: Recording message...');
        const messageSignature = await mailLedger.recordMessage(testMessage);
        console.log(`✓ Message recorded with signature: ${messageSignature}`);
        
        // Test 6: Get message history
        console.log('\nTest 6: Getting message history...');
        const messageHistory = await mailLedger.getMessageHistory();
        console.log(`✓ Retrieved ${messageHistory.length} messages from history`);
        
        // Test 7: Filter messages by sender
        console.log('\nTest 7: Filtering messages by sender...');
        const mayorMessages = await mailLedger.getMessageHistory('mayor');
        console.log(`✓ Mayor has sent ${mayorMessages.length} messages`);
        
        console.log('\n✓ All mail ledger tests completed successfully!');
        
    } catch (error) {
        console.error('✗ Mail ledger test failed:', error);
        throw error;
    }
}

// Run the test
testMailLedger().catch((error) => {
    console.error('Test failed:', error);
    process.exit(1);
});
