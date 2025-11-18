import React, { useState, useRef, useEffect } from 'react'
import './ChatPanel.css'

export default function ChatPanel({ messages, onSendMessage, isBuilding }) {
  const [input, setInput] = useState('')
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSubmit = (e) => {
    e.preventDefault()
    if (input.trim() && !isBuilding) {
      onSendMessage(input.trim())
      setInput('')
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  return (
    <div className="chat-panel">
      <div className="chat-header">
        <h2>🏗️ Toshokan Builder</h2>
        <p className="chat-subtitle">AI-Powered Code Generator</p>
      </div>

      <div className="chat-messages">
        {messages.map((msg, idx) => (
          <div key={idx} className={`message message-${msg.role}`}>
            <div className="message-content">{msg.content}</div>
          </div>
        ))}
        {isBuilding && (
          <div className="message message-system">
            <div className="spinner"></div>
            <div>Building your app...</div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input">
        <form onSubmit={handleSubmit} className="input-wrapper">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Describe your app (e.g., 'landing page with hero and gallery')..."
            disabled={isBuilding}
            className="input-field"
          />
          <button type="submit" disabled={isBuilding || !input.trim()} className="send-button">
            {isBuilding ? 'Building...' : 'Build'}
          </button>
        </form>
      </div>
    </div>
  )
}
