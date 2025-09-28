import { MailLedger } from './mailLedger';

async function exampleUsage() {
    console.log("Mailopolis Mail Ledger Example");
    console.log("=================================");
    
    try {
        // Initialize the mail ledger
        const mailLedger = new MailLedger();
        
        // Initialize the mail system on Solana
        console.log("\nInitializing mail system...");
        const initSignature = await mailLedger.initializeMailSystem();
        console.log(`Mail system initialized: ${initSignature}`);
        
        // Create some example messages
        console.log("\nCreating example messages...");
        
        // Mayor sends a policy recommendation
        const policyMessage = mailLedger.createMessage(
            'mayor',
            'finance_chief',
            'We need to increase the sustainability budget by 20% for next quarter',
            'policy_recommendation',
            'sustainability'
        );
        
        // Record the message
        const messageSignature1 = await mailLedger.recordMessage(policyMessage);
        console.log(`Policy message recorded: ${messageSignature1}`);
        
        // Finance chief responds with counter argument
        const counterMessage = mailLedger.createMessage(
            'finance_chief',
            'mayor',
            'The budget is already stretched thin. We need to prioritize infrastructure repairs',
            'counter_argument',
            'public_service'
        );
        
        const messageSignature2 = await mailLedger.recordMessage(counterMessage);
        console.log(`Counter message recorded: ${messageSignature2}`);
        
        // Bad actor lobbying (corruption)
        const lobbyingMessage = mailLedger.createMessage(
            'power_grid_chief',
            'mayor',
            'I have some concerns about the renewable energy proposal. Maybe we should reconsider the coal plant expansion',
            'bad_actor_lobbying',
            'corruption'
        );
        
        const messageSignature3 = await mailLedger.recordMessage(lobbyingMessage);
        console.log(`Lobbying message recorded: ${messageSignature3}`);
        
        // Solana is only for immutable proof of record - no behavior tracking needed
        
        // Get message history
        console.log("\nMessage History:");
        const mayorMessages = await mailLedger.getMessageHistory('mayor');
        console.log(`Mayor has sent ${mayorMessages.length} messages`);
        
        const allMessages = await mailLedger.getMessageHistory();
        console.log(`Total messages in system: ${allMessages.length}`);
        
        // Get agent accounts
        console.log("\nAgent Accounts:");
        const allAccounts = mailLedger.getAllAgentAccounts();
        allAccounts.forEach((account, agentType) => {
            console.log(`${agentType}: ${account.toString()}`);
        });
        
        console.log("\nExample completed successfully!");
        
    } catch (error) {
        console.error("Example failed:", error);
        throw error;
    }
}

// Run the example
exampleUsage().catch(console.error);
