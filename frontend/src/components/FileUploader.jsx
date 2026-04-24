import { useState, useRef } from 'react'
import axios from 'axios'

const API = 'http://localhost:8000'

export default function FileUploader({ onUploadSuccess }) {
  const [dragging, setDragging] = useState(false)
  const [uploading, setUploading] = useState(false)
  const [uploadedFile, setUploadedFile] = useState(null)
  const [error, setError] = useState(null)
  const inputRef = useRef()

  const handleFile = async (file) => {
    if (!file || !file.name.endsWith('.csv')) {
      setError('Please upload a CSV file.')
      return
    }
    setUploading(true)
    setError(null)
    try {
      const form = new FormData()
      form.append('file', file)
      const res = await axios.post(`${API}/api/upload`, form)
      setUploadedFile({ name: file.name, ...res.data })
      onUploadSuccess(res.data)
    } catch (e) {
      setError(e.response?.data?.detail || 'Upload failed.')
    } finally {
      setUploading(false)
    }
  }

  const onDrop = (e) => {
    e.preventDefault()
    setDragging(false)
    const file = e.dataTransfer.files[0]
    handleFile(file)
  }

  return (
    <div className="glass-card" style={{ padding: 0, overflow: 'hidden' }}>
      <div className="section-title">Dataset Upload</div>
      <div
        className={`upload-area ${dragging ? 'drag-over' : ''}`}
        onDragOver={(e) => { e.preventDefault(); setDragging(true) }}
        onDragLeave={() => setDragging(false)}
        onDrop={onDrop}
        onClick={() => inputRef.current?.click()}
      >
        <input
          ref={inputRef}
          type="file"
          accept=".csv"
          onChange={(e) => handleFile(e.target.files[0])}
        />
        {uploading ? (
          <>
            <div className="spinner" />
            <p style={{ marginTop: 12, color: 'var(--text-muted)' }}>Training models...</p>
          </>
        ) : uploadedFile ? (
          <>
            <span className="upload-icon">✅</span>
            <p className="upload-title">{uploadedFile.name}</p>
            <p className="upload-subtitle">
              {uploadedFile.total_employees} employees loaded • Click to replace
            </p>
            <div className="status-badge success">
              ✓ Best Model: {uploadedFile.model_info?.best_model}
            </div>
          </>
        ) : (
          <>
            <span className="upload-icon">📁</span>
            <p className="upload-title">Drop your CSV file here</p>
            <p className="upload-subtitle">or click to browse files</p>
          </>
        )}
      </div>
      {error && (
        <p style={{ color: 'var(--danger)', padding: '12px 24px', fontSize: '0.85rem' }}>
          ⚠ {error}
        </p>
      )}
    </div>
  )
}
