# Toshokan Code Builder - FastAPI Web Interface

A full-stack application with FastAPI backend and web-based IDE interface for building React applications from natural language prompts.

## Features

- 🤖 **AI-Powered Code Generation**: Uses Gemini 2.0 Flash to analyze prompts and generate code
- 💬 **Chat Interface**: Interactive chat to describe what you want to build
- 📁 **File Explorer**: Browse generated files in a tree structure
- 📝 **Code Editor**: View generated code with syntax highlighting
- 🔄 **Real-time Updates**: WebSocket support for live build progress
- 📦 **11 Pre-built Modules**: Auth, database, UI components, image handling, and more

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements-api.txt
```

### 2. Set Up Environment

Create a `.env` file:

```bash
GEMINI_API_KEY=your_api_key_here
```

Or export it:

```bash
export GEMINI_API_KEY=your_api_key_here
```

### 3. Run the Backend

```bash
python app.py
```

The API will start on `http://localhost:8000`

### 4. Open the Frontend

Open `frontend/index.html` in your browser, or serve it:

```bash
cd frontend
python -m http.server 3000
```

Then visit `http://localhost:3000`

## Usage

1. **Describe Your App**: Type what you want to build in the chat input
   - Example: "landing page with hero section and image gallery"
   - Example: "user authentication app with Firebase and profile editing"

2. **View Generated Code**: Click on files in the explorer to view their content

3. **Access Files**: Generated files are saved in `outputs/<timestamp>-<prompt-slug>/`

## API Endpoints

### GET `/api/modules`
Get all available modules

### POST `/api/build`
Build an app from a prompt
```json
{
  "prompt": "your app description"
}
```

### GET `/api/file/{session_id}/{file_path}`
Get content of a generated file

### WebSocket `/ws/build`
Real-time build updates

## Available Modules

### Authentication & Database
- React Sign Up Screen
- React Login Screen
- React Profile Screen
- Firebase Email Auth
- Firebase Realtime Database
- Firebase Storage

### Landing Page Components
- React Hero Section
- React Feature Grid
- React CTA Section

### Image Handling
- React Image Gallery
- React Image Uploader

## Architecture

```
┌─────────────────┐
│   Frontend      │
│  (HTML/JS/CSS)  │
└────────┬────────┘
         │
         │ HTTP/WebSocket
         ▼
┌─────────────────┐
│  FastAPI Server │
│    (app.py)     │
└────────┬────────┘
         │
         │ Uses
         ▼
┌─────────────────┐
│ ModuleBuilder   │
│   (test.py)     │
└────────┬────────┘
         │
         │ Gemini API
         ▼
┌─────────────────┐
│  Code Generator │
│  (modules.json) │
└─────────────────┘
```

## Development

### Project Structure

```
.
├── app.py                 # FastAPI backend
├── test.py               # Core builder logic
├── modules.json          # Module definitions
├── frontend/
│   └── index.html        # Web interface
├── outputs/              # Generated apps
└── .env                  # API keys (gitignored)
```

### Adding New Modules

Edit `modules.json` and add:

```json
{
  "module_id": "unique_id",
  "module_name": "Display Name",
  "language": "tsx",
  "inputs": ["input1", "input2"],
  "outputs": ["output description"],
  "documentation": "What this module does",
  "code": "actual code here"
}
```

## Troubleshooting

### API Key Not Found
Make sure `GEMINI_API_KEY` is set in `.env` or exported

### CORS Errors
The API allows all origins by default. Adjust in `app.py` if needed

### Port Already in Use
Change the port in `app.py`:
```python
uvicorn.run(app, host="0.0.0.0", port=8001)
```

## License

MIT
