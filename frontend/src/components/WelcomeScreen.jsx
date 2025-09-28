import React, { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Play, Zap, Shield, Target, Users, Activity } from 'lucide-react'

const WelcomeScreen = ({ onStart }) => {
  const [currentStep, setCurrentStep] = useState(0)
  const [showIntro, setShowIntro] = useState(true)

  const introSteps = [
    {
      title: "Welcome to Mailopolis",
      subtitle: "The Ultimate Adversarial Sustainability Game",
      description: "You are the city's sustainability strategist, competing against AI adversaries to shape the future.",
      icon: Zap,
      color: "cyber-blue"
    },
    {
      title: "Your Mission",
      subtitle: "Maximize City Sustainability",
      description: "Analyze blockchain data, create policies, and outmaneuver bad actors to achieve maximum sustainability.",
      icon: Target,
      color: "cyber-green"
    },
    {
      title: "The Competition",
      subtitle: "Battle Against Bad Actors",
      description: "Corporate lobbies, corrupt developers, and other adversaries will try to corrupt the Mayor's decisions.",
      icon: Shield,
      color: "cyber-red"
    },
    {
      title: "Your Tools",
      subtitle: "Advanced AI-Powered Arsenal",
      description: "AgentMail communications, blockchain analysis, and strategic policy creation tools at your disposal.",
      icon: Activity,
      color: "cyber-purple"
    }
  ]

  const features = [
    "🏛️ Influence Mayor decisions with strategic policy proposals",
    "🔗 Analyze blockchain transactions for intelligence gathering",
    "📧 Communicate through secure AgentMail system",
    "⚔️ Counter bad actor moves in real-time",
    "📊 Track sustainability metrics across 6 city departments",
    "🎯 25 rounds to maximize city sustainability index"
  ]

  useEffect(() => {
    if (showIntro) {
      const timer = setInterval(() => {
        setCurrentStep((prev) => {
          if (prev >= introSteps.length - 1) {
            clearInterval(timer)
            setTimeout(() => setShowIntro(false), 2000)
            return prev
          }
          return prev + 1
        })
      }, 3000)

      return () => clearInterval(timer)
    }
  }, [showIntro])

  const handleStart = () => {
    onStart()
  }

  const skipIntro = () => {
    setShowIntro(false)
  }

  if (showIntro) {
    const current = introSteps[currentStep]
    const IconComponent = current.icon

    return (
      <div className="min-h-screen bg-dark-bg overflow-hidden relative">
        {/* Animated Background */}
        <div className="absolute inset-0">
          <div className="absolute inset-0 bg-cyber-gradient"></div>
          <div className="absolute inset-0 bg-cyber-grid bg-[size:50px_50px] animate-circuit opacity-20"></div>
          <div className="matrix-rain absolute inset-0"></div>
        </div>

        {/* Main Content */}
        <div className="relative z-10 flex items-center justify-center min-h-screen px-4">
          <AnimatePresence mode="wait">
            <motion.div
              key={currentStep}
              initial={{ opacity: 0, y: 50 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -50 }}
              className="text-center max-w-2xl"
            >
              <motion.div
                initial={{ scale: 0, rotate: -180 }}
                animate={{ scale: 1, rotate: 0 }}
                transition={{ delay: 0.2, type: "spring" }}
                className={`inline-flex items-center justify-center w-24 h-24 rounded-full bg-${current.color}/20 border-2 border-${current.color} mb-8`}
              >
                <IconComponent size={40} className={`text-${current.color}`} />
              </motion.div>

              <motion.h1
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.4 }}
                className="cyber-text text-5xl font-bold mb-4 text-white animate-glow"
              >
                {current.title}
              </motion.h1>

              <motion.h2
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.6 }}
                className={`text-2xl font-semibold mb-6 text-${current.color}`}
              >
                {current.subtitle}
              </motion.h2>

              <motion.p
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.8 }}
                className="text-xl text-gray-300 mb-8 leading-relaxed"
              >
                {current.description}
              </motion.p>

              {/* Progress indicator */}
              <div className="flex justify-center gap-2 mb-8">
                {introSteps.map((_, index) => (
                  <motion.div
                    key={index}
                    className={`h-2 rounded-full transition-all duration-300 ${
                      index === currentStep ? 'w-8 bg-cyber-blue' : 
                      index < currentStep ? 'w-2 bg-cyber-green' : 'w-2 bg-gray-600'
                    }`}
                    animate={{ scale: index === currentStep ? 1.2 : 1 }}
                  />
                ))}
              </div>
            </motion.div>
          </AnimatePresence>
        </div>

        {/* Skip button */}
        <button
          onClick={skipIntro}
          className="absolute top-8 right-8 cyber-button text-sm px-4 py-2"
        >
          Skip Intro
        </button>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-dark-bg overflow-hidden relative">
      {/* Animated Background */}
      <div className="absolute inset-0">
        <div className="absolute inset-0 bg-cyber-gradient"></div>
        <div className="absolute inset-0 bg-cyber-grid bg-[size:50px_50px] animate-circuit opacity-20"></div>
        <div className="matrix-rain absolute inset-0"></div>
      </div>

      {/* Main Content */}
      <div className="relative z-10 flex items-center justify-center min-h-screen px-4">
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          className="max-w-4xl mx-auto text-center"
        >
          {/* Logo and Title */}
          <motion.div
            initial={{ y: -50 }}
            animate={{ y: 0 }}
            transition={{ type: "spring", stiffness: 100 }}
          >
            <h1 className="cyber-text text-7xl font-black mb-4 text-cyber-blue animate-glow">
              MAILOPOLIS
            </h1>
            <h2 className="text-3xl font-bold mb-8 text-cyber-purple">
              Adversarial Sustainability Strategy Game
            </h2>
          </motion.div>

          {/* Game Description */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="mb-12"
          >
            <p className="text-xl text-gray-300 mb-8 leading-relaxed max-w-3xl mx-auto">
              Step into the role of a sustainability strategist in a city where every decision matters. 
              Use advanced AI tools to analyze data, create policies, and outmaneuver corporate adversaries 
              in this high-stakes battle for the city's future.
            </p>

            {/* Features Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
              {features.map((feature, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.5 + index * 0.1 }}
                  className="text-left p-4 rounded-lg bg-dark-card/50 border border-cyber-blue/20"
                >
                  <span className="text-gray-300">{feature}</span>
                </motion.div>
              ))}
            </div>
          </motion.div>

          {/* Action Buttons */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.8 }}
            className="flex flex-col sm:flex-row gap-4 justify-center items-center"
          >
            <button
              onClick={handleStart}
              className="group relative px-8 py-4 bg-gradient-to-r from-cyber-blue to-cyber-purple rounded-lg text-white font-bold text-xl transition-all duration-300 hover:scale-105 hover:shadow-2xl overflow-hidden"
            >
              <span className="relative z-10 flex items-center gap-3">
                <Play size={24} />
                Enter the Game
              </span>
              <motion.div
                className="absolute inset-0 bg-gradient-to-r from-cyber-purple to-cyber-blue opacity-0 group-hover:opacity-100 transition-opacity duration-300"
              />
            </button>

            <div className="text-sm text-gray-400">
              <Users size={16} className="inline mr-2" />
              Single-player AI competition
            </div>
          </motion.div>

          {/* Game Stats */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 1 }}
            className="mt-12 pt-8 border-t border-gray-700"
          >
            <div className="grid grid-cols-2 md:grid-cols-4 gap-6 text-center">
              <div>
                <div className="cyber-text text-2xl font-bold text-cyber-green">25</div>
                <div className="text-sm text-gray-400">Game Rounds</div>
              </div>
              <div>
                <div className="cyber-text text-2xl font-bold text-cyber-blue">6</div>
                <div className="text-sm text-gray-400">City Departments</div>
              </div>
              <div>
                <div className="cyber-text text-2xl font-bold text-cyber-yellow">∞</div>
                <div className="text-sm text-gray-400">Strategic Possibilities</div>
              </div>
              <div>
                <div className="cyber-text text-2xl font-bold text-cyber-purple">AI</div>
                <div className="text-sm text-gray-400">Powered Adversaries</div>
              </div>
            </div>
          </motion.div>
        </motion.div>
      </div>
    </div>
  )
}

export default WelcomeScreen