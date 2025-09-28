// Core game types for Mailopolis Solana programs

export interface CityState {
    cityBudget: number;
}

export type Intentions = 
    | 'corruption'
    | 'sustainability'
    | 'political_gain'
    | 'public_service'
    | 'personal_benefit';

export type AgentType = 'mayor'
    | 'power_grid_chief'
    | 'hospital_chief'
    | 'transit_chief'
    | 'finance_chief'
    | 'citizen_representative';

export interface ChatMessage {
  id: string;
  sender: AgentType;
  recipient: AgentType;
  content: string;
  timestamp: number;
  messageType: MessageType;
  intention?: Intentions; // Optional behavior tracking
}

export type MessageType = 
  | 'policy_recommendation'
  | 'counter_argument' 
  | 'department_update'
  | 'mayor_decision'
  | 'bad_actor_lobbying'
  | 'coalition_building';

export interface FinancialTransaction {
  id: string;
  from: AgentType;
  to: AgentType;
  amount: number; // SOL amount
  transactionType: TransactionType;
  timestamp: number;
  description: string;
  intention?: Intentions; // Optional behavior tracking
}

export type TransactionType = 
  | 'bribe'
  | 'campaign_contribution'
  | 'policy_payment'
  | 'department_funding'
  | 'development_approval';

// No behavior tracking needed - Solana is just for immutable proof of record