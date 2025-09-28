import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { 
  Shield, 
  AlertTriangle, 
  TrendingUp, 
  TrendingDown, 
  Eye, 
  Target,
  DollarSign,
  Users,
  Building,
  Zap,
  Calendar,
  Activity,
  Crosshair,
  Search
} from 'lucide-react'
import { useGame } from '../context/GameContext'

const BadActorIntel = () => {
  const { badActors, loading } = useGame()
  const [selectedActor, setSelectedActor] = useState(null)
  const [threatLevel, setThreatLevel] = useState('medium')
  const [recentActivities, setRecentActivities] = useState([])

  // Mock bad actor data enhancement
  const [enhancedActors, setEnhancedActors] = useState([])

  useEffect(() => {
    // Enhance bad actors with additional intelligence data
    const enhanced = badActors.map(actor => ({
      ...actor,
      threat_level: Math.random() > 0.7 ? 'high' : Math.random() > 0.4 ? 'medium' : 'low',
      recent_activity: Math.floor(Math.random() * 10) + 1,
      success_rate: Math.floor(Math.random() * 60) + 20,
      next_move_prediction: getPredictedMove(actor.type),
      influence_trend: Math.random() > 0.5 ? 'increasing' : 'decreasing',
      last_seen: new Date(Date.now() - Math.random() * 86400000 * 3).toISOString(),
      operations: generateOperations(actor.name),
      weaknesses: generateWeaknesses(actor.type),
      strengths: generateStrengths(actor.type)
    }))
    
    setEnhancedActors(enhanced)
  }, [badActors])

  useEffect(() => {
    // Generate recent activities
    const activities = [
      {
        id: 1,
        actor: 'Sprawl Development Corp',
        action: 'Lobbied against public transit expansion',
        timestamp: new Date(Date.now() - 1800000).toISOString(),
        impact: 'high',
        success: false,
        details: 'Attempted to influence transportation committee with $200k campaign contribution'
      },
      {
        id: 2,
        actor: 'Carbon Industries Lobby',
        action: 'Spread misinformation about renewable energy costs',
        timestamp: new Date(Date.now() - 3600000).toISOString(),
        impact: 'medium',
        success: true,
        details: 'Social media campaign reached 50k residents, created doubt about solar initiatives'
      },
      {
        id: 3,
        actor: 'Waste Management Cartel',
        action: 'Blocked recycling facility expansion',
        timestamp: new Date(Date.now() - 7200000).toISOString(),
        impact: 'medium',
        success: true,
        details: 'Used legal challenges to delay construction permits by 6 months'
      },
      {
        id: 4,
        actor: 'Sprawl Development Corp',
        action: 'Proposed suburban mega-mall project',
        timestamp: new Date(Date.now() - 10800000).toISOString(),
        impact: 'high',
        success: false,
        details: 'Mayor rejected proposal after sustainability impact assessment'
      }
    ]
    
    setRecentActivities(activities)
  }, [])

  function getPredictedMove(type) {
    const moves = {
      'DEVELOPER_GROUP': [
        'Push for zoning law changes',
        'Lobby against green building requirements',
        'Propose low-density suburban expansion'
      ],
      'FOSSIL_FUEL_COMPANY': [
        'Attack renewable energy subsidies',
        'Fund climate denial campaigns',
        'Block electric vehicle infrastructure'
      ],
      'CORPORATE_LOBBY': [
        'Weaken environmental regulations',
        'Delay sustainability reporting requirements',
        'Oppose carbon pricing initiatives'
      ]
    }
    
    const typeKey = Object.keys(moves).find(key => type.includes(key.split('_')[0]))
    const typeMoves = moves[typeKey] || moves['CORPORATE_LOBBY']
    return typeMoves[Math.floor(Math.random() * typeMoves.length)]
  }

  function generateOperations(name) {
    return [
      'Operation Shadow Fund',
      'Project Green Wash',
      'Initiative Delay Tactics',
      'Campaign Influence Network'
    ]
  }

  function generateWeaknesses(type) {
    const weaknesses = {
      'DEVELOPER_GROUP': ['Public opposition to sprawl', 'Environmental impact studies', 'Zoning restrictions'],
      'FOSSIL_FUEL_COMPANY': ['Renewable energy momentum', 'Climate activism', 'Federal regulations'],
      'CORPORATE_LOBBY': ['Transparency requirements', 'Public accountability', 'Media scrutiny']
    }
    
    return weaknesses[type] || weaknesses['CORPORATE_LOBBY']
  }

  function generateStrengths(type) {
    const strengths = {
      'DEVELOPER_GROUP': ['Financial resources', 'Political connections', 'Legal expertise'],
      'FOSSIL_FUEL_COMPANY': ['Industry influence', 'Technical knowledge', 'Regulatory capture'],
      'CORPORATE_LOBBY': ['Network effects', 'Information warfare', 'Resource coordination']
    }
    
    return strengths[type] || strengths['CORPORATE_LOBBY']
  }

  const getThreatColor = (level) => {
    switch (level) {
      case 'high': return 'cyber-red'
      case 'medium': return 'cyber-yellow'
      case 'low': return 'cyber-green'
      default: return 'gray-400'
    }
  }

  const getActivityIcon = (action) => {
    if (action.includes('Lobby') || action.includes('lobbied')) return Users
    if (action.includes('misinformation') || action.includes('campaign')) return Activity
    if (action.includes('Block') || action.includes('legal')) return Shield
    if (action.includes('Proposed') || action.includes('project')) return Building
    return AlertTriangle
  }

  const formatTime = (timestamp) => {
    const date = new Date(timestamp)
    const now = new Date()
    const diffMs = now - date
    const diffHours = Math.floor(diffMs / 3600000)
    
    if (diffHours < 1) return 'Just now'
    if (diffHours < 24) return `${diffHours}h ago`
    return `${Math.floor(diffHours / 24)}d ago`
  }

  const overallThreat = enhancedActors.length > 0 
    ? enhancedActors.filter(a => a.threat_level === 'high').length > 2 ? 'CRITICAL'
    : enhancedActors.filter(a => a.threat_level === 'high').length > 0 ? 'HIGH'
    : 'MEDIUM'
    : 'LOW'

  const getThreatBgColor = (level) => {
    switch (level) {
      case 'CRITICAL': return 'bg-red-500/20 border-cyber-red'
      case 'HIGH': return 'bg-orange-500/20 border-orange-400'
      case 'MEDIUM': return 'bg-yellow-500/20 border-cyber-yellow'
      default: return 'bg-green-500/20 border-cyber-green'
    }
  }

  return (
    <div className="container mx-auto px-4">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-8"
      >
        <h1 className="cyber-text text-4xl font-bold mb-4 text-cyber-red animate-glow">
          Bad Actor Intelligence Hub
        </h1>
        <p className="text-xl text-gray-300">
          Advanced threat monitoring and adversary analysis
        </p>
      </motion.div>

      {/* Threat Level Overview */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className={`rounded-lg border-2 p-6 mb-8 ${getThreatBgColor(overallThreat)}`}
      >
        <div className="flex items-center justify-between">
          <div>
            <h2 className="cyber-text text-2xl font-bold text-white mb-2">
              Current Threat Level: {overallThreat}
            </h2>
            <p className="text-gray-300">
              {enhancedActors.filter(a => a.active).length} active adversaries detected
            </p>
          </div>
          <div className="text-right">
            <AlertTriangle size={48} className={`text-${getThreatColor(overallThreat.toLowerCase())}`} />
          </div>
        </div>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Bad Actor List */}
        <div className="lg:col-span-2">
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="data-card rounded-lg p-6"
          >
            <h3 className="cyber-text text-xl font-bold text-cyber-red mb-6">
              Known Adversaries
            </h3>

            <div className="space-y-4">
              {enhancedActors.map((actor, index) => (
                <motion.div
                  key={actor.id}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1 }}
                  onClick={() => setSelectedActor(actor)}
                  className={`
                    p-4 rounded-lg border-2 cursor-pointer transition-all duration-200
                    ${selectedActor?.id === actor.id
                      ? 'bg-cyber-red/20 border-cyber-red'
                      : 'bg-dark-accent/50 border-gray-600 hover:border-gray-400 hover:bg-dark-accent'
                    }
                  `}
                >
                  <div className="flex items-start justify-between mb-3">
                    <div>
                      <h4 className="font-bold text-white text-lg">{actor.name}</h4>
                      <div className="text-sm text-gray-400 mb-2">
                        Type: {actor.type.replace(/_/g, ' ')}
                      </div>
                    </div>
                    
                    <div className="flex items-center gap-2">
                      <div className={`px-2 py-1 rounded text-xs bg-${getThreatColor(actor.threat_level)}/20 text-${getThreatColor(actor.threat_level)}`}>
                        {actor.threat_level.toUpperCase()}
                      </div>
                      {actor.influence_trend === 'increasing' ? (
                        <TrendingUp className="text-cyber-red" size={16} />
                      ) : (
                        <TrendingDown className="text-cyber-green" size={16} />
                      )}
                    </div>
                  </div>

                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                    <div>
                      <div className="text-gray-400">Influence</div>
                      <div className="font-bold text-cyber-red">{actor.influence_power}%</div>
                    </div>
                    <div>
                      <div className="text-gray-400">Budget</div>
                      <div className="font-bold text-cyber-yellow">
                        ${(actor.corruption_budget / 1000).toFixed(0)}k
                      </div>
                    </div>
                    <div>
                      <div className="text-gray-400">Success Rate</div>
                      <div className="font-bold text-cyber-blue">{actor.success_rate}%</div>
                    </div>
                    <div>
                      <div className="text-gray-400">Last Seen</div>
                      <div className="font-bold text-gray-300">{formatTime(actor.last_seen)}</div>
                    </div>
                  </div>

                  <div className="mt-3 flex flex-wrap gap-2">
                    {actor.target_departments.map(dept => (
                      <span key={dept} className="text-xs bg-gray-700 text-gray-300 px-2 py-1 rounded">
                        {dept.replace(/_/g, ' ')}
                      </span>
                    ))}
                  </div>

                  {/* Activity indicator */}
                  <div className="mt-3 flex items-center justify-between">
                    <div className="text-xs text-gray-400">
                      Recent Activities: {actor.recent_activity}
                    </div>
                    <div className="flex items-center gap-1">
                      <div className={`w-2 h-2 rounded-full ${actor.active ? 'bg-cyber-red' : 'bg-gray-600'} ${actor.active ? 'animate-pulse' : ''}`} />
                      <span className="text-xs text-gray-400">
                        {actor.active ? 'ACTIVE' : 'DORMANT'}
                      </span>
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>
          </motion.div>
        </div>

        {/* Intelligence Panel */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          className="space-y-6"
        >
          {/* Selected Actor Details */}
          <div className="data-card rounded-lg p-6">
            {selectedActor ? (
              <>
                <div className="flex items-center justify-between mb-4">
                  <h3 className="cyber-text text-lg font-bold text-cyber-red">
                    Threat Analysis
                  </h3>
                  <div className={`px-2 py-1 rounded text-xs bg-${getThreatColor(selectedActor.threat_level)}/20 text-${getThreatColor(selectedActor.threat_level)}`}>
                    {selectedActor.threat_level.toUpperCase()}
                  </div>
                </div>

                <div className="space-y-4">
                  <div>
                    <h4 className="font-semibold text-white mb-2">{selectedActor.name}</h4>
                    <p className="text-sm text-gray-300">
                      {selectedActor.type.replace(/_/g, ' ')} with {selectedActor.influence_power}% influence power
                    </p>
                  </div>

                  <div>
                    <h5 className="font-semibold text-gray-300 mb-2">Predicted Next Move</h5>
                    <p className="text-sm text-cyber-yellow bg-dark-bg p-2 rounded">
                      {selectedActor.next_move_prediction}
                    </p>
                  </div>

                  <div>
                    <h5 className="font-semibold text-gray-300 mb-2">Active Operations</h5>
                    <div className="space-y-1">
                      {selectedActor.operations.map((op, i) => (
                        <div key={i} className="text-sm text-gray-400 flex items-center gap-2">
                          <Target size={12} />
                          {op}
                        </div>
                      ))}
                    </div>
                  </div>

                  <div>
                    <h5 className="font-semibold text-cyber-red mb-2">Strengths</h5>
                    <div className="space-y-1">
                      {selectedActor.strengths.map((strength, i) => (
                        <div key={i} className="text-sm text-gray-400">• {strength}</div>
                      ))}
                    </div>
                  </div>

                  <div>
                    <h5 className="font-semibold text-cyber-green mb-2">Weaknesses</h5>
                    <div className="space-y-1">
                      {selectedActor.weaknesses.map((weakness, i) => (
                        <div key={i} className="text-sm text-gray-400">• {weakness}</div>
                      ))}
                    </div>
                  </div>
                </div>

                <div className="mt-6 pt-4 border-t border-gray-700">
                  <button className="w-full cyber-button flex items-center justify-center gap-2">
                    <Crosshair size={16} />
                    Counter Strategy
                  </button>
                </div>
              </>
            ) : (
              <div className="text-center text-gray-400">
                <Shield size={48} className="mx-auto mb-4" />
                <p>Select an adversary to view intelligence</p>
              </div>
            )}
          </div>

          {/* Recent Activity Feed */}
          <div className="data-card rounded-lg p-6">
            <h3 className="cyber-text text-lg font-bold text-cyber-blue mb-4 flex items-center gap-2">
              <Activity size={18} />
              Recent Activity
            </h3>

            <div className="space-y-3 max-h-80 overflow-y-auto scrollbar-cyber">
              {recentActivities.map((activity, index) => {
                const IconComponent = getActivityIcon(activity.action)
                
                return (
                  <motion.div
                    key={activity.id}
                    initial={{ opacity: 0, x: 10 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.05 }}
                    className={`
                      p-3 rounded-lg border-l-4 
                      ${activity.success 
                        ? 'border-l-cyber-red bg-red-500/10' 
                        : 'border-l-cyber-green bg-green-500/10'
                      }
                    `}
                  >
                    <div className="flex items-start gap-3">
                      <IconComponent size={16} className={activity.success ? 'text-cyber-red' : 'text-cyber-green'} />
                      
                      <div className="flex-1">
                        <div className="flex items-center justify-between mb-1">
                          <h5 className="font-semibold text-white text-sm">
                            {activity.actor}
                          </h5>
                          <span className="text-xs text-gray-400">
                            {formatTime(activity.timestamp)}
                          </span>
                        </div>
                        
                        <p className="text-sm text-gray-300 mb-2">
                          {activity.action}
                        </p>
                        
                        <p className="text-xs text-gray-400">
                          {activity.details}
                        </p>

                        <div className="flex items-center gap-2 mt-2">
                          <span className={`text-xs px-2 py-1 rounded ${activity.success ? 'bg-cyber-red/20 text-cyber-red' : 'bg-cyber-green/20 text-cyber-green'}`}>
                            {activity.success ? 'SUCCESS' : 'BLOCKED'}
                          </span>
                          <span className="text-xs text-gray-400">
                            Impact: {activity.impact}
                          </span>
                        </div>
                      </div>
                    </div>
                  </motion.div>
                )
              })}
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  )
}

export default BadActorIntel