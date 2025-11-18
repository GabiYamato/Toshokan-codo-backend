#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}🔧 Starting Backend Server${NC}\n"

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

# Install dependencies
echo -e "${GREEN}📥 Installing dependencies...${NC}"
pip install -q -r requirements-api.txt

# Start server
echo -e "${GREEN}🚀 Starting FastAPI server on port 8000...${NC}"
python3 app.py
