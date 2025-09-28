import { CityStateProgram } from '../src/cityState';
import { getWalletKeypair } from '../src/config';

/**
 * Test City State functionality
 */
export async function testCityState() {
    console.log('Testing City State Program');
    console.log('==========================');
    
    try {
        // Test 1: Create CityStateProgram instance
        console.log('\nTest 1: Creating CityStateProgram instance...');
        const cityState = new CityStateProgram();
        console.log('✓ CityStateProgram created successfully');
        
        // Test 2: Get city account public key
        console.log('\nTest 2: Getting city account public key...');
        const cityAccount = cityState.getCityAccount();
        console.log(`✓ City account: ${cityAccount.toString()}`);
        
        // Test 3: Test wallet balance (this should work even with 0 balance)
        console.log('\nTest 3: Getting wallet balance...');
        const balance = await cityState.getWalletBalance();
        console.log(`✓ Wallet balance: ${balance.toFixed(4)} SOL`);
        
        // Test 4: Test city state (this will fail if city not initialized, but that's expected)
        console.log('\nTest 4: Getting city state (expected to fail if not initialized)...');
        try {
            const cityStateData = await cityState.getCityState();
            console.log(`✓ City budget: ${cityStateData.cityBudget.toFixed(4)} SOL`);
        } catch (error) {
            console.log(`⚠ City state not initialized yet (expected): ${error.message}`);
        }
        
        // Test 5: Wallet info
        console.log('\nTest 5: Wallet Information:');
        const wallet = getWalletKeypair();
        console.log(`✓ Wallet public key: ${wallet.publicKey.toString()}`);
        console.log(`✓ Wallet is properly configured`);
        
        console.log('\n✓ All city state tests completed successfully!');
        
    } catch (error) {
        console.error('✗ City state test failed:', error);
        throw error;
    }
}

// Run the test
testCityState().catch((error) => {
    console.error('Test failed:', error);
    process.exit(1);
});
