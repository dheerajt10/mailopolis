import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { 
  Wifi, 
  WifiOff, 
  Bell, 
  User, 
  Clock,
  Zap,
  TrendingUp,
  AlertTriangle
} from 'lucide-react'
import { useGame } from '../context/GameContext'

const HUD = ({ isConnected }) => {
  const { 
    sustainabilityIndex,
    mayorTrust,
    roundNumber,
    maxRounds,
    unreadCount,
    notifications 
  } = useGame()

  const [currentTime, setCurrentTime] = useState(new Date())

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTime(new Date())
    }, 1000)

    return () => clearInterval(timer)
  }, [])

  const formatTime = (date) => {
    return date.toLocaleTimeString('en-US', { 
      hour12: false, 
      hour: '2-digit', 
      minute: '2-digit',
      second: '2-digit'
    })
  }

  const getStatusColor = () => {
    if (sustainabilityIndex >= 70) return 'cyber-green'
    if (sustainabilityIndex >= 50) return 'cyber-yellow'
    if (sustainabilityIndex >= 30) return 'orange-400'
    return 'cyber-red'
  }

  const getThreatLevel = () => {
    if (sustainabilityIndex >= 70) return { level: 'LOW', color: 'cyber-green' }
    if (sustainabilityIndex >= 50) return { level: 'MEDIUM', color: 'cyber-yellow' }
    if (sustainabilityIndex >= 30) return { level: 'HIGH', color: 'orange-400' }
    return { level: 'CRITICAL', color: 'cyber-red' }
  }

  const threat = getThreatLevel()

  return (
    <motion.div
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      className="fixed top-0 left-0 right-0 z-30 bg-dark-card/90 backdrop-blur-lg border-b border-cyber-blue/30"
    >
      <div className="flex items-center justify-between px-4 py-2 lg:px-6">
        {/* Left section - Game status */}
        <div className="flex items-center gap-6">
          {/* Connection status */}
          <div className="flex items-center gap-2">
            {isConnected ? (
              <Wifi size={16} className="text-cyber-green" />
            ) : (
              <WifiOff size={16} className="text-cyber-red" />
            )}
            <span className={`text-xs cyber-text ${isConnected ? 'text-cyber-green' : 'text-cyber-red'}`}>
              {isConnected ? 'ONLINE' : 'OFFLINE'}
            </span>
          </div>

          {/* Round counter */}
          <div className="hidden sm:flex items-center gap-2">
            <Clock size={16} className="text-cyber-blue" />
            <span className="cyber-text text-sm text-cyber-blue">
              R{roundNumber}/{maxRounds}
            </span>
          </div>

          {/* Sustainability status */}
          <div className="hidden md:flex items-center gap-2">
            <Zap size={16} className={`text-${getStatusColor()}`} />
            <span className={`cyber-text text-sm text-${getStatusColor()}`}>
              SUS: {Math.round(sustainabilityIndex)}%
            </span>
          </div>

          {/* Threat level */}
          <div className="hidden lg:flex items-center gap-2">
            <AlertTriangle size={16} className={`text-${threat.color}`} />
            <span className={`cyber-text text-xs text-${threat.color}`}>
              THREAT: {threat.level}
            </span>
          </div>
        </div>

        {/* Center section - Time */}
        <div className="flex items-center gap-2">
          <div className="cyber-text text-sm text-cyber-blue">
            {formatTime(currentTime)}
          </div>
        </div>

        {/* Right section - User and notifications */}
        <div className="flex items-center gap-4">
          {/* Mayor trust indicator */}
          <div className="hidden sm:flex items-center gap-2">
            <TrendingUp size={16} className={mayorTrust >= 50 ? 'text-cyber-green' : 'text-cyber-red'} />
            <span className={`cyber-text text-sm ${mayorTrust >= 50 ? 'text-cyber-green' : 'text-cyber-red'}`}>
              TRUST: {Math.round(mayorTrust)}%
            </span>
          </div>

          {/* Notifications */}
          <div className="relative">
            <button className="p-2 hover:bg-white/5 rounded-lg transition-colors relative">
              <Bell size={18} className="text-gray-400" />
              {unreadCount > 0 && (
                <motion.span
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  className="absolute -top-1 -right-1 w-5 h-5 bg-cyber-red text-white text-xs rounded-full flex items-center justify-center cyber-text"
                >
                  {unreadCount > 9 ? '9+' : unreadCount}
                </motion.span>
              )}
            </button>
          </div>

          {/* User profile */}
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-full bg-gradient-to-br from-cyber-blue to-cyber-purple flex items-center justify-center">
              <User size={16} className="text-white" />
            </div>
            <span className="hidden sm:block cyber-text text-sm text-gray-300">
              STRATEGIST
            </span>
          </div>
        </div>
      </div>

      {/* Real-time data stream indicator */}
      <motion.div
        className="absolute bottom-0 left-0 h-0.5 bg-gradient-to-r from-cyber-blue via-cyber-purple to-cyber-green"
        animate={{
          x: ['-100%', '100%'],
        }}
        transition={{
          duration: 3,
          repeat: Infinity,
          ease: 'linear',
        }}
        style={{ width: '20%' }}
      />
    </motion.div>
  )
}

export default HUD