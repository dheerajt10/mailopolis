import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000'; // Adjust this to match your backend URL

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
});


// Types for API responses
export interface CityStats {
  budget: number;
  sustainability_score: number;
  public_approval: number;
  economic_growth: number;
  infrastructure_health: number;
  population_happiness: number;
  corruption_level: number;
}

export interface GameState {
  turn: number;
  city_stats: CityStats;
  active_events: any[];
  is_game_over: boolean;
}

export interface PolicyProposal {
  id: string;
  title: string;
  description: string;
  proposed_by: string;
  target_department: string;
  sustainability_impact: number;
  economic_impact: number;
  political_impact: number;
  bribe_amount: number;
  created_at: string;
}

export type ProposalSubmission = Pick<
  PolicyProposal,
  | 'title'
  | 'description'
  | 'target_department'
  | 'sustainability_impact'
  | 'economic_impact'
  | 'political_impact'
>;

export interface ProposalSuggestion {
  count: number;
  suggestions: PolicyProposal[];
}

export interface TurnRequest {
  proposal: ProposalSubmission;
}

export interface TurnResponse {
  ok: boolean;
  result: any;
}

export interface AgentPersonality {
  name: string;
  role: string;
  department: string;
  core_values: string[];
  communication_style: string;
  decision_factors: string[];
  traits: {
    corruption_resistance: number;
    sustainability_focus: number;
    political_awareness: number;
    risk_tolerance: number;
  };
}

export interface PersonalitiesResponse {
  ok: boolean;
  count: number;
  personalities: Record<string, AgentPersonality>;
}

// AgentMail inbox types
export interface AgentInboxInfo {
  agent_name: string;
  email_address: string;
  department: string;
  display_name: string;
  created_at: string;
  username: string;
}

export interface AgentInboxesResponse {
  ok: boolean;
  count: number;
  inboxes: AgentInboxInfo[];
  api_status: 'connected' | 'no_api_key';
}

export interface AgentMessage {
  message_id: string;
  subject: string;
  from: string;
  to: string[];
  cc: string[];
  bcc: string[];
  text_content?: string;
  html_content?: string;
  received_at: string;
  thread_id?: string;
  labels?: string[];
  attachments?: Array<{ filename: string; url?: string; contentType?: string }>;
}

export interface AgentInboxResponse {
  ok: boolean;
  agent_name: string;
  email_address: string;
  department: string;
  display_name: string;
  created_at: string;
  username: string;
  recent_messages: AgentMessage[];
  message_count: number;
}

export interface AgentMessagesResponse {
  ok: boolean;
  agent_name: string;
  email_address: string;
  total_messages: number;
  messages: AgentMessage[];
  inbox_info: {
    department: string;
    display_name: string;
    created_at: string;
  };
}

// API service functions
export const apiService = {
  // Start a new game
  async startGame(): Promise<{ ok: boolean; state: unknown }> {
    const response = await apiClient.post('/maylopolis/start');
    return response.data;
  },

  // Get current game state
  async getGameState(): Promise<GameState> {
    const response = await apiClient.get('/maylopolis/state');
    return response.data;
  },

  // Get proposal suggestions
  async getSuggestions(): Promise<ProposalSuggestion> {
    const response = await apiClient.get('/maylopolis/suggestions');
    return response.data;
  },

  // Play a turn by submitting a proposal
  async playTurn(request: TurnRequest): Promise<TurnResponse> {
    const response = await apiClient.post('/maylopolis/turn', request);
    return response.data;
  },

  // Get agent personalities
  async getPersonalities(): Promise<PersonalitiesResponse> {
    const response = await apiClient.get('/maylopolis/personalities');
    return response.data;
  },

  // // Get all agent inboxes
  // async getAgentInboxes(): Promise<AgentInboxesResponse> {
  //   const response = await apiClient.get('/maylopolis/inboxes');
  //   return response.data;
  // },

  // Get a specific agent inbox summary with recent messages
  async getAgentInbox(agentName: string): Promise<AgentInboxResponse> {
    console.log('getAgentInbox in api.ts', agentName);
    const response = await apiClient.get(`/maylopolis/inboxes/${encodeURIComponent(agentName)}`);

    return response.data;
  },

  // Get messages for an agent (optionally limit)
  async getAgentMessages(agentName: string, limit = 20): Promise<AgentMessagesResponse> {
    const response = await apiClient.get(`/maylopolis/inboxes/${encodeURIComponent(agentName)}/messages`, {
      params: { limit, include_content: true },
    });
    return response.data;
  },
};

export default apiService;
