import React, { useState, useEffect } from 'react'
import ChatPanel from './components/ChatPanel'
import CodeViewer from './components/CodeViewer'
import { getModules, buildApp } from './services/api'
import './App.css'

function App() {
  const [modules, setModules] = useState([])
  const [messages, setMessages] = useState([])
  const [currentSession, setCurrentSession] = useState(null)
  const [files, setFiles] = useState([])
  const [isBuilding, setIsBuilding] = useState(false)

  useEffect(() => {
    loadModules()
  }, [])

  const loadModules = async () => {
    try {
      const data = await getModules()
      setModules(data)
      setMessages([{
        role: 'system',
        content: `Welcome! I have ${data.length} modules available: ${data.map(m => m.module_id).join(', ')}. What would you like to build?`
      }])
    } catch (error) {
      console.error('Failed to load modules:', error)
      setMessages([{
        role: 'system',
        content: 'Error connecting to backend. Please ensure the server is running on port 8000.'
      }])
    }
  }

  const handleSendMessage = async (userMessage) => {
    setMessages(prev => [...prev, { role: 'user', content: userMessage }])
    setIsBuilding(true)

    try {
      const response = await buildApp(userMessage)
      
      setCurrentSession(response.session_id)
      setFiles(response.files)
      
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: response.message || `Successfully generated ${response.files.length} files!`
      }])

      if (response.setup_warnings && response.setup_warnings.length > 0) {
        setMessages(prev => [...prev, {
          role: 'system',
          content: `⚠️ Setup Required:\n${response.setup_warnings.join('\n')}`
        }])
      }
    } catch (error) {
      console.error('Build failed:', error)
      setMessages(prev => [...prev, {
        role: 'system',
        content: `Error: ${error.message || 'Failed to build app'}`
      }])
    } finally {
      setIsBuilding(false)
    }
  }

  return (
    <div className="app">
      <ChatPanel 
        messages={messages}
        onSendMessage={handleSendMessage}
        isBuilding={isBuilding}
      />
      <CodeViewer 
        files={files}
        sessionId={currentSession}
      />
    </div>
  )
}

export default App
