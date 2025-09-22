#!/bin/bash

# Theater Booking System - Frontend Development Script
# Start the Vue 3 development server with npm

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🎭 Starting Theater Booking Frontend Development Server...${NC}"

# Check if we're in the right directory
if [ ! -f "frontend/package.json" ]; then
    echo "Error: Please run this script from the project root directory"
    exit 1
fi

# Check if node_modules exists
if [ ! -d "frontend/node_modules" ]; then
    echo -e "${BLUE}Installing frontend dependencies...${NC}"
    npm install --prefix frontend
fi

echo -e "${GREEN}✅ Frontend server starting at http://localhost:3000${NC}"
echo ""

# Start the development server
cd frontend
npm run dev