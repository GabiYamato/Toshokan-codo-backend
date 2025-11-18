#!/bin/bash

echo "🚀 Starting Toshokan Code Builder..."
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found"
    echo "Please create a .env file with your GEMINI_API_KEY"
    exit 1
fi

# Check if dependencies are installed
if ! python3 -c "import fastapi" 2>/dev/null; then
    echo "📦 Installing dependencies..."
    pip install -r requirements-api.txt
fi

echo "✅ Starting FastAPI server on http://localhost:8000"
echo "✅ Open frontend/index.html in your browser"
echo ""
echo "Press Ctrl+C to stop"
echo ""

python3 app.py
