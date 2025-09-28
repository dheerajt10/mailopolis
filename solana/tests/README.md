# Mailopolis Solana Ledger Tests

This directory contains comprehensive tests for the Mailopolis Solana Ledger system. These tests verify that all components work correctly without requiring actual blockchain transactions.

## Test Files

- **`test-city-state.ts`** - Tests the CityStateProgram functionality
- **`test-mail-ledger.ts`** - Tests the MailLedger functionality  
- **`test-transaction-ledger.ts`** - Tests the TransactionLedger functionality
- **`test-ledger-integration.ts`** - Tests the integrated MailopolisLedger system
- **`run-all-tests.ts`** - Runs all tests and provides a summary

## Running Tests

### Run All Tests
```bash
npm test
```

### Run Individual Test Suites
```bash
# Test city state functionality
npm run test:city

# Test mail ledger functionality  
npm run test:mail

# Test transaction ledger functionality
npm run test:transaction

# Test integrated ledger functionality
npm run test:integration
```

### Run Example Usage
```bash
npm run example
```

## What These Tests Verify

### City State Tests
- ✅ CityStateProgram instantiation
- ✅ City account generation
- ✅ Wallet balance retrieval
- ✅ City state data structure
- ✅ Wallet configuration

### Mail Ledger Tests
- ✅ MailLedger instantiation
- ✅ Mail account generation
- ✅ Agent account generation
- ✅ Message creation and typing
- ✅ Message recording (local)
- ✅ Message history retrieval
- ✅ Message filtering by sender/recipient

### Transaction Ledger Tests
- ✅ TransactionLedger instantiation
- ✅ Transaction account generation
- ✅ Agent account generation
- ✅ Transaction creation and typing
- ✅ Transaction recording (local)
- ✅ Transaction history retrieval
- ✅ Transaction filtering by sender/recipient

### Integration Tests
- ✅ MailopolisLedger main class
- ✅ Component access and retrieval
- ✅ Wallet and connection information
- ✅ MCP Server functionality
- ✅ Ledger status reporting
- ✅ Cross-component integration

## Test Philosophy

These tests focus on **logic and data structure validation** rather than blockchain interaction. They verify:

1. **Type Safety** - All TypeScript types work correctly
2. **Data Flow** - Information flows properly between components
3. **Account Generation** - Solana keypairs are generated correctly
4. **Message/Transaction Creation** - Data structures are created properly
5. **Local Storage** - In-memory storage works as expected
6. **Filtering and Queries** - Data retrieval functions work correctly

## Expected Behavior

- All tests should pass without requiring funded wallets
- No actual blockchain transactions are performed
- Tests run quickly and provide immediate feedback
- Clear success/failure indicators for each test
- Comprehensive coverage of all major functionality

## Next Steps

Once these tests pass, you can proceed with:
1. Blockchain integration testing (requires funded wallet)
2. MCP server integration with Python backend
3. Full end-to-end testing with real Solana transactions

## Notes

- Tests use mock transaction signatures for local operations
- No SOL is required to run these tests
- All agent accounts are generated locally
- Message and transaction history is stored in memory
- Tests verify the intended behavior matches the implementation
