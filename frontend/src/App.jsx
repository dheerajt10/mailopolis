import React, { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import { motion, AnimatePresence } from 'framer-motion'

// Components
import GameDashboard from './components/GameDashboard'
import AgentMail from './components/AgentMail'
import BlockchainExplorer from './components/BlockchainExplorer'
import PolicyCreator from './components/PolicyCreator'
import BadActorIntel from './components/BadActorIntel'
import Navigation from './components/Navigation'
import HUD from './components/HUD'
import WelcomeScreen from './components/WelcomeScreen'

// Services
import { GameService } from './services/GameService'
import { WebSocketService } from './services/WebSocketService'

// Context
import { GameProvider } from './context/GameContext'

function App() {
  const [gameStarted, setGameStarted] = useState(false)
  const [isConnected, setIsConnected] = useState(false)

  useEffect(() => {
    // Initialize services
    const initializeServices = async () => {
      try {
        await GameService.initialize()
        WebSocketService.connect()
        
        WebSocketService.on('connect', () => {
          setIsConnected(true)
        })
        
        WebSocketService.on('disconnect', () => {
          setIsConnected(false)
        })
        
      } catch (error) {
        console.error('Failed to initialize services:', error)
      }
    }

    initializeServices()

    return () => {
      WebSocketService.disconnect()
    }
  }, [])

  const handleGameStart = () => {
    setGameStarted(true)
  }

  if (!gameStarted) {
    return <WelcomeScreen onStart={handleGameStart} />
  }

  return (
    <GameProvider>
      <Router>
        <div className="min-h-screen bg-dark-bg text-white overflow-hidden relative">
          {/* Animated Background */}
          <div className="fixed inset-0 z-0">
            <div className="absolute inset-0 bg-cyber-gradient"></div>
            <div className="absolute inset-0 bg-cyber-grid bg-[size:50px_50px] animate-circuit opacity-20"></div>
            <div className="matrix-rain absolute inset-0"></div>
          </div>

          {/* Main Game Interface */}
          <div className="relative z-10 min-h-screen">
            {/* HUD - Always visible */}
            <HUD isConnected={isConnected} />

            {/* Navigation */}
            <Navigation />

            {/* Main Content */}
            <main className="pt-20 pb-4 px-4">
              <AnimatePresence mode="wait">
                <Routes>
                  <Route 
                    path="/" 
                    element={
                      <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -20 }}
                        transition={{ duration: 0.3 }}
                      >
                        <GameDashboard />
                      </motion.div>
                    } 
                  />
                  <Route 
                    path="/agentmail" 
                    element={
                      <motion.div
                        initial={{ opacity: 0, x: 20 }}
                        animate={{ opacity: 1, x: 0 }}
                        exit={{ opacity: 0, x: -20 }}
                        transition={{ duration: 0.3 }}
                      >
                        <AgentMail />
                      </motion.div>
                    } 
                  />
                  <Route 
                    path="/blockchain" 
                    element={
                      <motion.div
                        initial={{ opacity: 0, scale: 0.95 }}
                        animate={{ opacity: 1, scale: 1 }}
                        exit={{ opacity: 0, scale: 1.05 }}
                        transition={{ duration: 0.3 }}
                      >
                        <BlockchainExplorer />
                      </motion.div>
                    } 
                  />
                  <Route 
                    path="/policy" 
                    element={
                      <motion.div
                        initial={{ opacity: 0, y: 30 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -30 }}
                        transition={{ duration: 0.3 }}
                      >
                        <PolicyCreator />
                      </motion.div>
                    } 
                  />
                  <Route 
                    path="/intel" 
                    element={
                      <motion.div
                        initial={{ opacity: 0, rotateY: 5 }}
                        animate={{ opacity: 1, rotateY: 0 }}
                        exit={{ opacity: 0, rotateY: -5 }}
                        transition={{ duration: 0.3 }}
                      >
                        <BadActorIntel />
                      </motion.div>
                    } 
                  />
                </Routes>
              </AnimatePresence>
            </main>
          </div>

          {/* Toast notifications */}
          <Toaster
            position="top-right"
            toastOptions={{
              duration: 4000,
              style: {
                background: 'rgba(26, 26, 46, 0.9)',
                color: '#ffffff',
                border: '1px solid rgba(0, 255, 255, 0.3)',
                backdropFilter: 'blur(10px)',
              },
              success: {
                iconTheme: {
                  primary: '#00ff88',
                  secondary: '#0a0a0f',
                },
              },
              error: {
                iconTheme: {
                  primary: '#ff0055',
                  secondary: '#0a0a0f',
                },
              },
            }}
          />
        </div>
      </Router>
    </GameProvider>
  )
}

export default App