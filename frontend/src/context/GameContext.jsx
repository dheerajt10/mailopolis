import React, { createContext, useContext, useReducer, useEffect } from 'react'
import { GameService } from '../services/GameService'
import { WebSocketService } from '../services/WebSocketService'
import toast from 'react-hot-toast'

// Initial game state
const initialState = {
  // Game metrics
  sustainabilityIndex: 50,
  mayorTrust: 50,
  badActorInfluence: 30,
  roundNumber: 1,
  maxRounds: 25,
  
  // Departments
  departments: [
    { name: 'Energy', sustainability_score: 50, id: 'ENERGY' },
    { name: 'Transportation', sustainability_score: 50, id: 'TRANSPORTATION' },
    { name: 'Housing & Development', sustainability_score: 50, id: 'HOUSING' },
    { name: 'Waste Management', sustainability_score: 50, id: 'WASTE' },
    { name: 'Water Systems', sustainability_score: 50, id: 'WATER' },
    { name: 'Economic Development', sustainability_score: 50, id: 'ECONOMIC_DEV' }
  ],
  
  // Bad actors
  badActors: [],
  
  // Blockchain
  blockchainTransactions: [],
  
  // AgentMail
  messages: [],
  unreadCount: 0,
  
  // Proposals
  pendingProposals: [],
  submittedProposals: [],
  
  // UI state
  loading: false,
  error: null,
  notifications: []
}

// Action types
const actionTypes = {
  SET_LOADING: 'SET_LOADING',
  SET_ERROR: 'SET_ERROR',
  UPDATE_GAME_STATE: 'UPDATE_GAME_STATE',
  UPDATE_DEPARTMENTS: 'UPDATE_DEPARTMENTS',
  UPDATE_BAD_ACTORS: 'UPDATE_BAD_ACTORS',
  ADD_MESSAGE: 'ADD_MESSAGE',
  MARK_MESSAGES_READ: 'MARK_MESSAGES_READ',
  ADD_PROPOSAL: 'ADD_PROPOSAL',
  UPDATE_BLOCKCHAIN: 'UPDATE_BLOCKCHAIN',
  ADD_NOTIFICATION: 'ADD_NOTIFICATION',
  REMOVE_NOTIFICATION: 'REMOVE_NOTIFICATION',
  START_NEW_ROUND: 'START_NEW_ROUND'
}

// Reducer function
function gameReducer(state, action) {
  switch (action.type) {
    case actionTypes.SET_LOADING:
      return { ...state, loading: action.payload }
      
    case actionTypes.SET_ERROR:
      return { ...state, error: action.payload, loading: false }
      
    case actionTypes.UPDATE_GAME_STATE:
      return { 
        ...state, 
        ...action.payload,
        error: null 
      }
      
    case actionTypes.UPDATE_DEPARTMENTS:
      return { 
        ...state, 
        departments: action.payload 
      }
      
    case actionTypes.UPDATE_BAD_ACTORS:
      return { 
        ...state, 
        badActors: action.payload 
      }
      
    case actionTypes.ADD_MESSAGE:
      return { 
        ...state, 
        messages: [action.payload, ...state.messages],
        unreadCount: state.unreadCount + 1
      }
      
    case actionTypes.MARK_MESSAGES_READ:
      return { 
        ...state, 
        unreadCount: 0 
      }
      
    case actionTypes.ADD_PROPOSAL:
      return { 
        ...state, 
        submittedProposals: [action.payload, ...state.submittedProposals]
      }
      
    case actionTypes.UPDATE_BLOCKCHAIN:
      return { 
        ...state, 
        blockchainTransactions: action.payload 
      }
      
    case actionTypes.ADD_NOTIFICATION:
      return { 
        ...state, 
        notifications: [...state.notifications, action.payload] 
      }
      
    case actionTypes.REMOVE_NOTIFICATION:
      return { 
        ...state, 
        notifications: state.notifications.filter(n => n.id !== action.payload) 
      }
      
    case actionTypes.START_NEW_ROUND:
      return { 
        ...state, 
        roundNumber: state.roundNumber + 1,
        pendingProposals: []
      }
      
    default:
      return state
  }
}

// Create context
const GameContext = createContext()

