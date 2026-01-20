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
import { Line } from 'react-chartjs.2'
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

function Analytics