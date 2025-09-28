import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { 
  Send, 
  Inbox, 
  SendHorizontal, 
  Star, 
  Search, 
  Filter,
  Mail,
  Clock,
  User,
  Tag,
  Reply,
  Forward,
  Trash2
} from 'lucide-react'
import { useGame } from '../context/GameContext'

const AgentMail = () => {
  const { messages, markMessagesRead, unreadCount } = useGame()
  const [activeTab, setActiveTab] = useState('inbox')
  const [selectedMessage, setSelectedMessage] = useState(null)
  const [searchQuery, setSearchQuery] = useState('')
  const [filterPriority, setFilterPriority] = useState('all')

  // Mock messages for demo
  const [mockMessages] = useState([
    {
      id: '1',
      from: 'Mayor Rodriguez',
      to: 'Sustainability Strategist',
      subject: 'Urgent: City Council Meeting Tomorrow',
      content: `Dear Strategist,

I need your policy recommendations ready for tomorrow's emergency city council meeting. The bad actors are pushing hard for their anti-sustainability agenda.

Current concerns:
- Sprawl Development Corp is proposing massive suburban expansion
- Carbon Industries Lobby wants to roll back emission standards
- Public pressure is mounting on both sides

Please prepare a comprehensive sustainability counter-proposal focusing on:
1. Green transportation initiatives
2. Renewable energy expansion
3. Sustainable housing development

Your expertise and timing are crucial. The city's future depends on the decisions we make tomorrow.

Best regards,
Mayor Maria Rodriguez`,
      timestamp: new Date().toISOString(),
      read: false,
      priority: 'high',
      tags: ['urgent', 'policy', 'council']
    },
    {
      id: '2',
      from: 'Energy Department',
      to: 'Sustainability Strategist',
      subject: 'Solar Panel Installation Progress Report',
      content: `Weekly Update - Solar Initiative

Current Status: 
- 347 residential installations completed
- 23% increase in renewable energy capacity
- $2.3M in federal grants secured
- Community satisfaction: 89%

Challenges:
- Grid integration delays in District 7
- Supply chain issues with premium panels
- Pushback from Carbon Industries Lobby

Opportunities:
- New federal incentive program launching
- Partnership potential with Tesla Energy
- Growing community support

Next steps:
- Prioritize grid upgrades in affected districts
- Secure additional supplier relationships
- Counter lobby misinformation campaign

The momentum is strong, but we need strategic policy support to maintain progress.

Dr. Sarah Chen
Director of Renewable Energy`,
      timestamp: new Date(Date.now() - 3600000).toISOString(),
      read: false,
      priority: 'medium',
      tags: ['energy', 'progress', 'solar']
    },
    {
      id: '3',
      from: 'Blockchain Analytics',
      to: 'All Agents',
      subject: 'Suspicious Transaction Pattern Detected',
      content: `SECURITY ALERT: Anomalous Financial Activity

Our blockchain monitoring systems have detected unusual transaction patterns:

Transaction ID: 0x7f8a9b2c4d5e6f1a2b3c4d5e6f7a8b9c
- Large payment ($750,000) from unknown wallet
- Destination: Mayor's campaign fund
- Timing: 2 hours before housing policy vote
- Pattern matches: Previous corruption cases

Risk Assessment: HIGH
Confidence Level: 87%

Recommended Actions:
1. Investigate source wallet identity
2. Review upcoming policy decisions
3. Monitor Mayor's voting patterns
4. Prepare counter-intelligence response

This pattern suggests coordinated bad actor influence. Immediate strategic response required.

AI Blockchain Sentinel
Neural Pattern Recognition System`,
      timestamp: new Date(Date.now() - 7200000).toISOString(),
      read: true,
      priority: 'critical',
      tags: ['blockchain', 'security', 'corruption']
    }
  ])

  useEffect(() => {
    markMessagesRead()
  }, [markMessagesRead])

  const filteredMessages = mockMessages.filter(message => {
    const matchesSearch = message.subject.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         message.from.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         message.content.toLowerCase().includes(searchQuery.toLowerCase())
    
    const matchesPriority = filterPriority === 'all' || message.priority === filterPriority
    
    return matchesSearch && matchesPriority
  })

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'critical': return 'cyber-red'
      case 'high': return 'orange-400'
      case 'medium': return 'cyber-yellow'
      default: return 'cyber-blue'
    }
  }

  const formatTime = (timestamp) => {
    const date = new Date(timestamp)
    const now = new Date()
    const diffMs = now - date
    const diffMins = Math.floor(diffMs / 60000)
    const diffHours = Math.floor(diffMins / 60)
    
    if (diffMins < 60) return `${diffMins}m ago`
    if (diffHours < 24) return `${diffHours}h ago`
    return date.toLocaleDateString()
  }

  return (
    <div className="container mx-auto px-4">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-8"
      >
        <h1 className="cyber-text text-4xl font-bold mb-4 text-cyber-purple animate-glow">
          AgentMail Communication Hub
        </h1>
        <p className="text-xl text-gray-300">
          Secure communications with Mayor, departments, and intelligence networks
        </p>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 h-[80vh]">
        {/* Sidebar */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          className="data-card rounded-lg p-6"
        >
          {/* Compose button */}
          <button className="w-full cyber-button mb-6 flex items-center justify-center gap-2">
            <Send size={18} />
            Compose Message
          </button>

          {/* Navigation */}
          <div className="space-y-2 mb-6">
            {[
              { id: 'inbox', label: 'Inbox', icon: Inbox, count: unreadCount },
              { id: 'sent', label: 'Sent', icon: SendHorizontal, count: 0 },
              { id: 'starred', label: 'Starred', icon: Star, count: 2 }
            ].map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`
                  w-full flex items-center justify-between p-3 rounded-lg transition-all duration-200
                  ${activeTab === tab.id 
                    ? 'bg-cyber-purple/20 text-cyber-purple border border-cyber-purple/30' 
                    : 'text-gray-400 hover:text-white hover:bg-white/5'
                  }
                `}
              >
                <div className="flex items-center gap-3">
                  <tab.icon size={18} />
                  <span>{tab.label}</span>
                </div>
                {tab.count > 0 && (
                  <span className="bg-cyber-red text-white text-xs px-2 py-1 rounded-full">
                    {tab.count}
                  </span>
                )}
              </button>
            ))}
          </div>

          {/* Filters */}
          <div className="border-t border-gray-700 pt-4">
            <h4 className="cyber-text text-sm font-semibold text-gray-300 mb-3">
              Priority Filter
            </h4>
            <select
              value={filterPriority}
              onChange={(e) => setFilterPriority(e.target.value)}
              className="w-full bg-dark-bg border border-gray-600 rounded-lg px-3 py-2 text-white text-sm"
            >
              <option value="all">All Priority Levels</option>
              <option value="critical">Critical</option>
              <option value="high">High</option>
              <option value="medium">Medium</option>
              <option value="low">Low</option>
            </select>
          </div>
        </motion.div>

        {/* Message List */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="data-card rounded-lg p-6 overflow-hidden flex flex-col"
        >
          {/* Search */}
          <div className="relative mb-4">
            <Search size={18} className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
            <input
              type="text"
              placeholder="Search messages..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full bg-dark-bg border border-gray-600 rounded-lg pl-10 pr-4 py-2 text-white placeholder-gray-400"
            />
          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto scrollbar-cyber space-y-2">
            {filteredMessages.map((message, index) => (
              <motion.div
                key={message.id}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.05 }}
                onClick={() => setSelectedMessage(message)}
                className={`
                  p-4 rounded-lg border cursor-pointer transition-all duration-200
                  ${selectedMessage?.id === message.id
                    ? 'bg-cyber-purple/20 border-cyber-purple'
                    : 'bg-dark-accent/50 border-gray-600 hover:border-gray-400 hover:bg-dark-accent'
                  }
                  ${!message.read ? 'border-l-4 border-l-cyber-blue' : ''}
                `}
              >
                <div className="flex items-start justify-between mb-2">
                  <div className="flex items-center gap-2">
                    <User size={14} className="text-gray-400" />
                    <span className={`text-sm font-medium ${!message.read ? 'text-white' : 'text-gray-300'}`}>
                      {message.from}
                    </span>
                  </div>
                  <div className="flex items-center gap-2">
                    <div className={`w-2 h-2 rounded-full bg-${getPriorityColor(message.priority)}`} />
                    <span className="text-xs text-gray-400">
                      {formatTime(message.timestamp)}
                    </span>
                  </div>
                </div>
                
                <h4 className={`font-medium mb-1 ${!message.read ? 'text-white' : 'text-gray-300'}`}>
                  {message.subject}
                </h4>
                
                <p className="text-sm text-gray-400 truncate">
                  {message.content.substring(0, 80)}...
                </p>

                {/* Tags */}
                <div className="flex gap-1 mt-2">
                  {message.tags.map(tag => (
                    <span key={tag} className="text-xs bg-gray-700 text-gray-300 px-2 py-1 rounded">
                      {tag}
                    </span>
                  ))}
                </div>
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* Message Details */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          className="data-card rounded-lg p-6 overflow-hidden flex flex-col"
        >
          {selectedMessage ? (
            <>
              {/* Header */}
              <div className="border-b border-gray-700 pb-4 mb-4">
                <div className="flex items-center justify-between mb-2">
                  <h3 className="text-lg font-semibold text-white">
                    {selectedMessage.subject}
                  </h3>
                  <div className={`px-2 py-1 rounded text-xs bg-${getPriorityColor(selectedMessage.priority)}/20 text-${getPriorityColor(selectedMessage.priority)}`}>
                    {selectedMessage.priority.toUpperCase()}
                  </div>
                </div>
                
                <div className="flex items-center gap-4 text-sm text-gray-400">
                  <span>From: {selectedMessage.from}</span>
                  <span>To: {selectedMessage.to}</span>
                  <span>{new Date(selectedMessage.timestamp).toLocaleString()}</span>
                </div>
              </div>

              {/* Content */}
              <div className="flex-1 overflow-y-auto scrollbar-cyber mb-4">
                <div className="prose prose-invert max-w-none">
                  <pre className="whitespace-pre-wrap text-gray-300 font-sans">
                    {selectedMessage.content}
                  </pre>
                </div>
              </div>

              {/* Actions */}
              <div className="flex gap-2 pt-4 border-t border-gray-700">
                <button className="cyber-button text-sm px-4 py-2 flex items-center gap-2">
                  <Reply size={14} />
                  Reply
                </button>
                <button className="cyber-button text-sm px-4 py-2 flex items-center gap-2">
                  <Forward size={14} />
                  Forward
                </button>
                <button className="cyber-button text-sm px-4 py-2 flex items-center gap-2">
                  <Star size={14} />
                  Star
                </button>
              </div>
            </>
          ) : (
            <div className="flex items-center justify-center h-full text-gray-400">
              <div className="text-center">
                <Mail size={48} className="mx-auto mb-4" />
                <p>Select a message to view details</p>
              </div>
            </div>
          )}
        </motion.div>
      </div>
    </div>
  )
}

export default AgentMail