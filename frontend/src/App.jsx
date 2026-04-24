import { useState, useEffect } from 'react'
import FileUploader from './components/FileUploader'
import SearchBar from './components/SearchBar'
import NineBoxGrid from './components/NineBoxGrid'
import ModelInfo from './components/ModelInfo'
import Chatbot from './components/Chatbot'

function App() {
  const [theme, setTheme] = useState(() => localStorage.getItem('theme') || 'light')
  const [datasetInfo, setDatasetInfo] = useState(null)
  const [modelInfo, setModelInfo] = useState(null)
  const [selectedEmployee, setSelectedEmployee] = useState(null)
  const [prediction, setPrediction] = useState(null)

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme)
    localStorage.setItem('theme', theme)
  }, [theme])

  const toggleTheme = () => setTheme(t => t === 'light' ? 'dark' : 'light')

  const handleUploadSuccess = (data) => {
    setDatasetInfo(data)
    setModelInfo(data.model_info)
    setSelectedEmployee(null)
    setPrediction(null)
  }

  const handleEmployeeSelect = (emp) => {
    setSelectedEmployee(emp)
    setPrediction(null)
  }

  const handlePrediction = (pred) => {
    setPrediction(pred)
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>◈ 9-Box Grid Predictor</h1>
        <div className="header-actions">
          <span className="theme-label">{theme === 'light' ? '☀️ Light' : '🌙 Dark'}</span>
          <button
            className={`theme-toggle ${theme === 'dark' ? 'dark' : ''}`}
            onClick={toggleTheme}
            aria-label="Toggle theme"
          />
        </div>
      </header>

      <main className="app-layout">
        <div className="left-panel">
          <FileUploader onUploadSuccess={handleUploadSuccess} />

          {modelInfo && <ModelInfo info={modelInfo} />}

          {datasetInfo && (
            <SearchBar
              datasetId={datasetInfo.dataset_id}
              onSelect={handleEmployeeSelect}
              onPrediction={handlePrediction}
            />
          )}

          <div className="glass-card nine-box-wrapper">
            <h2>📊 9-Box Grid Framework</h2>
            <NineBoxGrid prediction={prediction} />
          </div>
        </div>

        <div className="right-panel">
          <Chatbot
            employee={selectedEmployee}
            prediction={prediction}
          />
        </div>
      </main>
    </div>
  )
}

export default App
