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
};

export default apiService;
