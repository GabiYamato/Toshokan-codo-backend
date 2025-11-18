#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}⚛️  Starting Frontend Server${NC}\n"

cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}📥 Installing dependencies...${NC}"
    npm install
fi

# Start dev server
echo -e "${GREEN}🚀 Starting Vite dev server on port 5173...${NC}"
npm run dev
