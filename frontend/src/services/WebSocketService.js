import { io } from 'socket.io-client'

class WebSocketServiceClass {
  constructor() {
    this.socket = null
    this.connected = false
    this.reconnectAttempts = 0
    this.maxReconnectAttempts = 5
    this.reconnectDelay = 1000
    this.eventListeners = new Map()
  }

  connect(url) {
    if (this.socket?.connected) {
      console.log('🔗 WebSocket already connected')
      return
    }

    // Use environment variable or default
    const wsUrl = url || import.meta.env.VITE_WS_URL || 'ws://localhost:8000'

    console.log('🔌 Connecting to WebSocket server...')

    try {
      this.socket = io(wsUrl, {
        transports: ['websocket', 'polling'],
        upgrade: true,
        rememberUpgrade: true,
        timeout: 10000,
      })

      this.setupEventHandlers()
    } catch (error) {
      console.error('❌ WebSocket connection failed:', error)
      this.handleReconnection()
    }
  }

  setupEventHandlers() {
    if (!this.socket) return

    this.socket.on('connect', () => {
      console.log('✅ WebSocket connected successfully')
      this.connected = true
      this.reconnectAttempts = 0
      this.emit('connect')
    })

    this.socket.on('disconnect', (reason) => {
      console.log('🔌 WebSocket disconnected:', reason)
      this.connected = false
      this.emit('disconnect', reason)
      
      if (reason === 'io server disconnect') {
        // Server initiated disconnect, don't reconnect automatically
        return
      }
      
      this.handleReconnection()
    })

    this.socket.on('connect_error', (error) => {
      console.error('❌ WebSocket connection error:', error)
      this.handleReconnection()
    })

    // Game-specific events
    this.socket.on('game_state_update', (data) => {
      console.log('🎮 Game state update received:', data)
      this.emit('game_update', data)
    })

    this.socket.on('new_message', (data) => {
      console.log('📧 New AgentMail message:', data)
      this.emit('new_message', data)
    })

    this.socket.on('proposal_decision', (data) => {
      console.log('📝 Proposal decision:', data)
      this.emit('proposal_result', data)
    })

    this.socket.on('round_started', (data) => {
      console.log('🎯 New round started:', data)
      this.emit('round_start', data)
    })

    this.socket.on('bad_actor_action', (data) => {
      console.log('⚠️ Bad actor action:', data)
      this.emit('bad_actor_move', data)
    })

    this.socket.on('sustainability_change', (data) => {
      console.log('🌱 Sustainability index changed:', data)
      this.emit('sustainability_update', data)
    })

    this.socket.on('blockchain_transaction', (data) => {
      console.log('🔗 New blockchain transaction:', data)
      this.emit('blockchain_update', data)
    })
  }

  handleReconnection() {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      console.error('❌ Max reconnection attempts reached')
      this.emit('max_reconnect_attempts')
      return
    }

    this.reconnectAttempts++
    const delay = this.reconnectDelay * Math.pow(2, this.reconnectAttempts - 1) // Exponential backoff

    console.log(`🔄 Attempting to reconnect (${this.reconnectAttempts}/${this.maxReconnectAttempts}) in ${delay}ms...`)

    setTimeout(() => {
      this.connect()
    }, delay)
  }

  disconnect() {
    if (this.socket) {
      console.log('🔌 Disconnecting WebSocket...')
      this.socket.disconnect()
      this.socket = null
      this.connected = false
    }
  }

  // Event system for components to listen to WebSocket events
  on(event, callback) {
    if (!this.eventListeners.has(event)) {
      this.eventListeners.set(event, new Set())
    }
    this.eventListeners.get(event).add(callback)
  }

  off(event, callback = null) {
    if (!this.eventListeners.has(event)) return

    if (callback) {
      this.eventListeners.get(event).delete(callback)
    } else {
      this.eventListeners.delete(event)
    }
  }

  emit(event, data = null) {
    if (!this.eventListeners.has(event)) return

    this.eventListeners.get(event).forEach(callback => {
      try {
        callback(data)
      } catch (error) {
        console.error(`❌ Error in event listener for ${event}:`, error)
      }
    })
  }

  // Send data to server
  send(event, data) {
    if (!this.connected || !this.socket) {
      console.warn('⚠️ Cannot send data: WebSocket not connected')
      return false
    }

    try {
      this.socket.emit(event, data)
      console.log(`📤 Sent event: ${event}`, data)
      return true
    } catch (error) {
      console.error('❌ Failed to send WebSocket message:', error)
      return false
    }
  }

  // Utility methods
  isConnected() {
    return this.connected && this.socket?.connected
  }

  getConnectionStatus() {
    return {
      connected: this.connected,
      reconnectAttempts: this.reconnectAttempts,
      socketId: this.socket?.id
    }
  }

  // Game-specific helper methods
  joinGameRoom(gameId) {
    this.send('join_game', { gameId })
  }

  leaveGameRoom(gameId) {
    this.send('leave_game', { gameId })
  }

  sendPlayerAction(action, data) {
    this.send('player_action', { action, data })
  }

  requestGameUpdate() {
    this.send('request_update', {})
  }
}

// Create singleton instance
export const WebSocketService = new WebSocketServiceClass()

// Fallback polling service for when WebSocket is not available
export class PollingService {
  constructor(interval = 5000) {
    this.interval = interval
    this.polling = false
    this.pollTimer = null
    this.callbacks = new Map()
  }

  start(pollCallback) {
    if (this.polling) return

    console.log('📡 Starting polling service...')
    this.polling = true
    this.pollCallback = pollCallback

    this.poll()
  }

  stop() {
    if (!this.polling) return

    console.log('⏹️ Stopping polling service...')
    this.polling = false
    
    if (this.pollTimer) {
      clearTimeout(this.pollTimer)
      this.pollTimer = null
    }
  }

  async poll() {
    if (!this.polling) return

    try {
      if (this.pollCallback) {
        await this.pollCallback()
      }
    } catch (error) {
      console.warn('⚠️ Polling error:', error)
    }

    if (this.polling) {
      this.pollTimer = setTimeout(() => this.poll(), this.interval)
    }
  }

  isPolling() {
    return this.polling
  }
}