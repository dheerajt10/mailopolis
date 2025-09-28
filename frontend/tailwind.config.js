/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'cyber-blue': '#00d4ff',
        'cyber-purple': '#8b5cf6',
        'cyber-green': '#00ff88',
        'cyber-red': '#ff0055',
        'cyber-yellow': '#ffff00',
        'dark-bg': '#0a0a0f',
        'dark-card': '#1a1a2e',
        'dark-accent': '#16213e',
        'neon-blue': '#0ff',
        'neon-green': '#0f0',
        'neon-pink': '#f0f',
        'grid-dark': '#141425'
      },
      fontFamily: {
        'cyber': ['Orbitron', 'monospace'],
        'game': ['Rajdhani', 'sans-serif'],
      },
      animation: {
        'pulse-glow': 'pulse-glow 2s ease-in-out infinite alternate',
        'neon-flicker': 'neon-flicker 1.5s ease-in-out infinite',
        'data-stream': 'data-stream 20s linear infinite',
        'slide-up': 'slide-up 0.3s ease-out',
        'fade-in': 'fade-in 0.5s ease-out',
        'bounce-in': 'bounce-in 0.6s ease-out',
        'glow': 'glow 2s ease-in-out infinite alternate',
        'circuit': 'circuit 3s linear infinite'
      },
      keyframes: {
        'pulse-glow': {
          '0%': { boxShadow: '0 0 5px rgba(0, 255, 255, 0.5)' },
          '100%': { boxShadow: '0 0 20px rgba(0, 255, 255, 1), 0 0 30px rgba(0, 255, 255, 0.8)' }
        },
        'neon-flicker': {
          '0%, 100%': { opacity: 1 },
          '50%': { opacity: 0.8 }
        },
        'data-stream': {
          '0%': { transform: 'translateY(100vh)' },
          '100%': { transform: 'translateY(-100vh)' }
        },
        'slide-up': {
          '0%': { transform: 'translateY(10px)', opacity: 0 },
          '100%': { transform: 'translateY(0)', opacity: 1 }
        },
        'fade-in': {
          '0%': { opacity: 0 },
          '100%': { opacity: 1 }
        },
        'bounce-in': {
          '0%': { transform: 'scale(0.3)', opacity: 0 },
          '50%': { transform: 'scale(1.05)' },
          '70%': { transform: 'scale(0.9)' },
          '100%': { transform: 'scale(1)', opacity: 1 }
        },
        'glow': {
          '0%': { textShadow: '0 0 5px rgba(0, 255, 255, 0.5)' },
          '100%': { textShadow: '0 0 20px rgba(0, 255, 255, 1), 0 0 30px rgba(0, 255, 255, 0.5)' }
        },
        'circuit': {
          '0%': { backgroundPosition: '0 0' },
          '100%': { backgroundPosition: '50px 50px' }
        }
      },
      backgroundImage: {
        'cyber-grid': 'linear-gradient(rgba(0, 255, 255, 0.1) 1px, transparent 1px), linear-gradient(90deg, rgba(0, 255, 255, 0.1) 1px, transparent 1px)',
        'neon-gradient': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        'cyber-gradient': 'linear-gradient(135deg, #0f0f23 0%, #1a1a2e  50%, #16213e 100%)'
      },
      backdropBlur: {
        xs: '2px'
      }
    },
  },
  plugins: [],
}