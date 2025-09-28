import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { NavLink } from 'react-router-dom'
import { 
  Home, 
  Mail, 
  Activity, 
  FileText, 
  Shield, 
  Menu, 
  X,
  Settings,
  HelpCircle
} from 'lucide-react'

const Navigation = () => {
  const [isOpen, setIsOpen] = useState(false)

  const navItems = [
    { path: '/', icon: Home, label: 'Dashboard', color: 'cyber-blue' },
    { path: '/agentmail', icon: Mail, label: 'AgentMail', color: 'cyber-purple' },
    { path: '/blockchain', icon: Activity, label: 'Blockchain', color: 'cyber-green' },
    { path: '/policy', icon: FileText, label: 'Policy Creator', color: 'cyber-yellow' },
    { path: '/intel', icon: Shield, label: 'Bad Actor Intel', color: 'cyber-red' },
  ]

  const toggleNav = () => setIsOpen(!isOpen)

  return (
    <>
      {/* Mobile menu button */}
      <button
        onClick={toggleNav}
        className="lg:hidden fixed top-4 left-4 z-50 p-2 rounded-lg bg-dark-card border border-cyber-blue/30 text-cyber-blue"
      >
        {isOpen ? <X size={24} /> : <Menu size={24} />}
      </button>

      {/* Navigation sidebar */}
      <motion.nav
        initial={false}
        animate={{ 
          x: isOpen ? 0 : -280,
          opacity: isOpen ? 1 : 0.9
        }}
        className="fixed top-0 left-0 z-40 w-70 h-full bg-dark-card/95 backdrop-blur-lg border-r border-cyber-blue/30 lg:translate-x-0 lg:opacity-100"
      >
        {/* Logo/Header */}
        <div className="p-6 border-b border-cyber-blue/30">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-cyber-blue to-cyber-purple flex items-center justify-center">
              <span className="cyber-text font-bold text-dark-bg">M</span>
            </div>
            <div>
              <h1 className="cyber-text text-lg font-bold text-cyber-blue">
                Mailopolis
              </h1>
              <p className="text-xs text-gray-400">Strategic Command</p>
            </div>
          </div>
        </div>

        {/* Navigation items */}
        <div className="p-4 space-y-2">
          {navItems.map((item, index) => (
            <motion.div
              key={item.path}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.05 }}
            >
              <NavLink
                to={item.path}
                onClick={() => setIsOpen(false)}
                className={({ isActive }) => `
                  group flex items-center gap-3 w-full p-3 rounded-lg transition-all duration-200
                  ${isActive 
                    ? `bg-${item.color}/20 text-${item.color} border border-${item.color}/30` 
                    : 'text-gray-400 hover:text-white hover:bg-white/5'
                  }
                `}
              >
                <item.icon size={20} className="flex-shrink-0" />
                <span className="font-medium">{item.label}</span>
                
                {/* Active indicator */}
                <div className={`
                  ml-auto w-2 h-2 rounded-full transition-all duration-200
                  ${({ isActive }) => isActive 
                    ? `bg-${item.color} opacity-100` 
                    : 'bg-transparent opacity-0'
                  }
                `} />
              </NavLink>
            </motion.div>
          ))}
        </div>

        {/* Bottom section */}
        <div className="absolute bottom-0 left-0 right-0 p-4 border-t border-cyber-blue/30">
          <div className="space-y-2">
            <button className="flex items-center gap-3 w-full p-2 text-gray-400 hover:text-white transition-colors">
              <Settings size={18} />
              <span className="text-sm">Settings</span>
            </button>
            <button className="flex items-center gap-3 w-full p-2 text-gray-400 hover:text-white transition-colors">
              <HelpCircle size={18} />
              <span className="text-sm">Help & Tutorial</span>
            </button>
          </div>
          
          {/* Version info */}
          <div className="mt-4 pt-4 border-t border-gray-700">
            <div className="text-xs text-gray-500">
              Version 2.0.0 • Neural Enhanced
            </div>
          </div>
        </div>
      </motion.nav>

      {/* Overlay for mobile */}
      {isOpen && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          onClick={() => setIsOpen(false)}
          className="lg:hidden fixed inset-0 z-30 bg-black/50 backdrop-blur-sm"
        />
      )}

      {/* Main content padding */}
      <div className="lg:ml-70" />
    </>
  )
}

export default Navigation