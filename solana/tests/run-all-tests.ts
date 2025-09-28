import { testCityState } from './test-city-state';
import { testMailLedger } from './test-mail-ledger';
import { testTransactionLedger } from './test-transaction-ledger';
import { testLedgerIntegration } from './test-ledger-integration';

/**
 * Run all tests for the Mailopolis Solana Ledger
 */
async function runAllTests() {
    console.log('Running All Mailopolis Solana Ledger Tests');
    console.log('==========================================');
    console.log('Note: These tests run without blockchain transactions');
    console.log('They test the logic and data structures only.\n');
    
    const tests = [
        { name: 'City State', fn: testCityState },
        { name: 'Mail Ledger', fn: testMailLedger },
        { name: 'Transaction Ledger', fn: testTransactionLedger },
        { name: 'Ledger Integration', fn: testLedgerIntegration }
    ];
    
    let passed = 0;
    let failed = 0;
    
    for (const test of tests) {
        try {
            console.log(`\n${'='.repeat(50)}`);
            console.log(`Running ${test.name} Tests`);
            console.log(`${'='.repeat(50)}`);
            
            await test.fn();
            console.log(`\n✓ ${test.name} tests PASSED`);
            passed++;
            
        } catch (error) {
            console.error(`\n✗ ${test.name} tests FAILED:`, error.message);
            failed++;
        }
    }
    
    console.log(`\n${'='.repeat(50)}`);
    console.log('Test Summary');
    console.log(`${'='.repeat(50)}`);
    console.log(`✓ Passed: ${passed}`);
    console.log(`✗ Failed: ${failed}`);
    console.log(`Total: ${passed + failed}`);
    
    if (failed > 0) {
        console.log('\nSome tests failed. Check the output above for details.');
        process.exit(1);
    } else {
        console.log('\n🎉 All tests passed successfully!');
        console.log('\nThe Mailopolis Solana Ledger is working as intended.');
        console.log('You can now proceed with blockchain integration when ready.');
    }
}

// Run all tests
runAllTests().catch((error) => {
    console.error('Test runner failed:', error);
    process.exit(1);
});
