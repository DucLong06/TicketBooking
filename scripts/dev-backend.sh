#!/bin/bash

# Theater Booking System - Backend Development Script
# Start the Django development server with uv

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🎭 Starting Theater Booking Backend Development Server...${NC}"

# Check if we're in the right directory
if [ ! -f "backend/manage.py" ]; then
    echo "Error: Please run this script from the project root directory"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "backend/.venv" ]; then
    echo "Virtual environment not found. Creating..."
    cd backend
    uv venv
    uv pip install -r requirements/development.txt
    uv pip install setuptools
    cd ..
fi

# Check if databases are running
if ! docker compose ps | grep -q "theater_db.*Up"; then
    echo -e "${BLUE}Starting database services...${NC}"
    docker compose up -d db redis
    
    # Wait for database to be ready
    echo "Waiting for database to be ready..."
    sleep 5
fi

# Run migrations
echo -e "${BLUE}Running migrations...${NC}"
cd backend
./.venv/bin/python manage.py migrate

echo -e "${GREEN}✅ Backend server starting at http://localhost:8000${NC}"
echo -e "${GREEN}✅ Admin panel available at http://localhost:8000/admin${NC}"
echo -e "${GREEN}✅ API endpoints at http://localhost:8000/api${NC}"
echo ""

# Start the development server
./.venv/bin/python manage.py runserver 8000