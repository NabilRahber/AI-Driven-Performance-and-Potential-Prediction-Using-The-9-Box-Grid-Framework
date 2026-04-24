import { useState, useEffect, useRef } from 'react'
import axios from 'axios'

const API = 'http://localhost:8000'

export default function SearchBar({ datasetId, onSelect, onPrediction }) {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])
  const [showResults, setShowResults] = useState(false)
  const [loading, setLoading] = useState(false)
  const [predicting, setPredicting] = useState(false)
  const wrapperRef = useRef()

  useEffect(() => {
    const handleClickOutside = (e) => {
      if (wrapperRef.current && !wrapperRef.current.contains(e.target)) {
        setShowResults(false)
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  useEffect(() => {
    const timer = setTimeout(async () => {
      if (!datasetId) return
      setLoading(true)
      try {
        const res = await axios.get(`${API}/api/employees`, {
          params: { q: query, dataset_id: datasetId }
        })
        setResults(res.data.employees || [])
        setShowResults(true)
      } catch (e) {
        console.error(e)
      } finally {
        setLoading(false)
      }
    }, 300)
    return () => clearTimeout(timer)
  }, [query, datasetId])

  const handleSelect = async (emp) => {
    setQuery(emp.name)
    setShowResults(false)
    onSelect(emp)
    setPredicting(true)
    try {
      const res = await axios.get(`${API}/api/predict/${emp.id}`)
      onPrediction(res.data.prediction)
    } catch (e) {
      console.error('Prediction failed:', e)
    } finally {
      setPredicting(false)
    }
  }

  return (
    <div className="glass-card" style={{ padding: 0, overflow: 'visible' }}>
      <div className="section-title">Search Employee</div>
      <div ref={wrapperRef} className="search-container" style={{ padding: '0 24px 20px' }}>
        <span className="search-icon">🔍</span>
        <input
          type="text"
          className="search-input"
          placeholder="Type employee name..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onFocus={() => results.length > 0 && setShowResults(true)}
        />
        {predicting && (
          <div style={{ marginTop: 8, display: 'flex', alignItems: 'center', gap: 8 }}>
            <div className="spinner" style={{ width: 16, height: 16 }} />
            <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Predicting...</span>
          </div>
        )}
        {showResults && results.length > 0 && (
          <div className="search-results">
            {results.map((emp) => (
              <div
                key={emp.id}
                className="search-item"
                onClick={() => handleSelect(emp)}
              >
                <strong>{emp.name}</strong>
                {emp.data?.Department && (
                  <span style={{ color: 'var(--text-muted)', marginLeft: 8, fontSize: '0.8rem' }}>
                    {emp.data.Department}
                  </span>
                )}
              </div>
            ))}
          </div>
        )}
        {showResults && results.length === 0 && query && !loading && (
          <div className="search-results">
            <div className="search-item" style={{ color: 'var(--text-muted)' }}>
              No employees found
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
