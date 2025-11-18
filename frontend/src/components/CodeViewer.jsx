import React, { useState, useEffect } from 'react'
import FileExplorer from './FileExplorer'
import CodeEditor from './CodeEditor'
import { getFileContent } from '../services/api'
import './CodeViewer.css'

export default function CodeViewer({ files, sessionId }) {
  const [selectedFile, setSelectedFile] = useState(null)
  const [fileContent, setFileContent] = useState('')
  const [openTabs, setOpenTabs] = useState([])
  const [activeTab, setActiveTab] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleFileSelect = async (file) => {
    if (!sessionId) return

    setLoading(true)
    try {
      const content = await getFileContent(sessionId, file.path)
      
      // Add to tabs if not already open
      if (!openTabs.find(tab => tab.path === file.path)) {
        setOpenTabs(prev => [...prev, { ...file, content }])
      } else {
        // Update content if already open
        setOpenTabs(prev => prev.map(tab => 
          tab.path === file.path ? { ...tab, content } : tab
        ))
      }
      
      setSelectedFile(file)
      setFileContent(content)
      setActiveTab(file.path)
    } catch (error) {
      console.error('Error loading file:', error)
      setFileContent('// Error loading file content')
    } finally {
      setLoading(false)
    }
  }

  const handleTabClose = (path, e) => {
    e.stopPropagation()
    const newTabs = openTabs.filter(tab => tab.path !== path)
    setOpenTabs(newTabs)
    
    if (activeTab === path) {
      const newActiveTab = newTabs.length > 0 ? newTabs[newTabs.length - 1] : null
      if (newActiveTab) {
        setActiveTab(newActiveTab.path)
        setFileContent(newActiveTab.content)
        setSelectedFile(newActiveTab)
      } else {
        setActiveTab(null)
        setFileContent('')
        setSelectedFile(null)
      }
    }
  }

  const handleTabSwitch = (tab) => {
    setActiveTab(tab.path)
    setFileContent(tab.content)
    setSelectedFile(tab)
  }

  return (
    <div className="code-viewer">
      <div className="viewer-header">
        <h3>Generated Code</h3>
        {files.length > 0 && (
          <div className="file-count">{files.length} files</div>
        )}
      </div>

      <div className="viewer-content">
        <FileExplorer 
          files={files}
          selectedFile={selectedFile}
          onFileSelect={handleFileSelect}
        />

        <div className="editor-section">
          {openTabs.length > 0 && (
            <div className="editor-tabs">
              {openTabs.map(tab => (
                <div
                  key={tab.path}
                  className={`editor-tab ${activeTab === tab.path ? 'active' : ''}`}
                  onClick={() => handleTabSwitch(tab)}
                >
                  <span className="tab-name">{tab.path.split('/').pop()}</span>
                  <button
                    className="tab-close"
                    onClick={(e) => handleTabClose(tab.path, e)}
                  >
                    ×
                  </button>
                </div>
              ))}
            </div>
          )}

          <CodeEditor 
            content={fileContent}
            filename={selectedFile?.path}
            loading={loading}
          />
        </div>
      </div>
    </div>
  )
}
