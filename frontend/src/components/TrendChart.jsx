import React from 'react'
import { motion } from 'framer-motion'
import { Line } from 'react-chartjs-2'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js'

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
)

const TrendChart = ({ data, title }) => {
  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
        labels: {
          color: '#ffffff',
          font: {
            family: 'Orbitron',
            size: 12
          },
          usePointStyle: true,
        }
      },
      tooltip: {
        backgroundColor: 'rgba(26, 26, 46, 0.9)',
        borderColor: '#00d4ff',
        borderWidth: 1,
        titleColor: '#00d4ff',
        bodyColor: '#ffffff',
        cornerRadius: 8,
      }
    },
    scales: {
      x: {
        grid: {
          color: 'rgba(0, 212, 255, 0.1)',
          drawBorder: false,
        },
        ticks: {
          color: '#9ca3af',
          font: {
            family: 'Rajdhani',
            size: 11
          }
        }
      },
      y: {
        min: 0,
        max: 100,
        grid: {
          color: 'rgba(0, 212, 255, 0.1)',
          drawBorder: false,
        },
        ticks: {
          color: '#9ca3af',
          font: {
            family: 'Rajdhani',
            size: 11
          },
          callback: function(value) {
            return value + '%'
          }
        }
      }
    },
    elements: {
      line: {
        tension: 0.4,
        borderWidth: 3,
      },
      point: {
        radius: 4,
        hoverRadius: 6,
        borderWidth: 2,
      }
    },
    interaction: {
      intersect: false,
      mode: 'index',
    },
    animation: {
      duration: 2000,
      easing: 'easeInOutQuart',
    }
  }

  const chartData = {
    labels: data.map(d => `R${d.round}`),
    datasets: [
      {
        label: 'Sustainability Index',
        data: data.map(d => d.sustainability),
        borderColor: '#00ff88',
        backgroundColor: 'rgba(0, 255, 136, 0.1)',
        fill: true,
        pointBackgroundColor: '#00ff88',
        pointBorderColor: '#ffffff',
      },
      {
        label: 'Mayor Trust',
        data: data.map(d => d.mayorTrust),
        borderColor: '#00d4ff',
        backgroundColor: 'rgba(0, 212, 255, 0.1)',
        fill: false,
        pointBackgroundColor: '#00d4ff',
        pointBorderColor: '#ffffff',
      },
      {
        label: 'Bad Actor Influence',
        data: data.map(d => d.badActorInfluence),
        borderColor: '#ff0055',
        backgroundColor: 'rgba(255, 0, 85, 0.1)',
        fill: false,
        pointBackgroundColor: '#ff0055',
        pointBorderColor: '#ffffff',
      }
    ]
  }

  return (
    <div className="data-card rounded-lg p-6">
      <div className="flex justify-between items-center mb-6">
        <h3 className="cyber-text text-xl font-bold text-cyber-blue">
          {title}
        </h3>
        <div className="flex items-center gap-2">
          <div className="pulse-dot bg-cyber-green"></div>
          <span className="text-xs text-gray-400">Real-time</span>
        </div>
      </div>

      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5 }}
        className="h-64 relative"
      >
        {data && data.length > 0 ? (
          <Line options={chartOptions} data={chartData} />
        ) : (
          <div className="flex items-center justify-center h-full text-gray-400">
            <div className="text-center">
              <div className="loading-spinner mx-auto mb-4"></div>
              <p>Loading trend data...</p>
            </div>
          </div>
        )}
      </motion.div>

      {/* Trend insights */}
      {data && data.length > 1 && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
          className="mt-4 pt-4 border-t border-gray-700"
        >
          <div className="grid grid-cols-3 gap-4 text-sm">
            <div className="text-center">
              <div className="cyber-text text-cyber-green font-bold">
                {Math.round(data[data.length - 1].sustainability)}%
              </div>
              <div className="text-gray-400">Current Sustainability</div>
            </div>
            <div className="text-center">
              <div className="cyber-text text-cyber-blue font-bold">
                {Math.round(data[data.length - 1].mayorTrust)}%
              </div>
              <div className="text-gray-400">Mayor Trust</div>
            </div>
            <div className="text-center">
              <div className="cyber-text text-cyber-red font-bold">
                {Math.round(data[data.length - 1].badActorInfluence)}%
              </div>
              <div className="text-gray-400">Bad Actor Influence</div>
            </div>
          </div>
        </motion.div>
      )}
    </div>
  )
}

export default TrendChart