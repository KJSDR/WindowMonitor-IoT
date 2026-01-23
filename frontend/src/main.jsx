import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter, Routes, Route} from 'react-router-dom'
import App from './App.jsx'
import History from './History.jsx'
import Analytics from './Analytics.jsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<App />} />
        <Route path="/history" element={<History />} />
        <Route path="/analytics" element={<Analytics />} />
      </Routes>
    </BrowserRouter>
  </React.StrictMode>,
)