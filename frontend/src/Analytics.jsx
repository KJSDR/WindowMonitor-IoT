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
        responsive: true;
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
    
    
    


}