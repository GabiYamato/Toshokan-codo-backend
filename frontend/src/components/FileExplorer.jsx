import React from 'react'
import './FileExplorer.css'

export default function FileExplorer({ files, selectedFile, onFileSelect }) {
  const getFileIcon = (filename) => {
    const ext = filename.split('.').pop()
    const iconMap = {
      'js': '📜',
      'jsx': '⚛️',
      'ts': '📘',
      'tsx': '⚛️',
      'json': '📋',
      'css': '🎨',
      'html': '🌐',
      'md': '📝',
      'py': '🐍',
      'txt': '📄'
    }
    return iconMap[ext] || '📄'
  }

  return (
    <div className="file-explorer">
      <div className="explorer-header">
        <span>FILES</span>
      </div>

      <div className="file-tree">
        {files.length === 0 ? (
          <div className="empty-state">
            <p>No files yet</p>
            <p className="empty-hint">Build an app to see files here</p>
          </div>
        ) : (
          files.map((file, idx) => (
            <div
              key={idx}
              className={`file-item ${selectedFile?.path === file.path ? 'active' : ''}`}
              onClick={() => onFileSelect(file)}
            >
              <span className="file-icon">{getFileIcon(file.path)}</span>
              <span className="file-name">{file.path}</span>
            </div>
          ))
        )}
      </div>
    </div>
  )
}
