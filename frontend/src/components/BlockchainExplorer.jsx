import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { 
  Activity, 
  Search, 
  Filter, 
  AlertTriangle, 
  CheckCircle, 
  Eye,
  Hash,
  Clock,
  DollarSign,
  ArrowRight,
  Zap,
  TrendingUp,
  Shield
} from 'lucide-react'

const BlockchainExplorer = () => {
  const [transactions, setTransactions] = useState([])
  const [filter, setFilter] = useState('all') // all, suspicious, policy, financial
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedTransaction, setSelectedTransaction] = useState(null)

  // Mock blockchain data
  useEffect(() => {
    const mockTransactions = [
      {
        id: '0x7f8a9b2c4d5e6f1a2b3c4d5e6f7a8b9c',
        type: 'financial',
        from: '0x742d35Cc6624C0532D0B6c8B4D4E6B1c7A8F9E',
        to: '0x8B5CF6C7D8E9F0A1B2C3D4E5F6A7B8C9D0E1F',
        amount: 750000,
        timestamp: new Date().toISOString(),
        status: 'suspicious',
        description: 'Large payment to Mayor campaign fund',
        confidence: 87,
        tags: ['corruption', 'campaign', 'housing-vote'],
        details: {
          gasUsed: 21000,
          blockNumber: 18420156,
          confirmations: 12,
          nonce: 42,
          value: '750000000000000000000000',
          data: '0x'
        }
      },
      {
        id: '0x1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a',
        type: 'policy',
        from: 'Sustainability_Strategist',
        to: 'Mayor_Office',
        amount: 0,
        timestamp: new Date(Date.now() - 1800000).toISOString(),
        status: 'confirmed',
        description: 'Solar Panel Incentive Policy Proposal',
        confidence: 95,
        tags: ['energy', 'proposal', 'solar'],
        details: {
          policyId: 'POL-2024-003',
          department: 'Energy',
          priority: 'high',
          expectedImpact: 'significant',
          votes: { for: 4, against: 1, abstain: 0 }
        }
      },
      {
        id: '0x9f8e7d6c5b4a39281706f5e4d3c2b1a09e8d7c',
        type: 'financial',
        from: '0x3E5F7A9B1C2D4E6F8A0B2C4D6E8F0A1B3C5D7',
        to: '0xA1B2C3D4E5F6A7B8C9D0E1F2A3B4C5D6E7F8A',
        amount: 150000,
        timestamp: new Date(Date.now() - 3600000).toISOString(),
        status: 'normal',
        description: 'Green infrastructure development fund',
        confidence: 98,
        tags: ['infrastructure', 'green', 'approved'],
        details: {
          gasUsed: 45000,
          blockNumber: 18420098,
          confirmations: 67,
          projectId: 'GRN-INF-2024-12',
          contractor: 'EcoConstruct Ltd'
        }
      },
      {
        id: '0x5c4b3a29180716f5e4d3c2b1a09f8e7d6c5b4a',
        type: 'vote',
        from: 'Mayor_Office',
        to: 'City_Council',
        amount: 0,
        timestamp: new Date(Date.now() - 7200000).toISOString(),
        status: 'confirmed',
        description: 'Vote: Electric Bus Fleet Expansion - APPROVED',
        confidence: 100,
        tags: ['transportation', 'vote', 'approved'],
        details: {
          votingResults: { approved: 6, rejected: 1 },
          budget: 2500000,
          timeline: '18 months',
          impact: 'High sustainability increase expected'
        }
      },
      {
        id: '0xb8a7965432109fedcba9876543210fedcba98',
        type: 'suspicious',
        from: '0xDEADBEEF123456789ABCDEF0123456789ABCDEF',
        to: '0x456789ABCDEF0123456789ABCDEF01234567',
        amount: 500000,
        timestamp: new Date(Date.now() - 10800000).toISOString(),
        status: 'flagged',
        description: 'Suspicious payment from construction lobby',
        confidence: 78,
        tags: ['lobby', 'construction', 'investigation'],
        details: {
          riskLevel: 'HIGH',
          pattern: 'Recurring payments before zoning votes',
          similarTransactions: 3,
          investigation: 'ACTIVE'
        }
      }
    ]
    
    setTransactions(mockTransactions)
  }, [])

  const filteredTransactions = transactions.filter(tx => {
    const matchesSearch = tx.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         tx.id.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         tx.tags.some(tag => tag.toLowerCase().includes(searchQuery.toLowerCase()))
    
    const matchesFilter = filter === 'all' || tx.type === filter || tx.status === filter
    
    return matchesSearch && matchesFilter
  })

  const getStatusColor = (status) => {
    switch (status) {
      case 'suspicious':
      case 'flagged':
        return 'cyber-red'
      case 'confirmed':
      case 'normal':
        return 'cyber-green'
      case 'pending':
        return 'cyber-yellow'
      default:
        return 'gray-400'
    }
  }

  const getTypeIcon = (type) => {
    switch (type) {
      case 'financial': return DollarSign
      case 'policy': return Shield
      case 'vote': return CheckCircle
      case 'suspicious': return AlertTriangle
      default: return Activity
    }
  }

  const formatAmount = (amount) => {
    if (amount === 0) return 'N/A'
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0
    }).format(amount)
  }

  const formatAddress = (address) => {
    return `${address.substring(0, 6)}...${address.substring(address.length - 4)}`
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

  const riskStats = {
    total: transactions.length,
    suspicious: transactions.filter(tx => tx.status === 'suspicious' || tx.status === 'flagged').length,
    highRisk: transactions.filter(tx => tx.confidence < 80).length,
    confirmed: transactions.filter(tx => tx.status === 'confirmed' || tx.status === 'normal').length
  }

  return (
    <div className="container mx-auto px-4">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-8"
      >
        <h1 className="cyber-text text-4xl font-bold mb-4 text-cyber-green animate-glow">
          Blockchain Intelligence Center
        </h1>
        <p className="text-xl text-gray-300">
          Real-time transaction analysis and corruption detection
        </p>
      </motion.div>

      {/* Stats Dashboard */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8"
      >
        <div className="data-card rounded-lg p-4">
          <div className="flex items-center justify-between">
            <div>
              <div className="cyber-text text-2xl font-bold text-cyber-blue">
                {riskStats.total}
              </div>
              <div className="text-sm text-gray-400">Total Transactions</div>
            </div>
            <Activity className="text-cyber-blue" size={24} />
          </div>
        </div>

        <div className="data-card rounded-lg p-4">
          <div className="flex items-center justify-between">
            <div>
              <div className="cyber-text text-2xl font-bold text-cyber-red">
                {riskStats.suspicious}
              </div>
              <div className="text-sm text-gray-400">Suspicious</div>
            </div>
            <AlertTriangle className="text-cyber-red" size={24} />
          </div>
        </div>

        <div className="data-card rounded-lg p-4">
          <div className="flex items-center justify-between">
            <div>
              <div className="cyber-text text-2xl font-bold text-cyber-yellow">
                {riskStats.highRisk}
              </div>
              <div className="text-sm text-gray-400">High Risk</div>
            </div>
            <TrendingUp className="text-cyber-yellow" size={24} />
          </div>
        </div>

        <div className="data-card rounded-lg p-4">
          <div className="flex items-center justify-between">
            <div>
              <div className="cyber-text text-2xl font-bold text-cyber-green">
                {riskStats.confirmed}
              </div>
              <div className="text-sm text-gray-400">Verified</div>
            </div>
            <CheckCircle className="text-cyber-green" size={24} />
          </div>
        </div>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Transaction List */}
        <div className="lg:col-span-2">
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="data-card rounded-lg p-6"
          >
            {/* Controls */}
            <div className="flex flex-col sm:flex-row gap-4 mb-6">
              <div className="relative flex-1">
                <Search size={18} className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
                <input
                  type="text"
                  placeholder="Search transactions..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full bg-dark-bg border border-gray-600 rounded-lg pl-10 pr-4 py-2 text-white placeholder-gray-400"
                />
              </div>
              
              <select
                value={filter}
                onChange={(e) => setFilter(e.target.value)}
                className="bg-dark-bg border border-gray-600 rounded-lg px-4 py-2 text-white"
              >
                <option value="all">All Types</option>
                <option value="financial">Financial</option>
                <option value="policy">Policy</option>
                <option value="vote">Votes</option>
                <option value="suspicious">Suspicious</option>
              </select>
            </div>

            {/* Transaction List */}
            <div className="space-y-3 max-h-[600px] overflow-y-auto scrollbar-cyber">
              {filteredTransactions.map((tx, index) => {
                const IconComponent = getTypeIcon(tx.type)
                const statusColor = getStatusColor(tx.status)
                
                return (
                  <motion.div
                    key={tx.id}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: index * 0.05 }}
                    onClick={() => setSelectedTransaction(tx)}
                    className={`
                      p-4 rounded-lg border cursor-pointer transition-all duration-200
                      ${selectedTransaction?.id === tx.id
                        ? 'bg-cyber-blue/20 border-cyber-blue'
                        : 'bg-dark-accent/50 border-gray-600 hover:border-gray-400 hover:bg-dark-accent'
                      }
                    `}
                  >
                    <div className="flex items-start justify-between mb-2">
                      <div className="flex items-center gap-3">
                        <IconComponent size={18} className={`text-${statusColor}`} />
                        <div>
                          <div className="font-mono text-sm text-gray-300">
                            {formatAddress(tx.id)}
                          </div>
                          <div className="font-medium text-white">
                            {tx.description}
                          </div>
                        </div>
                      </div>
                      
                      <div className="text-right">
                        <div className={`text-sm font-bold text-${statusColor}`}>
                          {formatAmount(tx.amount)}
                        </div>
                        <div className="text-xs text-gray-400">
                          {formatTime(tx.timestamp)}
                        </div>
                      </div>
                    </div>

                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <div className={`px-2 py-1 rounded text-xs bg-${statusColor}/20 text-${statusColor}`}>
                          {tx.status.toUpperCase()}
                        </div>
                        <div className="text-xs text-gray-400">
                          Confidence: {tx.confidence}%
                        </div>
                      </div>

                      <div className="flex gap-1">
                        {tx.tags.slice(0, 2).map(tag => (
                          <span key={tag} className="text-xs bg-gray-700 text-gray-300 px-2 py-1 rounded">
                            {tag}
                          </span>
                        ))}
                        {tx.tags.length > 2 && (
                          <span className="text-xs text-gray-400">
                            +{tx.tags.length - 2}
                          </span>
                        )}
                      </div>
                    </div>
                  </motion.div>
                )
              })}
            </div>
          </motion.div>
        </div>

        {/* Transaction Details */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          className="data-card rounded-lg p-6"
        >
          {selectedTransaction ? (
            <>
              <div className="flex items-center justify-between mb-4">
                <h3 className="cyber-text text-lg font-bold text-cyber-green">
                  Transaction Details
                </h3>
                <div className={`px-2 py-1 rounded text-xs bg-${getStatusColor(selectedTransaction.status)}/20 text-${getStatusColor(selectedTransaction.status)}`}>
                  {selectedTransaction.status.toUpperCase()}
                </div>
              </div>

              <div className="space-y-4">
                <div>
                  <div className="text-sm font-semibold text-gray-300 mb-1">Transaction Hash</div>
                  <div className="font-mono text-xs text-gray-400 bg-dark-bg p-2 rounded">
                    {selectedTransaction.id}
                  </div>
                </div>

                <div>
                  <div className="text-sm font-semibold text-gray-300 mb-1">Description</div>
                  <div className="text-sm text-white">
                    {selectedTransaction.description}
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <div className="text-sm font-semibold text-gray-300 mb-1">From</div>
                    <div className="font-mono text-xs text-gray-400">
                      {typeof selectedTransaction.from === 'string' && selectedTransaction.from.startsWith('0x') 
                        ? formatAddress(selectedTransaction.from)
                        : selectedTransaction.from
                      }
                    </div>
                  </div>
                  <div>
                    <div className="text-sm font-semibold text-gray-300 mb-1">To</div>
                    <div className="font-mono text-xs text-gray-400">
                      {typeof selectedTransaction.to === 'string' && selectedTransaction.to.startsWith('0x')
                        ? formatAddress(selectedTransaction.to)
                        : selectedTransaction.to
                      }
                    </div>
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <div className="text-sm font-semibold text-gray-300 mb-1">Amount</div>
                    <div className="text-lg font-bold text-cyber-blue">
                      {formatAmount(selectedTransaction.amount)}
                    </div>
                  </div>
                  <div>
                    <div className="text-sm font-semibold text-gray-300 mb-1">Confidence</div>
                    <div className="text-lg font-bold text-cyber-green">
                      {selectedTransaction.confidence}%
                    </div>
                  </div>
                </div>

                <div>
                  <div className="text-sm font-semibold text-gray-300 mb-2">Tags</div>
                  <div className="flex flex-wrap gap-2">
                    {selectedTransaction.tags.map(tag => (
                      <span key={tag} className="text-xs bg-gray-700 text-gray-300 px-2 py-1 rounded">
                        {tag}
                      </span>
                    ))}
                  </div>
                </div>

                {selectedTransaction.details && (
                  <div>
                    <div className="text-sm font-semibold text-gray-300 mb-2">Additional Details</div>
                    <div className="bg-dark-bg p-3 rounded text-xs">
                      <pre className="text-gray-400 whitespace-pre-wrap">
                        {JSON.stringify(selectedTransaction.details, null, 2)}
                      </pre>
                    </div>
                  </div>
                )}
              </div>

              {/* Actions */}
              <div className="mt-6 pt-4 border-t border-gray-700 flex gap-2">
                <button className="cyber-button text-xs px-3 py-2 flex items-center gap-2">
                  <Eye size={14} />
                  View on Explorer
                </button>
                {selectedTransaction.status === 'suspicious' && (
                  <button className="cyber-button text-xs px-3 py-2 flex items-center gap-2">
                    <AlertTriangle size={14} />
                    Report Threat
                  </button>
                )}
              </div>
            </>
          ) : (
            <div className="flex items-center justify-center h-full text-gray-400">
              <div className="text-center">
                <Hash size={48} className="mx-auto mb-4" />
                <p>Select a transaction to view details</p>
              </div>
            </div>
          )}
        </motion.div>
      </div>

      {/* Real-time indicator */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.5 }}
        className="fixed bottom-8 left-8 z-50 flex items-center gap-2 bg-dark-card/90 backdrop-blur-lg border border-cyber-green/30 rounded-lg px-4 py-2"
      >
        <div className="pulse-dot bg-cyber-green"></div>
        <span className="cyber-text text-sm text-cyber-green">LIVE MONITORING</span>
      </motion.div>
    </div>
  )
}

export default BlockchainExplorer