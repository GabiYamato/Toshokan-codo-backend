import React from 'react'
import './CodeEditor.css'

export default function CodeEditor({ content, filename, loading }) {
  if (loading) {
    return (
      <div className="code-editor">
        <div className="editor-loading">
          <div className="spinner-large"></div>
          <p>Loading file...</p>
        </div>
      </div>
    )
  }

  if (!content) {
    return (
      <div className="code-editor">
        <div className="editor-empty">
          <div className="empty-icon">📝</div>
          <h3>No file selected</h3>
          <p>Select a file from the explorer to view its contents</p>
        </div>
      </div>
    )
  }

  return (
    <div className="code-editor">
      {filename && (
        <div className="editor-title">
          <span className="title-icon">📄</span>
          <span>{filename}</span>
        </div>
      )}
      <div className="editor-content">
        <pre className="code-display">
          <code>{content}</code>
        </pre>
      </div>
    </div>
  )
}
