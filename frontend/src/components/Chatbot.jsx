import { useState, useEffect, useRef } from 'react'
import axios from 'axios'

const API = 'http://localhost:8000'

export default function Chatbot({ employee, prediction }) {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [gridLabel, setGridLabel] = useState('')
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => { scrollToBottom() }, [messages])

  // When employee + prediction change, fetch initial advice
  useEffect(() => {
    if (!employee || !prediction) return

    const fetchAdvice = async () => {
      setLoading(true)
      setMessages([])
      try {
        const res = await axios.post(`${API}/api/chat`, {
          employee_id: employee.id,
          message: '',
          grid_label: prediction.label || ''
        })
        setMessages(res.data.messages || [])
        setGridLabel(res.data.grid_label || '')
      } catch (e) {
        setMessages([{
          role: 'assistant',
          content: 'Sorry, I could not fetch advice right now. Please try again.'
        }])
      } finally {
        setLoading(false)
      }
    }
    fetchAdvice()
  }, [employee?.id, prediction?.label])

  const handleSend = async () => {
    if (!input.trim() || !employee) return
    const userMsg = input.trim()
    setInput('')
    setMessages(prev => [...prev, { role: 'user', content: userMsg }])
    setLoading(true)

    try {
      const res = await axios.post(`${API}/api/chat`, {
        employee_id: employee.id,
        message: userMsg,
        grid_label: gridLabel
      })
      setMessages(prev => [...prev, ...(res.data.messages || [])])
    } catch (e) {
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: 'Sorry, something went wrong. Please try again.'
      }])
    } finally {
      setLoading(false)
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  // Simple markdown-like rendering
  const renderContent = (text) => {
    if (!text) return null
    const lines = text.split('\n')
    return lines.map((line, i) => {
      // Headers
      if (line.startsWith('## ')) {
        return <h2 key={i}>{line.slice(3)}</h2>
      }
      // Bold
      let processed = line
      const parts = []
      let lastIndex = 0
      const boldRegex = /\*\*(.*?)\*\*/g
      let match
      while ((match = boldRegex.exec(processed)) !== null) {
        if (match.index > lastIndex) {
          parts.push(processed.slice(lastIndex, match.index))
        }
        parts.push(<strong key={`b${i}-${match.index}`}>{match[1]}</strong>)
        lastIndex = match.index + match[0].length
      }
      if (lastIndex < processed.length) {
        parts.push(processed.slice(lastIndex))
      }
      // List items
      if (line.startsWith('- ')) {
        return <li key={i} style={{ marginLeft: 16 }}>{parts.length > 0 ? parts : line.slice(2)}</li>
      }
      if (line.trim() === '') return <br key={i} />
      return <p key={i} style={{ margin: '2px 0' }}>{parts.length > 0 ? parts : line}</p>
    })
  }

  return (
    <div className="glass-card chatbot-wrapper">
      <div className="chatbot-header">
        <div className="bot-avatar">🤖</div>
        <div className="bot-info">
          <h3>HR Advisor</h3>
          <p>{employee ? `Analyzing ${employee.name}` : 'Select an employee to start'}</p>
        </div>
      </div>

      {messages.length === 0 && !loading ? (
        <div className="chat-empty">
          <div className="empty-icon">💬</div>
          <p>Upload a dataset and select an employee to get personalized improvement advice</p>
        </div>
      ) : (
        <div className="chat-messages">
          {messages.map((msg, i) => (
            <div key={i} className={`chat-message ${msg.role}`}>
              {renderContent(msg.content)}
            </div>
          ))}
          {loading && (
            <div className="chat-message assistant">
              <div className="spinner" style={{ width: 20, height: 20 }} />
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
      )}

      <div className="chat-input-area">
        <input
          type="text"
          className="chat-input"
          placeholder={employee ? 'Ask about training, promotion, retention...' : 'Select an employee first'}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={!employee || loading}
        />
        <button
          className="chat-send-btn"
          onClick={handleSend}
          disabled={!employee || !input.trim() || loading}
        >
          Send
        </button>
      </div>
    </div>
  )
}
