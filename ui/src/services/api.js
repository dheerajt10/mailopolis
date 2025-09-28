import axios from 'axios';
const API_BASE_URL = 'http://localhost:8000'; // Adjust this to match your backend URL
const apiClient = axios.create({
    baseURL: API_BASE_URL,
    timeout: 10000,
});
// API service functions
export const apiService = {
    // Start a new game
    async startGame() {
        const response = await apiClient.post('/maylopolis/start');
        return response.data;
    },
    // Get current game state
    async getGameState() {
        const response = await apiClient.get('/maylopolis/state');
        return response.data;
    },
    // Get proposal suggestions
    async getSuggestions() {
        const response = await apiClient.get('/maylopolis/suggestions');
        return response.data;
    },
    // Play a turn by submitting a proposal
    async playTurn(request) {
        const response = await apiClient.post('/maylopolis/turn', request);
        return response.data;
    },
    // Get agent personalities
    async getPersonalities() {
        const response = await apiClient.get('/maylopolis/personalities');
        return response.data;
    },
};
export default apiService;
