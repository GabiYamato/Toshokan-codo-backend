#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Starting Toshokan Code Builder${NC}\n"

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${RED}❌ Error: .env file not found${NC}"
    echo "Please create a .env file with your GEMINI_API_KEY"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "dlenv" ]; then
    echo -e "${YELLOW}⚠️  Virtual environment not found. Creating one...${NC}"
    python3 -m venv dlenv
fi

# Activate virtual environment
echo -e "${GREEN}📦 Activating virtual environment...${NC}"
source dlenv/bin/activate

# Install Python dependencies
echo -e "${GREEN}📥 Installing Python dependencies...${NC}"
pip install -q -r requirements-api.txt

# Check if node_modules exists in frontend
if [ ! -d "frontend/node_modules" ]; then
    echo -e "${GREEN}📥 Installing frontend dependencies...${NC}"
    cd frontend && npm install && cd ..
fi

# Function to cleanup on exit
cleanup() {
    echo -e "\n${YELLOW}🛑 Shutting down servers...${NC}"
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

trap cleanup EXIT INT TERM

# Start backend server
echo -e "${GREEN}🔧 Starting backend server on port 8000...${NC}"
python3 app.py &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

# Start frontend server
echo -e "${GREEN}⚛️  Starting React frontend on port 5173...${NC}"
cd frontend && npm run dev &
FRONTEND_PID=$!

echo -e "\n${GREEN}✅ All servers started!${NC}"
echo -e "${YELLOW}📝 Backend API: ${NC}http://localhost:8000"
echo -e "${YELLOW}🌐 Frontend: ${NC}http://localhost:5173"
echo -e "\n${YELLOW}Press Ctrl+C to stop all servers${NC}\n"

# Wait for processes
wait
