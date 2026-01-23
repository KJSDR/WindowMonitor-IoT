import { useState, useEffect } from 'react'
import './History.css'

const API_URL = 'http://127.0.0.1:5001/api/readings'

function History() {
    const [readings, setReadings] = useState([])
    const [loading, setLoading] = useState(true)
    const [limit, setLimit] = useState(100)

    useEffect(() => {
        fetchHistory()
    },    [limit])

    const fetchHistory = async () => {
        setLoading(true)
        try {
            const response = await fetch(`${API_URL}?limit=${limit}`)
            const json = await response.json()
            setReadings(json.readings || [])
        }   catch (error) {
            console.error('Failed to fetch history:', error)
        }
        setLoading(false)
    }

    const formatDate = (timestamp) => {
        const date = new Date(timestamp)
        return date.toLocaleString()
    }

    return (
        <div className="container">
            <header>
                <h1>History</h1>
                <p className="subtitle">Historical Sensor Readings</p>
            </header>

            <div className="controls">
                <label>
                    Show last:
                    <select value={limit} onChange={(e) => setLimit(Number(e.target.value))}>
                        <option value={50}>50 readings</option>
                        <option value={100}>100 readings</option>
                        <option value={200}>200 readings</option>
                        <option value={500}>500 readings</option>
                    </select>
                </label>
                <a href="/" className="back-link">Back to Dashboard</a>
            </div>

            {loading ? (
                <div className="loading">Loading...</div>
            ) : (
                <>
                    <div className="stats">
                        Showing {readings.length} readings
                    </div>
                    
                    <div className="table-container">
                        <table>
                            <thead>
                                <tr>
                                    <th>Time</th>
                                    <th>Temperature</th>
                                    <th>Humidity</th>
                                    <th>Air Quality</th>
                                </tr>
                            </thead>
                            <tbody>
                                {readings.map((reading, index) => (
                                    <tr key={index} className={!reading.is_valid ? 'invalid-row' : ''}>
                                        <td>{formatDate(reading.timestamp)}</td>
                                        <td>
                                            {reading.temperature.toFixed(1)}°F
                                            {!reading.is_valid && (
                                                <span className="warning-icon" title="Unreliable data - validation failed">
                                                ⚠️
                                                </span>
                                            )}
                                        </td>
                                         <td>
                                            {reading.humidity.toFixed(1)}%
                                            {!reading.is_valid && (
                                                <span className="warning-icon" title="Unreliable data - validation failed">
                                                ⚠️
                                                </span>
                                            )}
                                        </td>
                                        <td>
                                            {reading.air_quality}
                                            {!reading.is_valid && (
                                                <span className="warning-icon" title="Unreliable data - validation failed">
                                                ⚠️
                                                </span>
                                            )}
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </>
            )}
        </div>
    )
}

export default History