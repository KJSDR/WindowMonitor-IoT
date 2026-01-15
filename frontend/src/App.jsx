import { useState, useEffect } from 'react'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js'
import { Line } from 'react-chartjs-2'
import './App.css'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
)

const API_URL = 'http://127.0.0.1:5001/api/latest'
const MAX_DATA_POINTS = 30

function App() {
  const [data, setData] = useState({
    temp: 0,
    humidity: 0,
    air_quality: 0,
    recommendation: 'LOADING',
    reason: 'Connecting to sensors...'
  })
  const [lastUpdate, setLastUpdate] = useState(null)

  const [history, setHistory] = useState({
    temp: [],
    humidity: [],
    air_quality: [],
    timestamps: []
  })

  useEffect(() => {
    fetchData()

    const interval = setInterval(fetchData, 2000)

    return () => clearInterval(interval)
  }, [])

  const fetchData = async () => {
    try {
      const response = await fetch(API_URL)
      const json = await response.json()
      setData(json)

      const now = new Date()
      setLastUpdate(now)

      setHistory(prev => {
        const newHistory = {
          temp: [...prev.temp, json.temp],
          humidity: [...prev.humidity, json.humidity],
          air_quality: [...prev.air_quality, json.air_quality],
          timestamps: [...prev.timestamps, now.toLocaleTimeString()]
        }

        if (newHistory.temp.length > MAX_DATA_POINTS) {
          newHistory.temp = newHistory.temp.slice(-MAX_DATA_POINTS)
          newHistory.humidity = newHistory.humidity.slice(-MAX_DATA_POINTS)
          newHistory.air_quality = newHistory.air_quality.slice(-MAX_DATA_POINTS)
          newHistory.timestamps = newHistory.timestamps.slice(-MAX_DATA_POINTS)
        }
        return newHistory
      })
    } catch (error) {
      console.error('Failed to fetch:, error')
    }
  }

  const isOpen = data.recommendation === 'OPEN'

  const chartOptions = {
    responsive: true,
    maintainAspectRation: false,
    plugins: {
      legend: {
        display: false
      },
      tooltip: {
        x: {
          display: false
        }
      },
      scales: {
        x: {
          display: false
        },
        y: {
          ticks: {
            font: {
              size: 10
            }
          }
        }
      },
      elements: {
        point: {
          radius: 0
        },
        line: {
          tension: 0.4
        }
      }
    }
  }
const tempChartData = {
  labels: history.timestamps,
  datasets: [{
    label: 'Temperature',
    data: history.temp,
    borderColor: '#ef4444',
    backgroundColor: 'rgba(239, 68, 68, 0.1)',
    borderWdith: 2,
    fill: true
  }]
}

const humidityChartData = {
  labels: history.timestamps,
  datasets: [{
    label: 'Humidity',
    data: history.humidity,
    borderColor: '#ef4444',
    backgroundColor: 'rgba(239, 68, 68, 0.1)',
    borderWdith: 2,
    fill: true
  }]
}

const airQualityChartData = {
  labels: history.timestamps,
  datasets: [{
    label: 'Air Quality',
    data: history.air_quality,
    borderColor: '#ef4444',
    backgroundColor: 'rgba(239, 68, 68, 0.1)',
    borderWdith: 2,
    fill: true
  }]
}

  return (
    <div className="container">
      <header>
        <h1>Window Monitor</h1>
        <p className="subtitle">Environmental Monitoring System</p>
      </header>

      <div className="sensor-grid">
        <div className="sensor-card">
          <div className="sensor-value">{data.temp.toFixed(1)}°F</div>
          <div className="sensor-label">Temperature</div>
          <div className="chart-container">
            <Line data={tempChartData} options={chartOptions} />
          </div>
        </div>

        <div className="sensor-card">
          <div className="sensor-value">{data.humidity.toFixed(1)}%</div>
          <div className="sensor-label">Humidity</div>
          <div className="chart-container">
            <Line data={humidityChartData} options={chartOptions} />
          </div>
        </div>

        <div className="sensor-card">
          <div className="sensor-value">{data.air_quality}</div>
          <div className="sensor-label">Air Quality</div>
          <div className="chart-container">
            <Line data={airQualityChartData} options={chartOptions} />
          </div>
        </div>
      </div>

      <div className={`recommendation ${isOpen ? 'open' : 'close'}`}>
        <div className="rec-status">
          {isOpen ? '🟢 WINDOW OPEN' : '🔴 CLOSE WINDOW'}
        </div>
        <div className="rec-reason">{data.reason}</div>
      </div>

      {lastUpdate && (
        <div className="last-update">
          Last update: {lastUpdate.toLocaleTimeString()}
        </div>
      )}
    </div>
  )
}

export default App