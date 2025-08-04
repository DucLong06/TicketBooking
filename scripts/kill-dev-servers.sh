#!/bin/bash

# Theater Booking System - Kill Development Servers
# Stops all running development servers and services

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🛑 Stopping Theater Booking Development Servers...${NC}"

# Kill Django runserver processes
echo -e "${BLUE}Stopping Django backend...${NC}"
pkill -f "manage.py runserver" 2>/dev/null || echo "No Django processes found"

# Kill Vite/Node processes
echo -e "${BLUE}Stopping Vue frontend...${NC}"
pkill -f "vite" 2>/dev/null || echo "No Vite processes found"
pkill -f "node.*vite" 2>/dev/null || echo "No Node/Vite processes found"

# Stop Docker services
echo -e "${BLUE}Stopping database services...${NC}"
docker compose down 2>/dev/null || echo "Docker services already stopped"

# Clean up any remaining processes on ports 3000 and 8000
echo -e "${BLUE}Cleaning up ports...${NC}"
lsof -ti:3000 | xargs kill -9 2>/dev/null || echo "Port 3000 already free"
lsof -ti:8000 | xargs kill -9 2>/dev/null || echo "Port 8000 already free"

echo -e "${GREEN}✅ All development servers stopped!${NC}"
echo -e "${GREEN}📱 Ports 3000 and 8000 are now available${NC}"