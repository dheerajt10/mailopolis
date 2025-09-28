import React from 'react'
import { motion } from 'framer-motion'
import { Shield, Users, Clock, TrendingUp, TrendingDown } from 'lucide-react'

const QuickStats = ({ mayorTrust, badActorInfluence, roundsRemaining }) => {
  const stats = [
    {
      id: 'trust',
      label: 'Mayor Trust',
      value: mayorTrust,
      icon: Users,
      color: mayorTrust >= 70 ? 'cyber-green' : mayorTrust >= 40 ? 'cyber-yellow' : 'cyber-red',
      trend: Math.random() > 0.5 ? 'up' : 'down'
    },
    {
      id: 'threat',
      label: 'Bad Actor Influence',
      value: badActorInfluence,
      icon: Shield,
      color: badActorInfluence <= 30 ? 'cyber-green' : badActorInfluence <= 60 ? 'cyber-yellow' : 'cyber-red',
      trend: Math.random() > 0.5 ? 'up' : 'down',
      inverted: true // Lower is better
    },
    {
      id: 'time',
      label: 'Rounds Left',
      value: roundsRemaining,
      icon: Clock,
      color: roundsRemaining >= 15 ? 'cyber-green' : roundsRemaining >= 8 ? 'cyber-yellow' : 'cyber-red',
      trend: 'down',
      unit: ''
    }
  ]

  return (
    <div className="space-y-4">
      {stats.map((stat, index) => (
        <motion.div
          key={stat.id}
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: index * 0.1 }}
          className="data-card rounded-lg p-4"
        >
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className={`p-2 rounded-lg bg-${stat.color}/20`}>
                <stat.icon 
                  size={20} 
                  className={`text-${stat.color}`}
                />
              </div>
              <div>
                <div className="text-sm text-gray-400">{stat.label}</div>
                <div className={`cyber-text text-2xl font-bold text-${stat.color}`}>
                  {stat.value}
                  {stat.id !== 'time' && '%'}
                  {stat.unit || ''}
                </div>
              </div>
            </div>
            
            <div className="text-right">
              {stat.trend === 'up' && (
                <TrendingUp 
                  size={16} 
                  className={stat.inverted ? 'text-cyber-red' : 'text-cyber-green'} 
                />
              )}
              {stat.trend === 'down' && (
                <TrendingDown 
                  size={16} 
                  className={stat.inverted ? 'text-cyber-green' : 'text-cyber-red'} 
                />
              )}
            </div>
          </div>

          {/* Mini progress bar */}
          <div className="mt-3">
            <div className="w-full bg-dark-bg rounded-full h-1.5 overflow-hidden">
              <motion.div
                className={`h-full bg-${stat.color}`}
                initial={{ width: 0 }}
                animate={{ 
                  width: stat.id === 'time' 
                    ? `${(stat.value / 25) * 100}%` 
                    : `${stat.value}%` 
                }}
                transition={{ duration: 1, delay: index * 0.1 + 0.5 }}
              />
            </div>
          </div>
        </motion.div>
      ))}

      {/* Action recommendation */}
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5 }}
        className="data-card rounded-lg p-4 border-l-4 border-cyber-blue"
      >
        <h4 className="cyber-text text-sm font-semibold text-cyber-blue mb-2">
          Strategic Recommendation
        </h4>
        <p className="text-sm text-gray-300">
          {mayorTrust < 50 && badActorInfluence > 50 
            ? "🎯 Focus on building Mayor trust while countering bad actor influence"
            : mayorTrust >= 70 
            ? "🚀 Excellent position! Push for ambitious sustainability policies"
            : badActorInfluence > 70 
            ? "⚠️ Bad actors gaining control - immediate counter-action needed"
            : "📈 Maintain momentum with strategic policy proposals"}
        </p>
      </motion.div>
    </div>
  )
}

export default QuickStats