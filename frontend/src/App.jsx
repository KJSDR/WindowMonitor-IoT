import { useState } from 'react'
import './App.css'

const API_URL = 'http://127.0.0.1:5001/api/latest'

function App() {
  const [data, setData] = useState({
    temp: 0,
    humidity: 0,
    air_quality: 0,
    recommendation: 'LOADING',
    reason: 'Connecting to sensors...'
  })
  const [lastUpdate, setLastUpdate] = useState(null)

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
      setLastUpdate(new Date())
    } catch (error) {
      console.error('Failed to fetch:', error)
    }
  }

  const isOpen = data.recommendation === 'OPEN'

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
        </div>

        <div className="sensor-card">
          <div className="sensor-value">{data.humidity.toFixed(1)}%</div>
          <div className="sensor-label">Humidity</div>
        </div>

        <div className="sensor-card">
          <div className="sensor-value">{data.air_quality}</div>
          <div className="sensor-label">Air Quality</div>
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