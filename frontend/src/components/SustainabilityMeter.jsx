import React from 'react'
import { motion } from 'framer-motion'
import { TrendingUp, TrendingDown, Minus } from 'lucide-react'

const SustainabilityMeter = ({ value, trend = 0, size = 'medium' }) => {
  const getColor = (value) => {
    if (value >= 70) return 'cyber-green'
    if (value >= 50) return 'cyber-yellow'
    if (value >= 30) return 'orange-400'
    return 'cyber-red'
  }

  const getGradient = (value) => {
    if (value >= 70) return 'from-green-500 to-cyber-green'
    if (value >= 50) return 'from-yellow-500 to-cyber-yellow'
    if (value >= 30) return 'from-orange-500 to-orange-400'
    return 'from-red-600 to-cyber-red'
  }

  const getTrendIcon = () => {
    if (trend > 0) return <TrendingUp className="text-cyber-green" size={20} />
    if (trend < 0) return <TrendingDown className="text-cyber-red" size={20} />
    return <Minus className="text-gray-400" size={20} />
  }

  const getTrendColor = () => {
    if (trend > 0) return 'text-cyber-green'
    if (trend < 0) return 'text-cyber-red'
    return 'text-gray-400'
  }

  const sizeClasses = {
    small: 'w-24 h-24',
    medium: 'w-40 h-40',
    large: 'w-64 h-64'
  }

  const textSizes = {
    small: 'text-lg',
    medium: 'text-2xl',
    large: 'text-4xl'
  }

  const circumference = 2 * Math.PI * 45 // radius = 45
  const strokeDasharray = circumference
  const strokeDashoffset = circumference - (value / 100) * circumference

  return (
    <div className="data-card rounded-lg p-6">
      <div className="flex justify-between items-center mb-4">
        <h3 className="cyber-text text-xl font-bold text-cyber-blue">
          City Sustainability Index
        </h3>
        <div className="flex items-center gap-2">
          {getTrendIcon()}
          <span className={`text-sm font-mono ${getTrendColor()}`}>
            {trend > 0 ? '+' : ''}{trend.toFixed(1)}%
          </span>
        </div>
      </div>

      <div className="flex items-center justify-center">
        <div className="relative">
          {/* Outer glow effect */}
          <div className={`absolute inset-0 rounded-full bg-${getColor(value)} opacity-20 blur-xl`}></div>
          
          <svg 
            className={`${sizeClasses[size]} transform -rotate-90`}
            viewBox="0 0 100 100"
          >
            {/* Background circle */}
            <circle
              cx="50"
              cy="50"
              r="45"
              stroke="rgba(255,255,255,0.1)"
              strokeWidth="4"
              fill="transparent"
            />
            
            {/* Progress circle */}
            <motion.circle
              cx="50"
              cy="50"
              r="45"
              stroke={`url(#gradient-${size})`}
              strokeWidth="4"
              fill="transparent"
              strokeLinecap="round"
              strokeDasharray={strokeDasharray}
              initial={{ strokeDashoffset: circumference }}
              animate={{ strokeDashoffset: strokeDashoffset }}
              transition={{ duration: 2, ease: "easeInOut" }}
              className="drop-shadow-lg"
            />
            
            {/* Gradient definition */}
            <defs>
              <linearGradient id={`gradient-${size}`} x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stopColor="#00ff88" />
                <stop offset="50%" stopColor="#00d4ff" />
                <stop offset="100%" stopColor="#8b5cf6" />
              </linearGradient>
            </defs>
          </svg>
          
          {/* Center value display */}
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="text-center">
              <motion.div 
                className={`${textSizes[size]} font-bold cyber-text text-${getColor(value)}`}
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ delay: 1, type: "spring" }}
              >
                {Math.round(value)}
              </motion.div>
              <div className="text-xs text-gray-400 font-mono">INDEX</div>
            </div>
          </div>
        </div>
      </div>

      {/* Status indicators */}
      <div className="mt-4 flex justify-center">
        <div className="flex space-x-4 text-sm">
          <div className={`flex items-center ${value >= 70 ? 'text-cyber-green' : 'text-gray-500'}`}>
            <div className={`w-2 h-2 rounded-full mr-2 ${value >= 70 ? 'bg-cyber-green' : 'bg-gray-500'}`}></div>
            Excellent (70+)
          </div>
          <div className={`flex items-center ${value >= 50 && value < 70 ? 'text-cyber-yellow' : 'text-gray-500'}`}>
            <div className={`w-2 h-2 rounded-full mr-2 ${value >= 50 && value < 70 ? 'bg-cyber-yellow' : 'bg-gray-500'}`}></div>
            Good (50-69)
          </div>
          <div className={`flex items-center ${value < 30 ? 'text-cyber-red' : 'text-gray-500'}`}>
            <div className={`w-2 h-2 rounded-full mr-2 ${value < 30 ? 'bg-cyber-red' : 'bg-gray-500'}`}></div>
            Critical (&lt;30)
          </div>
        </div>
      </div>

      {/* Performance message */}
      <div className="mt-4 text-center">
        <motion.p 
          className="text-sm text-gray-300"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 2 }}
        >
          {value >= 70 && "🏆 Outstanding sustainability leadership!"}
          {value >= 50 && value < 70 && "📈 Making solid progress toward sustainability goals"}
          {value >= 30 && value < 50 && "⚠️ City sustainability needs urgent attention"}
          {value < 30 && "🚨 Critical situation - immediate action required!"}
        </motion.p>
      </div>
    </div>
  )
}

export default SustainabilityMeter