import React, { useState, useEffect, useRef } from 'react';
import './ChatPanel.css';

const ChatPanel = ({ onSendMessage, messages, isBuilding }) => {
  const [input, setInput] = useState('');
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim() && !isBuilding) {
      onSendMessage(input.trim());
      setInput('');
    }
  };

  return (
    <div className="chat-panel">
      <div className="chat-header">
        <h2>🚀 Toshokan Code Builder</h2>
        <p>Describe your app and I'll build it</p>
      </div>

      <div className="chat-messages">
        {messages.length === 0 && (
          <div className="welcome-message">
            <h3>Welcome! 👋</h3>
            <p>Tell me what you want to build. For example:</p>
            <ul>
              <li>"Create a landing page with hero section and image gallery"</li>
              <li>"Build a signup and login system with Firebase"</li>
              <li>"Make a profile screen with edit options"</li>
            </ul>
          </div>
        )}

        {messages.map((msg, idx) => (
          <div key={idx} className={`message message-${msg.role}`}>
            <div className="message-header">
              <span className="message-role">
                {msg.role === 'user' ? '👤 You' : msg.role === 'assistant' ? '🤖 Assistant' : '⚙️ System'}
              </span>
              <span className="message-time">{msg.timestamp}</span>
            </div>
            <div className="message-content">
              {msg.content}
            </div>
          </div>
        ))}

        {isBuilding && (
          <div className="message message-system">
            <div className="message-content">
              <div className="loading-spinner"></div>
              Building your app...
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      <form className="chat-input-form" onSubmit={handleSubmit}>
        <input
          type="text"
          className="chat-input"
          placeholder="Describe your app..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          disabled={isBuilding}
        />
        <button 
          type="submit" 
          className="send-button"
          disabled={isBuilding || !input.trim()}
        >
          {isBuilding ? '⏳' : '➤'}
        </button>
      </form>
    </div>
  );
};

export default ChatPanel;
