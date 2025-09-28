import axios from 'axios'

// Configure axios instance
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: `${API_BASE_URL}/api`,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor for adding auth or logging
api.interceptors.request.use(
  (config) => {
    console.log(`🚀 API Request: ${config.method?.toUpperCase()} ${config.url}`)
    return config
  },
  (error) => {
    console.error('❌ API Request Error:', error)
    return Promise.reject(error)
  }
)

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    console.log(`✅ API Response: ${response.status} ${response.config.url}`)
    return response
  },
  (error) => {
    console.error('❌ API Response Error:', error.response?.data || error.message)
    
    // Handle specific error cases
    if (error.response?.status === 503) {
      throw new Error('Game server is temporarily unavailable. Please try again.')
    } else if (error.response?.status >= 500) {
      throw new Error('Server error occurred. Please try again later.')
    } else if (error.response?.status === 429) {
      throw new Error('Too many requests. Please slow down.')
    }
    
    throw error
  }
)

export class GameService {
  static async initialize() {
    try {
      // Test connection with the root endpoint (not API)
      const rootResponse = await axios.get(`${API_BASE_URL}/`)
      console.log('🎮 Backend connection:', rootResponse.data)
      
      // Initialize game state
      const gameResponse = await api.get('/game/state')
      console.log('🎮 Game service initialized:', gameResponse.data)
      return gameResponse.data
    } catch (error) {
      console.error('Failed to initialize game service:', error)
      throw error
    }
  }

  // Game state endpoints
  static async getGameState() {
    const response = await api.get('/game/state')
    return response.data
  }

  static async getDepartments() {
    const response = await api.get('/departments')
    return response.data
  }

  static async getBadActors() {
    const response = await api.get('/bad-actors')
    return response.data
  }

  static async getBlockchainAnalysis() {
    const response = await api.get('/blockchain/analysis')
    return response.data
  }

  // Game actions
  static async startNewRound() {
    const response = await api.get('/round/start')
    return response.data
  }

  static async submitProposal(title, description, targetDepartment, sustainabilityImpact = 5) {
    const response = await api.post('/proposals/submit', {
      title,
      description,
      target_department: targetDepartment,
      sustainability_impact: sustainabilityImpact,
      economic_impact: 0,
      political_impact: 0
    })
    return response.data
  }

  static async requestMayorDecision() {
    const response = await api.post('/mayor/decide')
    return response.data
  }

  // AgentMail endpoints (simulated for now)
  static async getMessages() {
    // Simulate fetching messages - in real implementation this would be an API endpoint
    return {
      messages: [
        {
          id: '1',
          from: 'Mayor',
          to: 'Player',
          subject: 'Welcome to Mailopolis',
          content: 'I look forward to working with you to improve our city\'s sustainability. Please submit your first policy recommendations.',
          timestamp: new Date().toISOString(),
          read: false,
          priority: 'high'
        },
        {
          id: '2',
          from: 'Energy Department',
          to: 'Player',
          subject: 'Current Energy Infrastructure',
          content: 'Our current renewable energy adoption is at 45%. We need urgent investment in solar and wind infrastructure.',
          timestamp: new Date(Date.now() - 3600000).toISOString(),
          read: false,
          priority: 'medium'
        }
      ]
    }
  }

  static async sendMessage(to, subject, content) {
    // Simulate sending message - in real implementation this would be an API endpoint
    return {
      success: true,
      messageId: `msg_${Date.now()}`,
      message: 'Message sent successfully'
    }
  }

  // Analytics and insights
  static async getPlayerMetrics() {
    return {
      proposalsSubmitted: 5,
      proposalsAccepted: 3,
      trustGained: 15,
      sustainabilityImprovement: 12,
      badActorsDefeated: 2
    }
  }

  static async getPredictions() {
    return {
      nextRoundOutlook: 'positive',
      riskAreas: ['Transportation', 'Housing'],
      opportunities: ['Energy', 'Water'],
      confidenceScore: 0.76
    }
  }

  // Real-time updates (polling fallback)
  static async pollForUpdates() {
    try {
      const [gameState, departments] = await Promise.all([
        this.getGameState(),
        this.getDepartments()
      ])
      
      return {
        gameState,
        departments: departments.departments
      }
    } catch (error) {
      console.warn('Failed to poll for updates:', error)
      return null
    }
  }
}

export { api }