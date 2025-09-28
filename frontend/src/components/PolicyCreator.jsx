import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { 
  FileText, 
  Target, 
  Zap, 
  Users, 
  Building, 
  Droplets, 
  Truck, 
  DollarSign,
  Send,
  Save,
  Eye,
  Lightbulb,
  TrendingUp,
  AlertCircle
} from 'lucide-react'
import { useGame } from '../context/GameContext'
import toast from 'react-hot-toast'

const PolicyCreator = () => {
  const { departments, submitProposal, loading } = useGame()
  
  const [formData, setFormData] = useState({
    title: '',
    targetDepartment: '',
    description: '',
    priority: 'medium',
    expectedImpact: 'moderate'
  })
  
  const [step, setStep] = useState(1)
  const [aiSuggestions, setAiSuggestions] = useState([])

  const departmentIcons = {
    'ENERGY': { icon: Zap, color: 'cyber-yellow' },
    'TRANSPORTATION': { icon: Truck, color: 'cyber-blue' },
    'HOUSING': { icon: Building, color: 'cyber-purple' },
    'WASTE': { icon: Target, color: 'cyber-green' },
    'WATER': { icon: Droplets, color: 'cyan-400' },
    'ECONOMIC_DEV': { icon: DollarSign, color: 'green-400' }
  }

  const policyTemplates = {
    'ENERGY': [
      'Solar Panel Incentive Program',
      'Green Building Standards',
      'Energy Efficiency Retrofits',
      'Community Solar Gardens'
    ],
    'TRANSPORTATION': [
      'Electric Bus Fleet Expansion',
      'Bike Lane Infrastructure',
      'Car-Free City Center',
      'Electric Vehicle Charging Network'
    ],
    'HOUSING': [
      'Affordable Green Housing Initiative',
      'Zero-Emission Building Code',
      'Urban Density Optimization',
      'Community Land Trust Program'
    ],
    'WASTE': [
      'Zero-Waste Initiative',
      'Circular Economy Program',
      'Composting Infrastructure',
      'Plastic Reduction Mandate'
    ],
    'WATER': [
      'Rainwater Harvesting System',
      'Water Conservation Incentives',
      'Green Infrastructure Expansion',
      'Smart Water Management'
    ],
    'ECONOMIC_DEV': [
      'Green Jobs Training Program',
      'Sustainable Business Incentives',
      'Carbon Credit Marketplace',
      'Innovation Hub Development'
    ]
  }

  const handleInputChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }))
    
    // Generate AI suggestions when department is selected
    if (field === 'targetDepartment' && value) {
      generateAISuggestions(value)
    }
  }

  const generateAISuggestions = (department) => {
    // Simulate AI-generated suggestions based on current game state
    const departmentData = departments?.find(d => d.id === department)
    const score = departmentData?.sustainability_score || 50
    
    const suggestions = []
    
    if (score < 30) {
      suggestions.push({
        type: 'urgent',
        title: 'Emergency Action Required',
        suggestion: `${departmentData?.name || department} needs immediate intervention. Consider emergency funding and rapid deployment policies.`
      })
    }
    
    if (score < 50) {
      suggestions.push({
        type: 'improvement',
        title: 'Strategic Enhancement',
        suggestion: `Focus on infrastructure improvements and stakeholder engagement for ${departmentData?.name || department}.`
      })
    }
    
    suggestions.push({
      type: 'innovation',
      title: 'Innovation Opportunity',
      suggestion: `Consider cutting-edge technology integration and public-private partnerships.`
    })
    
    setAiSuggestions(suggestions)
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!formData.title || !formData.targetDepartment || !formData.description) {
      toast.error('Please fill in all required fields')
      return
    }
    
    try {
      await submitProposal(formData.title, formData.description, formData.targetDepartment)
      
      // Reset form
      setFormData({
        title: '',
        targetDepartment: '',
        description: '',
        priority: 'medium',
        expectedImpact: 'moderate'
      })
      setStep(1)
      setAiSuggestions([])
      
      toast.success('Policy proposal submitted successfully!')
    } catch (error) {
      toast.error('Failed to submit proposal')
    }
  }

  const useTemplate = (template) => {
    setFormData(prev => ({ ...prev, title: template }))
    setStep(2)
  }

  const formatDepartmentName = (id) => {
    const dept = departments?.find(d => d.id === id)
    return dept?.name || id.replace(/_/g, ' ')
  }

  return (
    <div className="container mx-auto px-4">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-8"
      >
        <h1 className="cyber-text text-4xl font-bold mb-4 text-cyber-yellow animate-glow">
          Policy Creator Workshop
        </h1>
        <p className="text-xl text-gray-300">
          Craft strategic sustainability policies to influence Mayor decisions
        </p>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main Form */}
        <div className="lg:col-span-2">
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="data-card rounded-lg p-6"
          >
            {/* Progress Steps */}
            <div className="flex items-center justify-between mb-8">
              {[1, 2, 3].map(num => (
                <div key={num} className="flex items-center">
                  <div className={`
                    w-10 h-10 rounded-full flex items-center justify-center border-2 cyber-text font-bold
                    ${step >= num 
                      ? 'bg-cyber-yellow text-dark-bg border-cyber-yellow' 
                      : 'border-gray-600 text-gray-400'
                    }
                  `}>
                    {num}
                  </div>
                  {num < 3 && (
                    <div className={`w-16 h-1 mx-2 ${step > num ? 'bg-cyber-yellow' : 'bg-gray-600'}`} />
                  )}
                </div>
              ))}
            </div>

            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Step 1: Department and Template Selection */}
              {step === 1 && (
                <motion.div
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  className="space-y-6"
                >
                  <h3 className="cyber-text text-xl font-semibold text-cyber-yellow mb-4">
                    Select Target Department
                  </h3>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {departments?.map((dept, index) => {
                      const { icon: IconComponent, color } = departmentIcons[dept.id] || departmentIcons['ENERGY']
                      
                      return (
                        <motion.button
                          key={dept.id}
                          type="button"
                          initial={{ opacity: 0, y: 10 }}
                          animate={{ opacity: 1, y: 0 }}
                          transition={{ delay: index * 0.05 }}
                          onClick={() => {
                            handleInputChange('targetDepartment', dept.id)
                            setStep(2)
                          }}
                          className={`
                            p-4 rounded-lg border-2 transition-all duration-200 text-left
                            ${formData.targetDepartment === dept.id
                              ? `border-${color} bg-${color}/10`
                              : 'border-gray-600 hover:border-gray-400 bg-dark-accent/50'
                            }
                          `}
                        >
                          <div className="flex items-center gap-3 mb-2">
                            <IconComponent size={24} className={`text-${color}`} />
                            <span className="font-semibold text-white">
                              {formatDepartmentName(dept.id)}
                            </span>
                          </div>
                          <div className="text-sm text-gray-400 mb-2">
                            Current Score: {Math.round(dept.sustainability_score)}%
                          </div>
                          <div className="w-full bg-dark-bg rounded-full h-2">
                            <div 
                              className={`h-full bg-${color} rounded-full`}
                              style={{ width: `${dept.sustainability_score}%` }}
                            />
                          </div>
                        </motion.button>
                      )
                    })}
                  </div>
                </motion.div>
              )}

              {/* Step 2: Policy Details */}
              {step === 2 && (
                <motion.div
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  className="space-y-6"
                >
                  <h3 className="cyber-text text-xl font-semibold text-cyber-yellow mb-4">
                    Policy Details
                  </h3>

                  {/* Quick Templates */}
                  {formData.targetDepartment && (
                    <div className="mb-6">
                      <h4 className="text-sm font-semibold text-gray-300 mb-3">Quick Templates:</h4>
                      <div className="flex flex-wrap gap-2">
                        {policyTemplates[formData.targetDepartment]?.map(template => (
                          <button
                            key={template}
                            type="button"
                            onClick={() => useTemplate(template)}
                            className="text-xs bg-gray-700 hover:bg-gray-600 text-gray-300 px-3 py-1 rounded-full transition-colors"
                          >
                            {template}
                          </button>
                        ))}
                      </div>
                    </div>
                  )}

                  <div>
                    <label className="block text-sm font-semibold text-gray-300 mb-2">
                      Policy Title *
                    </label>
                    <input
                      type="text"
                      value={formData.title}
                      onChange={(e) => handleInputChange('title', e.target.value)}
                      placeholder="Enter a compelling policy title..."
                      className="w-full bg-dark-bg border border-gray-600 rounded-lg px-4 py-3 text-white placeholder-gray-400 focus:border-cyber-yellow focus:outline-none"
                      required
                    />
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-semibold text-gray-300 mb-2">
                        Priority Level
                      </label>
                      <select
                        value={formData.priority}
                        onChange={(e) => handleInputChange('priority', e.target.value)}
                        className="w-full bg-dark-bg border border-gray-600 rounded-lg px-4 py-3 text-white focus:border-cyber-yellow focus:outline-none"
                      >
                        <option value="low">Low Priority</option>
                        <option value="medium">Medium Priority</option>
                        <option value="high">High Priority</option>
                        <option value="urgent">Urgent</option>
                      </select>
                    </div>

                    <div>
                      <label className="block text-sm font-semibold text-gray-300 mb-2">
                        Expected Impact
                      </label>
                      <select
                        value={formData.expectedImpact}
                        onChange={(e) => handleInputChange('expectedImpact', e.target.value)}
                        className="w-full bg-dark-bg border border-gray-600 rounded-lg px-4 py-3 text-white focus:border-cyber-yellow focus:outline-none"
                      >
                        <option value="minimal">Minimal Impact</option>
                        <option value="moderate">Moderate Impact</option>
                        <option value="significant">Significant Impact</option>
                        <option value="transformative">Transformative</option>
                      </select>
                    </div>
                  </div>

                  <div className="flex gap-4">
                    <button
                      type="button"
                      onClick={() => setStep(1)}
                      className="px-6 py-2 border border-gray-600 text-gray-400 rounded-lg hover:text-white hover:border-gray-400 transition-colors"
                    >
                      Back
                    </button>
                    <button
                      type="button"
                      onClick={() => setStep(3)}
                      disabled={!formData.title}
                      className="px-6 py-2 bg-cyber-yellow text-dark-bg rounded-lg hover:bg-yellow-400 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                    >
                      Next: Description
                    </button>
                  </div>
                </motion.div>
              )}

              {/* Step 3: Description and Submit */}
              {step === 3 && (
                <motion.div
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  className="space-y-6"
                >
                  <h3 className="cyber-text text-xl font-semibold text-cyber-yellow mb-4">
                    Policy Description
                  </h3>

                  <div>
                    <label className="block text-sm font-semibold text-gray-300 mb-2">
                      Detailed Description *
                    </label>
                    <textarea
                      value={formData.description}
                      onChange={(e) => handleInputChange('description', e.target.value)}
                      placeholder="Provide a comprehensive description of your policy proposal, including implementation strategy, expected outcomes, and resource requirements..."
                      rows={8}
                      className="w-full bg-dark-bg border border-gray-600 rounded-lg px-4 py-3 text-white placeholder-gray-400 focus:border-cyber-yellow focus:outline-none resize-vertical"
                      required
                    />
                    <div className="text-xs text-gray-400 mt-1">
                      {formData.description.length}/2000 characters
                    </div>
                  </div>

                  <div className="flex gap-4">
                    <button
                      type="button"
                      onClick={() => setStep(2)}
                      className="px-6 py-2 border border-gray-600 text-gray-400 rounded-lg hover:text-white hover:border-gray-400 transition-colors"
                    >
                      Back
                    </button>
                    
                    <button
                      type="submit"
                      disabled={loading || !formData.description}
                      className="flex-1 cyber-button flex items-center justify-center gap-2 py-3"
                    >
                      {loading ? (
                        <>
                          <div className="loading-spinner w-4 h-4"></div>
                          Submitting...
                        </>
                      ) : (
                        <>
                          <Send size={18} />
                          Submit to Mayor
                        </>
                      )}
                    </button>
                  </div>
                </motion.div>
              )}
            </form>
          </motion.div>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* AI Suggestions */}
          {aiSuggestions.length > 0 && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="data-card rounded-lg p-6"
            >
              <h3 className="cyber-text text-lg font-semibold text-cyber-blue mb-4 flex items-center gap-2">
                <Lightbulb size={18} />
                AI Strategy Suggestions
              </h3>

              <div className="space-y-3">
                {aiSuggestions.map((suggestion, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, x: 10 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.1 }}
                    className={`
                      p-3 rounded-lg border-l-4
                      ${suggestion.type === 'urgent' ? 'border-l-cyber-red bg-red-500/10' :
                        suggestion.type === 'improvement' ? 'border-l-cyber-yellow bg-yellow-500/10' :
                        'border-l-cyber-blue bg-blue-500/10'
                      }
                    `}
                  >
                    <h4 className="font-semibold text-white text-sm mb-1">
                      {suggestion.title}
                    </h4>
                    <p className="text-xs text-gray-300">
                      {suggestion.suggestion}
                    </p>
                  </motion.div>
                ))}
              </div>
            </motion.div>
          )}

          {/* Tips */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="data-card rounded-lg p-6"
          >
            <h3 className="cyber-text text-lg font-semibold text-cyber-green mb-4 flex items-center gap-2">
              <TrendingUp size={18} />
              Strategy Tips
            </h3>

            <div className="space-y-3 text-sm text-gray-300">
              <div className="flex items-start gap-2">
                <AlertCircle size={14} className="text-cyber-blue mt-0.5 flex-shrink-0" />
                <span>Target departments with scores below 50% for maximum impact</span>
              </div>
              <div className="flex items-start gap-2">
                <AlertCircle size={14} className="text-cyber-blue mt-0.5 flex-shrink-0" />
                <span>Use specific, measurable goals to increase Mayor trust</span>
              </div>
              <div className="flex items-start gap-2">
                <AlertCircle size={14} className="text-cyber-blue mt-0.5 flex-shrink-0" />
                <span>Counter bad actor proposals with superior alternatives</span>
              </div>
              <div className="flex items-start gap-2">
                <AlertCircle size={14} className="text-cyber-blue mt-0.5 flex-shrink-0" />
                <span>Build coalitions by addressing multiple department needs</span>
              </div>
            </div>
          </motion.div>
        </div>
      </div>
    </div>
  )
}

export default PolicyCreator