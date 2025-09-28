import React from 'react'
import { motion } from 'framer-motion'

const DepartmentGrid = ({ departments, icons }) => {
  const getScoreColor = (score) => {
    if (score >= 70) return 'text-cyber-green border-cyber-green'
    if (score >= 50) return 'text-cyber-yellow border-cyber-yellow'
    if (score >= 30) return 'text-orange-400 border-orange-400'
    return 'text-cyber-red border-cyber-red'
  }

  const getProgressColor = (score) => {
    if (score >= 70) return 'bg-cyber-green'
    if (score >= 50) return 'bg-cyber-yellow'
    if (score >= 30) return 'bg-orange-400'
    return 'bg-cyber-red'
  }

  const formatDepartmentName = (name) => {
    return name.replace(/[_&]/g, ' ').replace(/\b\w/g, l => l.toUpperCase())
  }

  return (
    <div className="data-card rounded-lg p-6">
      <div className="flex justify-between items-center mb-6">
        <h3 className="cyber-text text-xl font-bold text-cyber-blue">
          Department Performance
        </h3>
        <div className="text-sm text-gray-400">
          {departments?.length || 0} Active Departments
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {departments?.map((dept, index) => {
          const IconComponent = icons[dept.id] || icons['ENERGY']
          const score = dept.sustainability_score || 0
          
          return (
            <motion.div
              key={dept.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              whileHover={{ scale: 1.02, y: -2 }}
              className={`
                relative overflow-hidden rounded-lg border-2 
                bg-gradient-to-br from-dark-card to-dark-accent 
                p-4 cursor-pointer transition-all duration-300
                hover:shadow-lg ${getScoreColor(score)}
              `}
            >
              {/* Background glow effect */}
              <div className={`absolute inset-0 bg-gradient-to-br ${
                score >= 70 ? 'from-green-500/10 to-transparent' :
                score >= 50 ? 'from-yellow-500/10 to-transparent' :
                score >= 30 ? 'from-orange-500/10 to-transparent' :
                'from-red-500/10 to-transparent'
              }`}></div>

              <div className="relative z-10">
                {/* Header */}
                <div className="flex items-start justify-between mb-3">
                  <div className="flex items-center gap-2">
                    <IconComponent 
                      size={24} 
                      className={`${getScoreColor(score).split(' ')[0]} drop-shadow-sm`}
                    />
                    <h4 className="font-semibold text-white text-sm">
                      {formatDepartmentName(dept.name)}
                    </h4>
                  </div>
                  <div className={`cyber-text text-lg font-bold ${getScoreColor(score).split(' ')[0]}`}>
                    {Math.round(score)}
                  </div>
                </div>

                {/* Progress bar */}
                <div className="mb-3">
                  <div className="w-full bg-dark-bg rounded-full h-2 overflow-hidden">
                    <motion.div
                      className={`h-full ${getProgressColor(score)} relative`}
                      initial={{ width: 0 }}
                      animate={{ width: `${score}%` }}
                      transition={{ duration: 1, delay: index * 0.1 + 0.5 }}
                    >
                      {/* Shimmer effect */}
                      <motion.div
                        className="absolute top-0 left-0 h-full w-4 bg-white opacity-30"
                        animate={{ x: [-16, score * 2] }}
                        transition={{ 
                          duration: 2, 
                          repeat: Infinity, 
                          repeatDelay: 3,
                          ease: "easeInOut"
                        }}
                      />
                    </motion.div>
                  </div>
                </div>

                {/* Status indicators */}
                <div className="flex justify-between items-center text-xs">
                  <span className="text-gray-400">
                    {score >= 70 ? 'Excellent' : 
                     score >= 50 ? 'Good' : 
                     score >= 30 ? 'Needs Work' : 'Critical'}
                  </span>
                  <div className="flex items-center gap-1">
                    <div className={`w-1.5 h-1.5 rounded-full pulse-dot ${
                      score >= 70 ? 'bg-cyber-green' : 
                      score >= 50 ? 'bg-cyber-yellow' : 
                      score >= 30 ? 'bg-orange-400' : 'bg-cyber-red'
                    }`}></div>
                    <span className="text-gray-500">Live</span>
                  </div>
                </div>

                {/* Trend indicator */}
                <div className="absolute top-2 right-2">
                  <motion.div
                    className={`w-2 h-2 rounded-full ${
                      score >= 60 ? 'bg-cyber-green' :
                      score >= 40 ? 'bg-cyber-yellow' : 'bg-cyber-red'
                    }`}
                    animate={{ 
                      scale: [1, 1.2, 1],
                      opacity: [0.7, 1, 0.7] 
                    }}
                    transition={{ 
                      duration: 2, 
                      repeat: Infinity,
                      delay: index * 0.2
                    }}
                  />
                </div>
              </div>
            </motion.div>
          )
        })}
      </div>

      {/* Summary stats */}
      <div className="mt-6 pt-4 border-t border-gray-700">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
          <div>
            <div className="cyber-text text-lg font-bold text-cyber-green">
              {departments?.filter(d => d.sustainability_score >= 70).length || 0}
            </div>
            <div className="text-xs text-gray-400">Excellent</div>
          </div>
          <div>
            <div className="cyber-text text-lg font-bold text-cyber-yellow">
              {departments?.filter(d => d.sustainability_score >= 50 && d.sustainability_score < 70).length || 0}
            </div>
            <div className="text-xs text-gray-400">Good</div>
          </div>
          <div>
            <div className="cyber-text text-lg font-bold text-orange-400">
              {departments?.filter(d => d.sustainability_score >= 30 && d.sustainability_score < 50).length || 0}
            </div>
            <div className="text-xs text-gray-400">Needs Work</div>
          </div>
          <div>
            <div className="cyber-text text-lg font-bold text-cyber-red">
              {departments?.filter(d => d.sustainability_score < 30).length || 0}
            </div>
            <div className="text-xs text-gray-400">Critical</div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default DepartmentGrid