// Provider component
export function GameProvider({ children }) {
  const [state, dispatch] = useReducer(gameReducer, initialState)

  // Initialize game data
  useEffect(() => {
    loadGameData()
  }, [])

  // WebSocket event listeners
  useEffect(() => {
    WebSocketService.on('game_update', (data) => {
      dispatch({ type: actionTypes.UPDATE_GAME_STATE, payload: data })
    })

    WebSocketService.on('new_message', (message) => {
      dispatch({ type: actionTypes.ADD_MESSAGE, payload: message })
      toast.success(`New message from ${message.from}`)
    })

    WebSocketService.on('proposal_result', (result) => {
      const toastMessage = result.accepted 
        ? `Policy "${result.title}" accepted by Mayor!` 
        : `Policy "${result.title}" rejected by Mayor`
      
      if (result.accepted) {
        toast.success(toastMessage)
      } else {
        toast.error(toastMessage)
      }
    })

    WebSocketService.on('round_start', (roundData) => {
      dispatch({ type: actionTypes.START_NEW_ROUND })
      toast(`Round ${roundData.round} begins!`, {
        icon: '🎯',
      })
    })

    WebSocketService.on('bad_actor_move', (move) => {
      toast(`Bad actor alert: ${move.description}`, {
        icon: '⚠️',
      })
    })

    return () => {
      WebSocketService.off('game_update')
      WebSocketService.off('new_message')
      WebSocketService.off('proposal_result')
      WebSocketService.off('round_start')
      WebSocketService.off('bad_actor_move')
    }
  }, [])

  // Action creators
  const actions = {
    async loadGameData() {
      try {
        dispatch({ type: actionTypes.SET_LOADING, payload: true })
        
        const [gameState, departments, badActors, blockchain] = await Promise.all([
          GameService.getGameState(),
          GameService.getDepartments(),
          GameService.getBadActors(),
          GameService.getBlockchainAnalysis()
        ])

        dispatch({ type: actionTypes.UPDATE_GAME_STATE, payload: gameState })
        dispatch({ type: actionTypes.UPDATE_DEPARTMENTS, payload: departments.departments })
        dispatch({ type: actionTypes.UPDATE_BAD_ACTORS, payload: Object.values(badActors.active_bad_actors) })
        dispatch({ type: actionTypes.UPDATE_BLOCKCHAIN, payload: blockchain.transactions || [] })
        
      } catch (error) {
        dispatch({ type: actionTypes.SET_ERROR, payload: error.message })
        toast.error('Failed to load game data')
      } finally {
        dispatch({ type: actionTypes.SET_LOADING, payload: false })
      }
    },

    async submitProposal(title, description, targetDepartment) {
      try {
        dispatch({ type: actionTypes.SET_LOADING, payload: true })
        
        const result = await GameService.submitProposal(title, description, targetDepartment)
        
        dispatch({ 
          type: actionTypes.ADD_PROPOSAL, 
          payload: { 
            id: result.proposal_id, 
            title, 
            description, 
            targetDepartment, 
            timestamp: new Date().toISOString()
          } 
        })
        
        toast.success('Policy proposal submitted to Mayor!')
        return result
        
      } catch (error) {
        toast.error('Failed to submit proposal')
        throw error
      } finally {
        dispatch({ type: actionTypes.SET_LOADING, payload: false })
      }
    },

    async startNewRound() {
      try {
        const result = await GameService.startNewRound()
        dispatch({ type: actionTypes.START_NEW_ROUND })
        toast.success('New round started!')
        return result
      } catch (error) {
        toast.error('Failed to start new round')
        throw error
      }
    },

    markMessagesRead() {
      dispatch({ type: actionTypes.MARK_MESSAGES_READ })
    },

    addNotification(notification) {
      const notificationWithId = { ...notification, id: Date.now() }
      dispatch({ type: actionTypes.ADD_NOTIFICATION, payload: notificationWithId })
      
      // Auto-remove after 5 seconds
      setTimeout(() => {
        dispatch({ type: actionTypes.REMOVE_NOTIFICATION, payload: notificationWithId.id })
      }, 5000)
    }
  }

  // Provide both state and actions
  const value = {
    ...state,
    ...actions,
    dispatch
  }

  return (
    <GameContext.Provider value={value}>
      {children}
    </GameContext.Provider>
  )
}

// Custom hook to use the game context
export function useGame() {
  const context = useContext(GameContext)
  if (!context) {
    throw new Error('useGame must be used within a GameProvider')
  }
  return context
}

// Action types export for direct usage
export { actionTypes }

async function loadGameData() {
  // This function is called from the actions object
}