# Toshokan Code Builder 🏗️

AI-powered modular code generation platform with React frontend and FastAPI backend.

## 🌟 Features

- **AI-Powered Generation**: Uses Google Gemini 2.0 Flash to understand natural language prompts
- **Modular System**: 11 pre-built modules for React components, Firebase integration, and landing pages
- **Modern UI**: React-based IDE with code viewer, file explorer, and chat interface
- **Real-time Updates**: FastAPI backend with WebSocket support
- **Flexible Architecture**: Easy to extend with custom modules

## 📋 Prerequisites

- Python 3.8+
- Node.js 16+
- Google Gemini API key

## 🚀 Quick Start

### 1. Clone and Setup

```bash
cd Toshokan-codo-backend
```

### 2. Configure Environment

Create a `.env` file in the root directory:

```env
GEMINI_API_KEY=your_api_key_here
```

### 3. Start Both Servers

```bash
./start-all.sh
```

This will start:
- Backend API on `http://localhost:8000`
- React frontend on `http://localhost:5173`

### Alternative: Start Separately

**Backend only:**
```bash
./start-backend.sh
```

**Frontend only:**
```bash
./start-frontend.sh
```

## 🎯 Usage

1. Open `http://localhost:5173` in your browser
2. Type a description of what you want to build, for example:
   - "landing page with hero section and image gallery"
   - "signup and login screens with Firebase auth"
   - "profile page with edit functionality"
3. Click "Build" and watch your app get generated!
4. Browse the generated files in the file explorer
5. Click on any file to view its code

## 📁 Project Structure

```
Toshokan-codo-backend/
├── app.py                 # FastAPI backend server
├── test.py                # ModuleBasedAppBuilder core logic
├── modules.json           # Available code modules
├── frontend/              # React frontend
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── services/     # API service layer
│   │   ├── App.jsx       # Main app component
│   │   └── main.jsx      # Entry point
│   ├── package.json
│   └── vite.config.js
├── outputs/               # Generated apps (gitignored)
├── requirements-api.txt   # Python dependencies
└── start-all.sh          # Startup script
```

## 🧩 Available Modules

### React Components
- **react_signup_screen**: Material UI signup form with validation
- **react_login_screen**: Login form with forgot password
- **react_profile_screen**: Editable profile with avatar upload
- **react_hero_section**: Full-width hero with CTA
- **react_feature_grid**: Responsive feature showcase
- **react_image_gallery**: Masonry gallery with lightbox
- **react_image_uploader**: Drag-drop upload with preview
- **react_cta_section**: Call-to-action component

### Firebase Integration
- **firebase_email_auth**: Email/password authentication helpers
- **firebase_realtime_db**: Realtime Database CRUD operations
- **firebase_storage**: Cloud Storage file upload/download

## 🛠️ API Endpoints

### GET `/api/modules`
List all available modules

### POST `/api/build`
Build an app from a prompt

```json
{
  "prompt": "landing page with hero and gallery"
}
```

### GET `/api/file/{session_id}/{file_path}`
Get content of a generated file

### WebSocket `/ws/build`
Real-time build updates

## 🔧 Development

### Backend Development

```bash
# Activate virtual environment
source dlenv/bin/activate

# Install dependencies
pip install -r requirements-api.txt

# Run server
python3 app.py
```

### Frontend Development

```bash
cd frontend

# Install dependencies
npm install

# Run dev server
npm run dev

# Build for production
npm run build
```

## 📝 Adding Custom Modules

Edit `modules.json` and add your module:

```json
{
  "module_id": "your_module_id",
  "name": "Your Module Name",
  "description": "What it does",
  "tags": ["react", "custom"],
  "language": "tsx",
  "code": "// Your code here",
  "dependencies": ["dependency1", "dependency2"],
  "setup_required": false
}
```

## 🐛 Troubleshooting

### Backend won't start
- Check if `.env` file exists with valid `GEMINI_API_KEY`
- Ensure port 8000 is not in use: `lsof -ti:8000 | xargs kill -9`

### Frontend won't start
- Delete `node_modules` and run `npm install` again
- Ensure port 5173 is not in use: `lsof -ti:5173 | xargs kill -9`

### CORS errors
- Make sure backend is running on port 8000
- Check that CORS middleware is configured in `app.py`

## 📄 License

MIT

## 🤝 Contributing

Contributions welcome! Please feel free to submit a Pull Request.

## 🙏 Credits

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Powered by [Google Gemini](https://deepmind.google/technologies/gemini/)
- UI built with [React](https://react.dev/) and [Vite](https://vitejs.dev/)
