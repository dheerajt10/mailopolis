import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { 
  Activity, 
  TrendingUp, 
  TrendingDown, 
  Target, 
  Shield, 
  Zap,
  Users,
  Building,
  Droplets,
  Truck,
  DollarSign
} from 'lucide-react'

import { useGame } from '../context/GameContext'
import SustainabilityMeter from './SustainabilityMeter'
import DepartmentGrid from './DepartmentGrid'
import QuickStats from './QuickStats'
import AlertsPanel from './AlertsPanel'
import TrendChart from './TrendChart'

const GameDashboard = () => {
  const { 
    sustainabilityIndex,
    departments,
    mayorTrust,
    badActorInfluence,
    roundNumber,
    maxRounds,
    loading,
    loadGameData
  } = useGame()

  const [trendData, setTrendData] = useState([])

  useEffect(() => {
    loadGameData()
    
    // Generate mock trend data for visualization
    const mockTrends = Array.from({ length: 10 }, (_, i) => ({
      round: i + 1,
      sustainability: Math.max(20, Math.min(80, 50 + Math.sin(i * 0.5) * 15 + Math.random() * 10)),
      mayorTrust: Math.max(10, Math.min(90, 50 + Math.cos(i * 0.7) * 20 + Math.random() * 10)),
      badActorInfluence: Math.max(5, Math.min(70, 30 + Math.sin(i * 0.3) * 15 + Math.random() * 8))
    }))
    setTrendData(mockTrends)
  }, [loadGameData])

  const gameProgress = (roundNumber / maxRounds) * 100
  const isWinning = sustainabilityIndex > 60
  const isCritical = sustainabilityIndex < 30

  const departmentIcons = {
    'ENERGY': Zap,
    'TRANSPORTATION': Truck,
    'HOUSING': Building,
    'WASTE': Shield,
    'WATER': Droplets,
    'ECONOMIC_DEV': DollarSign
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <motion.div
          className="cyber-text text-2xl"
          animate={{ opacity: [0.5, 1, 0.5] }}
          transition={{ duration: 2, repeat: Infinity }}
        >
          Initializing Game Systems<span className="loading-dots"></span>
        </motion.div>
      </div>
    )
  }

  return (
    <div className="container mx-auto px-4 space-y-6">
      {/* Header Section */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center mb-8"
      >
        <h1 className="cyber-text text-4xl font-bold mb-4 text-cyber-blue animate-glow">
          Strategic Command Center
        </h1>
        <p className="text-xl text-gray-300">
          Round {roundNumber} of {maxRounds} • {isWinning ? 'Winning' : isCritical ? 'Critical' : 'Fighting'} 
          <span className="ml-2">
            {isWinning ? '🏆' : isCritical ? '⚠️' : '⚔️'}
          </span>
        </p>
      </motion.div>

      {/* Main Metrics Row */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        {/* Sustainability Index - Main Metric */}
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.1 }}
          className="lg:col-span-2"
        >
          <SustainabilityMeter 
            value={sustainabilityIndex}
            trend={trendData.length > 1 ? 
              sustainabilityIndex - trendData[trendData.length - 2].sustainability : 0
            }
            size="large"
          />
        </motion.div>

        {/* Key Metrics */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.2 }}
          className="space-y-4"
        >
          <QuickStats 
            mayorTrust={mayorTrust}
            badActorInfluence={badActorInfluence}
            roundsRemaining={maxRounds - roundNumber}
          />
        </motion.div>
      </div>

      {/* Departments Grid */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        className="mb-8"
      >
        <DepartmentGrid 
          departments={departments}
          icons={departmentIcons}
        />
      </motion.div>

      {/* Bottom Row: Trends and Alerts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Trend Analysis */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.4 }}
        >
          <TrendChart 
            data={trendData}
            title="Performance Trends"
          />
        </motion.div>

        {/* Real-time Alerts */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.5 }}
        >
          <AlertsPanel 
            sustainabilityIndex={sustainabilityIndex}
            mayorTrust={mayorTrust}
            badActorInfluence={badActorInfluence}
            departments={departments}
          />
        </motion.div>
      </div>

      {/* Game Progress Bar */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.6 }}
        className="mt-8"
      >
        <div className="data-card rounded-lg p-6">
          <div className="flex justify-between items-center mb-3">
            <h3 className="cyber-text text-lg font-semibold text-cyber-blue">
              Game Progress
            </h3>
            <span className="text-sm text-gray-400">
              {Math.round(gameProgress)}% Complete
            </span>
          </div>
          
          <div className="relative h-4 bg-dark-bg rounded-full overflow-hidden neon-border">
            <motion.div
              className="h-full bg-gradient-to-r from-cyber-blue to-cyber-purple"
              initial={{ width: 0 }}
              animate={{ width: `${gameProgress}%` }}
              transition={{ duration: 1, delay: 0.7 }}
            />
            
            {/* Pulse effect */}
            <motion.div
              className="absolute top-0 right-0 h-full w-2 bg-white opacity-75"
              animate={{ 
                x: [0, -10, 0],
                opacity: [0.75, 1, 0.75] 
              }}
              transition={{ 
                duration: 2, 
                repeat: Infinity,
                ease: "easeInOut"
              }}
            />
          </div>
          
          <div className="flex justify-between mt-2 text-sm text-gray-400">
            <span>Round {roundNumber}</span>
            <span>Final Round: {maxRounds}</span>
          </div>
        </div>
      </motion.div>

      {/* Action Buttons */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.7 }}
        className="flex flex-wrap gap-4 justify-center mt-8"
      >
        <button 
          className="cyber-button flex items-center gap-2"
          onClick={() => window.location.hash = '/policy'}
        >
          <Target size={18} />
          Create Policy
        </button>
        
        <button 
          className="cyber-button flex items-center gap-2"
          onClick={() => window.location.hash = '/agentmail'}
        >
          <Users size={18} />
          AgentMail
        </button>
        
        <button 
          className="cyber-button flex items-center gap-2"
          onClick={() => window.location.hash = '/blockchain'}
        >
          <Activity size={18} />
          Blockchain Intel
        </button>
      </motion.div>

      {/* Floating Action Button for Quick Actions */}
      <motion.div
        className="fixed bottom-8 right-8 z-50"
        initial={{ scale: 0, rotate: -180 }}
        animate={{ scale: 1, rotate: 0 }}
        transition={{ delay: 1, type: "spring" }}
      >
        <button 
          className="bg-cyber-blue text-dark-bg p-4 rounded-full shadow-lg neon-glow hover:bg-cyber-purple transition-all duration-300"
          onClick={loadGameData}
          title="Refresh Game Data"
        >
          <Activity size={24} />
        </button>
      </motion.div>
    </div>
  )
}

export default GameDashboard