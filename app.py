import json
import os
import asyncio
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import google.generativeai as genai

# Import the builder
from test import ModuleBasedAppBuilder, _load_env_file

app = FastAPI(title="Toshokan Code Builder", version="1.0.0")

# CORS middleware - Allow React dev server and any other origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load environment
_load_env_file()

# Models
class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str
    timestamp: Optional[str] = None

class BuildRequest(BaseModel):
    prompt: str
    session_id: Optional[str] = None

class BuildResponse(BaseModel):
    session_id: str
    output_dir: str
    status: str
    message: str
    files: List[Dict[str, str]] = []

class FileContent(BaseModel):
    path: str
    content: str

# In-memory storage for chat sessions
chat_sessions: Dict[str, List[ChatMessage]] = {}
build_sessions: Dict[str, Dict] = {}

@app.get("/")
async def root():
    return {"message": "Toshokan Code Builder API", "version": "1.0.0"}

@app.get("/api/modules")
async def get_modules():
    """Get all available modules."""
    try:
        with open("modules.json", "r") as f:
            modules = json.load(f)
        return {"modules": modules, "count": len(modules)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat")
async def chat(message: ChatMessage):
    """Handle chat messages (for conversation history)."""
    session_id = message.timestamp or datetime.utcnow().isoformat()
    
    if session_id not in chat_sessions:
        chat_sessions[session_id] = []
    
    chat_sessions[session_id].append(message)
    
    return {
        "session_id": session_id,
        "message": "Message received",
        "history_length": len(chat_sessions[session_id])
    }

@app.get("/api/chat/{session_id}")
async def get_chat_history(session_id: str):
    """Get chat history for a session."""
    if session_id not in chat_sessions:
        return {"session_id": session_id, "messages": []}
    
    return {
        "session_id": session_id,
        "messages": chat_sessions[session_id]
    }

@app.post("/api/build")
async def build_app(request: BuildRequest):
    """Build an app from a user prompt."""
    try:
        session_id = request.session_id or datetime.utcnow().strftime("%Y%m%d-%H%M%S")
        
        # Initialize builder
        builder = ModuleBasedAppBuilder()
        
        # Store session info
        build_sessions[session_id] = {
            "prompt": request.prompt,
            "status": "building",
            "started_at": datetime.utcnow().isoformat()
        }
        
        # Build the app
        builder.build_app(request.prompt)
        
        # Get the output directory
        output_dir = str(builder.output_dir)
        
        # Collect generated files
        files = []
        for file_path in Path(output_dir).rglob("*"):
            if file_path.is_file():
                rel_path = str(file_path.relative_to(output_dir))
                files.append({
                    "path": rel_path,
                    "name": file_path.name,
                    "size": file_path.stat().st_size
                })
        
        # Update session
        build_sessions[session_id].update({
            "status": "completed",
            "output_dir": output_dir,
            "files": files,
            "completed_at": datetime.utcnow().isoformat()
        })
        
        return BuildResponse(
            session_id=session_id,
            output_dir=output_dir,
            status="completed",
            message=f"Successfully generated {len(files)} files",
            files=files
        )
        
    except Exception as e:
        if session_id in build_sessions:
            build_sessions[session_id]["status"] = "failed"
            build_sessions[session_id]["error"] = str(e)
        
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/build/{session_id}")
async def get_build_status(session_id: str):
    """Get build status for a session."""
    if session_id not in build_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return build_sessions[session_id]

@app.get("/api/files/{session_id}")
async def list_files(session_id: str):
    """List all files in a build session."""
    if session_id not in build_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = build_sessions[session_id]
    if "output_dir" not in session:
        raise HTTPException(status_code=400, detail="Build not completed")
    
    return {"files": session.get("files", [])}

@app.get("/api/file/{session_id}/{file_path:path}")
async def get_file_content(session_id: str, file_path: str):
    """Get content of a specific file."""
    if session_id not in build_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = build_sessions[session_id]
    if "output_dir" not in session:
        raise HTTPException(status_code=400, detail="Build not completed")
    
    full_path = Path(session["output_dir"]) / file_path
    
    if not full_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    try:
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        return {
            "path": file_path,
            "content": content,
            "size": full_path.stat().st_size
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading file: {str(e)}")

@app.websocket("/ws/build")
async def websocket_build(websocket: WebSocket):
    """WebSocket endpoint for real-time build updates."""
    await websocket.accept()
    
    try:
        while True:
            # Receive build request
            data = await websocket.receive_json()
            prompt = data.get("prompt", "")
            
            if not prompt:
                await websocket.send_json({"error": "No prompt provided"})
                continue
            
            session_id = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
            
            # Send status update
            await websocket.send_json({
                "type": "status",
                "message": "Starting build...",
                "session_id": session_id
            })
            
            try:
                # Initialize builder
                builder = ModuleBasedAppBuilder()
                
                await websocket.send_json({
                    "type": "status",
                    "message": "Analyzing prompt..."
                })
                
                # Build the app
                builder.build_app(prompt)
                
                # Get output directory
                output_dir = str(builder.output_dir)
                
                # Collect files
                files = []
                for file_path in Path(output_dir).rglob("*"):
                    if file_path.is_file():
                        rel_path = str(file_path.relative_to(output_dir))
                        files.append({
                            "path": rel_path,
                            "name": file_path.name
                        })
                
                # Send completion
                await websocket.send_json({
                    "type": "complete",
                    "session_id": session_id,
                    "output_dir": output_dir,
                    "files": files,
                    "message": f"Successfully generated {len(files)} files"
                })
                
            except Exception as e:
                await websocket.send_json({
                    "type": "error",
                    "message": str(e)
                })
    
    except WebSocketDisconnect:
        print("WebSocket disconnected")

# Serve static files for the frontend
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
