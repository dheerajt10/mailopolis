import React, { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { AlertTriangle, CheckCircle, Info, X, Filter } from 'lucide-react'

const AlertsPanel = ({ sustainabilityIndex, mayorTrust, badActorInfluence, departments }) => {
  const [filter, setFilter] = useState('all') // all, critical, warning, info
  const [dismissed, setDismissed] = useState(new Set())

  // Generate alerts based on game state
  const generateAlerts = () => {
    const alerts = []

    // Critical alerts
    if (sustainabilityIndex < 30) {
      alerts.push({
        id: 'sustainability-critical',
        type: 'critical',
        title: 'City Sustainability Crisis',
        message: 'Sustainability index has fallen below 30%. Immediate action required!',
        action: 'Submit emergency sustainability policies',
        timestamp: new Date()
      })
    }

    if (mayorTrust < 25) {
      alerts.push({
        id: 'trust-critical',
        type: 'critical',
        title: 'Mayor Trust Critical',
        message: 'Mayor trust is dangerously low. Your influence is severely compromised.',
        action: 'Focus on rebuilding relationships',
        timestamp: new Date()
      })
    }

    if (badActorInfluence > 80) {
      alerts.push({
        id: 'badactor-critical',
        type: 'critical',
        title: 'Bad Actors Dominant',
        message: 'Bad actors have gained overwhelming influence over city decisions.',
        action: 'Counter their proposals immediately',
        timestamp: new Date()
      })
    }

    // Warning alerts
    departments?.forEach(dept => {
      if (dept.sustainability_score < 25) {
        alerts.push({
          id: `dept-warning-${dept.id}`,
          type: 'warning',
          title: `${dept.name} Department Critical`,
          message: `${dept.name} sustainability score is critically low (${Math.round(dept.sustainability_score)}%).`,
          action: `Submit targeted policy for ${dept.name}`,
          timestamp: new Date()
        })
      }
    })

    if (sustainabilityIndex < 50 && sustainabilityIndex >= 30) {
      alerts.push({
        id: 'sustainability-warning',
        type: 'warning',
        title: 'Sustainability Declining',
        message: 'City sustainability is below average and trending downward.',
        action: 'Review and adjust strategy',
        timestamp: new Date()
      })
    }

    // Info alerts
    if (mayorTrust > 70) {
      alerts.push({
        id: 'trust-good',
        type: 'info',
        title: 'Strong Mayor Relationship',
        message: 'Excellent relationship with Mayor. Perfect time for ambitious policies.',
        action: 'Propose transformative initiatives',
        timestamp: new Date()
      })
    }

    if (sustainabilityIndex > 70) {
      alerts.push({
        id: 'sustainability-good',
        type: 'info',
        title: 'Sustainability Excellence',
        message: 'Outstanding sustainability performance across the city.',
        action: 'Maintain momentum and share success',
        timestamp: new Date()
      })
    }

    return alerts.filter(alert => !dismissed.has(alert.id))
  }

  const alerts = generateAlerts()
  
  const filteredAlerts = alerts.filter(alert => 
    filter === 'all' || alert.type === filter
  )

  const getAlertIcon = (type) => {
    switch (type) {
      case 'critical': return AlertTriangle
      case 'warning': return AlertTriangle
      case 'info': return Info
      default: return CheckCircle
    }
  }

  const getAlertColors = (type) => {
    switch (type) {
      case 'critical': return 'text-cyber-red border-cyber-red bg-red-500/10'
      case 'warning': return 'text-cyber-yellow border-cyber-yellow bg-yellow-500/10'
      case 'info': return 'text-cyber-blue border-cyber-blue bg-blue-500/10'
      default: return 'text-cyber-green border-cyber-green bg-green-500/10'
    }
  }

  const dismissAlert = (alertId) => {
    setDismissed(new Set([...dismissed, alertId]))
  }

  const filterCounts = {
    all: alerts.length,
    critical: alerts.filter(a => a.type === 'critical').length,
    warning: alerts.filter(a => a.type === 'warning').length,
    info: alerts.filter(a => a.type === 'info').length
  }

  return (
    <div className="data-card rounded-lg p-6">
      <div className="flex justify-between items-center mb-4">
        <h3 className="cyber-text text-xl font-bold text-cyber-blue">
          Strategic Alerts
        </h3>
        <div className="text-sm text-gray-400">
          {filteredAlerts.length} Active
        </div>
      </div>

      {/* Filter controls */}
      <div className="flex flex-wrap gap-2 mb-4">
        {Object.entries(filterCounts).map(([type, count]) => (
          <button
            key={type}
            onClick={() => setFilter(type)}
            className={`
              px-3 py-1 text-xs rounded-full border transition-all duration-200
              ${filter === type 
                ? 'bg-cyber-blue text-dark-bg border-cyber-blue' 
                : 'bg-transparent text-gray-400 border-gray-600 hover:border-gray-400'
              }
            `}
          >
            <Filter size={10} className="inline mr-1" />
            {type.charAt(0).toUpperCase() + type.slice(1)} ({count})
          </button>
        ))}
      </div>

      {/* Alerts list */}
      <div className="space-y-3 max-h-80 overflow-y-auto scrollbar-cyber">
        <AnimatePresence>
          {filteredAlerts.map((alert, index) => {
            const IconComponent = getAlertIcon(alert.type)
            const colors = getAlertColors(alert.type)
            
            return (
              <motion.div
                key={alert.id}
                layout
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: 20 }}
                transition={{ delay: index * 0.05 }}
                className={`
                  relative rounded-lg border p-4 ${colors}
                  hover:bg-opacity-20 transition-all duration-200
                `}
              >
                <div className="flex items-start gap-3">
                  <IconComponent size={18} className="mt-0.5 flex-shrink-0" />
                  
                  <div className="flex-1 min-w-0">
                    <div className="flex justify-between items-start">
                      <h4 className="font-semibold text-white text-sm mb-1">
                        {alert.title}
                      </h4>
                      <button
                        onClick={() => dismissAlert(alert.id)}
                        className="text-gray-400 hover:text-white transition-colors ml-2 flex-shrink-0"
                      >
                        <X size={14} />
                      </button>
                    </div>
                    
                    <p className="text-sm text-gray-300 mb-2">
                      {alert.message}
                    </p>
                    
                    {alert.action && (
                      <div className="text-xs text-gray-400 italic">
                        💡 {alert.action}
                      </div>
                    )}
                  </div>
                </div>

                {/* Priority indicator */}
                <div className={`
                  absolute left-0 top-0 bottom-0 w-1 rounded-l-lg
                  ${alert.type === 'critical' ? 'bg-cyber-red' : 
                    alert.type === 'warning' ? 'bg-cyber-yellow' : 
                    'bg-cyber-blue'}
                `} />
              </motion.div>
            )
          })}
        </AnimatePresence>

        {filteredAlerts.length === 0 && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="text-center py-8 text-gray-400"
          >
            <CheckCircle size={48} className="mx-auto mb-3 text-cyber-green" />
            <p className="text-lg">All Clear!</p>
            <p className="text-sm">No {filter !== 'all' ? filter : ''} alerts at this time.</p>
          </motion.div>
        )}
      </div>

      {/* Quick actions */}
      {filteredAlerts.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="mt-4 pt-4 border-t border-gray-700"
        >
          <div className="flex flex-wrap gap-2">
            <button className="cyber-button text-xs px-3 py-1">
              Address Critical Issues
            </button>
            <button className="cyber-button text-xs px-3 py-1">
              Create Emergency Policy
            </button>
          </div>
        </motion.div>
      )}
    </div>
  )
}

export default AlertsPanel