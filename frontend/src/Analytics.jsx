import {useState, useEffect} from 'react'
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
import './Analytics.css'

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
)

const READINGS_API = 'http://127.0.0.1:5001/api/readings'
const STATS_API = 'http://127.0.0.1:5001/api/stats'

function Analytics() {
    const [stats, setStats] = useState(null)
    const [readings, setReadings] = useState([])
    const [loading, setLoading] = useState(true)
    const [limit, setLimit] = useState(100)

    useEffect(() => {
        fetchData()
    }, [limit])

    const fetchData = async () => {
        setLoading(true)
        try {
            //fetch stats and readings
            const [statsRes, readingsRes] = await Promise.all([
                fetch(`${STATS_API}?limit=${limit}`),
                fetch(`${READINGS_API}?limit=${limit}`),
            ])

            const statsData = await statsRes.json()
            const readingsData = await readingsRes.json()

            setStats(statsData)
            setReadings(readingsData.readings || [])
        }   catch (error) {
            console.error('Failed to fetch analytics:', error)
        }
        setLoading(false)
    }

    //prepares chart data (oldest first)
    const chartData = readings.slice().reverse()

    const timestamps = chartData.map(r => {
        const date = new Date(r.timestamp)
        return date.toLocaleTimeString()
    })

    const chartOptions = {
        responsive: true,
        maintainAspectRation: false,
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
                ticks: {
                    maxticketsLimit: 10,
                    font: { size: 10 }
                }
            },
            y: {
                ticks: {
                    maxTicketsLimit: 10,
                    font: { size: 10 }
                }
            }
        },
        elements: {
            point: {
                radius: 2
            },
            line: {
                tension: 0.4
            }
        }
    }

    const TempChartData = {
        labels: timestamps,
        datasets: [{
            label: 'Temperature',
            data: chartData.map(r => r.temperature),
            borderColor: '#ef4444',
            backgroundColor: 'rgba(239, 68, 68, 0.1)',
            borderWidth: 2,
            fill: true
        }]
    }

    const humidityChartData = {
        labels: timestamps,
        datasets: [{
            label: 'Humidity',
            data: chartData.map(r => r.humidity),
            borderColor: '#3b82f6',
            backgroundColor: 'rgba(59, 130, 246, 0.1)',
            borderWidth: 2,
            fill: true
        }]
    }

    const airQualityChartData = {
        labels: timestamps,
        datasets: [{
            label: 'Air Quality',
            data: chartData.map(r => r.air_quality),
            borderColor: '#10b981',
            backgroundColor: 'rgba(16, 185, 129, 0.1)',
            borderWidth: 2,
            fill: true
        }]
    }

    if (loading) {
        return (
            <div className="container">
                <div className="loading">Loading analytics...</div>
            </div>
        )
    }

    if (!stats) {
        return (
            <div className="container">
                <div className="error">No data available</div>
            </div>
        )
    }

    return (
        <div className="container">
            <header>
                <h1>Analytics</h1>
                <p className="subtitle">Statistical Analysis & Historical Trends</p>
            </header>

            <div className="controls">
                <label>
                    Data Range:
                    <select value={limit} onChange={(e) => setLimit(Number(e.target.value))}>
                        <option value={50}>Last 50 readings</option>
                        <option value={100}>Last 100 readings</option>
                        <option value={200}>Last 200 readings</option>
                        <option value={500}>Last 500 readings</option>
                    </select>
                </label>
                <a href="/" className="back-link">Back to Dashboard</a>
            </div>

            <div className="stats-summary">
                <div className="stat-card">
                    <h3>Temperature</h3>
                    <div className="stat-row">
                        <span>Min:</span>
                        <span>{stats.temperature.min.toFixed(1)}°F</span>
                    </div>
                    <div className="stat-row">
                        <span>Max:</span>
                        <span>{stats.temperature.max.toFixed(1)}°F</span>
                    </div>
                    <div className="stat-row highlight">
                        <span>Avg:</span>
                        <span>{stats.temperature.avg.toFixed(1)}°F</span>
                    </div>
                </div>

                <div className="stat-card">
                    <h3>Humidity</h3>
                    <div className="stat-row">
                        <span>Min:</span>
                        <span>{stats.humidity.min.toFixed(1)}%</span>
                    </div>
                    <div className="stat-row">
                        <span>Max:</span>
                        <span>{stats.humidity.max.toFixed(1)}%</span>
                    </div>
                    <div className="stat-row highlight">
                        <span>Avg:</span>
                        <span>{stats.humidity.avg.toFixed(1)}%</span>
                    </div>
                </div>

                <div className="stat-card">
                    <h3>Air Quality</h3>
                    <div className="stat-row">
                        <span>Min:</span>
                        <span>{stats.air_quality.min.toFixed(1)}</span>
                    </div>
                    <div className="stat-row">
                        <span>Max:</span>
                        <span>{stats.air_quality.max.toFixed(1)}</span>
                    </div>
                    <div className="stat-row highlight">
                        <span>Avg:</span>
                        <span>{Math.round(stats.air_quality.avg)}</span>
                    </div>
                </div>
            </div>

            <div className="chart-section">
                <h2>Temperature Trend</h2>
                <div className="large-chart">
                    <Line data={tempChartData} options={chartOptions} />
                </div>
            </div>

            <div className="chart-section">
                <h2>Humidity Trend</h2>
                <div className="large-chart">
                    <Line data={humidityChartData} options={chartOptions} />
                </div>
            </div>

            <div className="chart-section">
                <h2>Air Quality Trend</h2>
                <div className="large-chart">
                    <Line data={airQualityChartData} options={chartOptions} />
                </div>
            </div>

            <div className="into-text">
                Showing data from {stats.count} readings
            </div>
        </div>
    )
}

export default Analytics