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

//register chartsjs components, this is the stuff it uses
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
)

const API_URL = 'http://127.0.0.1:5001/api/latest' //imports from this link from our flask rest api backend
const MAX_DATA_POINTS = 30 //keeps last 30 readings (ends up being 60 secs at 2s intervals)

function App() {
  //current sensor readings and recommendation
  const [data, setData] = useState({
    temp: 0,
    humidity: 0,
    air_quality: 0,
    recommendation: 'LOADING',
    reason: 'Connecting to sensors...'
  })
  const [lastUpdate, setLastUpdate] = useState(null)
  const [error, setError] = useState(null)

  //history data of the graphs (arrays of past readings)
  const [history, setHistory] = useState({
    temp: [],
    humidity: [],
    air_quality: [],
    timestamps: []
  })
  //fetches data on the component mount every 2s
  useEffect(() => {
    fetchData()

    const interval = setInterval(fetchData, 2000)

    return () => clearInterval(interval) //cleans up on unmount
  }, [])

  const fetchData = async () => {
    try {
      const response = await fetch(API_URL)
      const json = await response.json()
      setData(json)
      setError(null)

      const now = new Date()
      setLastUpdate(now)
      //adds new readings to the history
      setHistory(prev => {
        const newHistory = {
          temp: [...prev.temp, json.temp],
          humidity: [...prev.humidity, json.humidity],
          air_quality: [...prev.air_quality, json.air_quality],
          timestamps: [...prev.timestamps, now.toLocaleTimeString()]
        }
        //keeps on the last max data points cause it prevents memory issues
        if (newHistory.temp.length > MAX_DATA_POINTS) {
          newHistory.temp = newHistory.temp.slice(-MAX_DATA_POINTS)
          newHistory.humidity = newHistory.humidity.slice(-MAX_DATA_POINTS)
          newHistory.air_quality = newHistory.air_quality.slice(-MAX_DATA_POINTS)
          newHistory.timestamps = newHistory.timestamps.slice(-MAX_DATA_POINTS)
        }
        return newHistory
      })
    } catch (error) {
      console.error('Failed to fetch:', error)
      setError('Unable to connect to sensor API')
    }
  }

  const isOpen = data.recommendation === 'OPEN'
  //chartjs config, easy and simple
  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false
      },
      tooltip: {
        mode: 'index',
        intersect: false
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
        tension: 0.4 //smooth curve
      }
    }
  }

//temp chart data config
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
//humidity chart data config
const humidityChartData = {
  labels: history.timestamps,
  datasets: [{
    label: 'Humidity',
    data: history.humidity,
    borderColor: '#3b82f6',
    backgroundColor: 'rgba(59, 130, 246, 0.1)',
    borderWdith: 2,
    fill: true
  }]
}
//aq chart data config
const airQualityChartData = {
  labels: history.timestamps,
  datasets: [{
    label: 'Air Quality',
    data: history.air_quality,
    borderColor: '#10b981',
    backgroundColor: 'rgba(16, 185, 129, 0.1)',
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

      <div className="nav-link">
        <a href="/history">View History</a>
      </div>

      {/* sensor cards for live values and graphs*/}
      {error && (
        <div className="error-banner">
          {error} Check if backend is running on port 5001
          </div>
      )}
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
      {/* window recs based on threshold logic */}
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