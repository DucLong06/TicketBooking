#!/bin/bash

# Theater Booking System - Local Development Setup Script
# Sets up the development environment using uv for backend and npm for frontend

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

echo -e "${BLUE}🎭 Setting up Theater Booking System for Local Development...${NC}"

# Check requirements
print_status "Checking requirements..."

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    print_error "uv could not be found. Please install uv first."
    print_status "Install with: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    print_error "npm could not be found. Please install Node.js and npm first."
    exit 1
fi

# Check if docker compose is available
if ! command -v docker &> /dev/null; then
    print_error "docker could not be found. Please install Docker first."
    exit 1
fi

if ! command -v "docker compose" &> /dev/null; then
    print_error "docker compose could not be found. Please install docker compose."
    exit 1
fi

print_success "All requirements satisfied"

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    print_status "Creating .env file from template..."
    cp .env.example .env
    print_success ".env file created"
else
    print_warning ".env file already exists"
fi

# Setup backend with uv
print_status "Setting up backend environment with uv..."
cd backend

if [ ! -d ".venv" ]; then
    print_status "Creating Python virtual environment..."
    uv venv
    print_success "Virtual environment created"
else
    print_warning "Virtual environment already exists"
fi

print_status "Installing backend dependencies..."
uv pip install -r requirements/development.txt
uv pip install setuptools  # Fix for pkg_resources warning

print_success "Backend dependencies installed"
cd ..

# Setup frontend with npm
print_status "Setting up frontend environment with npm..."
if [ ! -d "frontend/node_modules" ]; then
    print_status "Installing frontend dependencies..."
    npm install --prefix frontend
    print_success "Frontend dependencies installed"
else
    print_warning "Frontend dependencies already installed"
fi

# Start database services
print_status "Starting database services..."
docker compose up -d db redis

# Wait for database to be ready
print_status "Waiting for database to be ready..."
max_attempts=30
attempt=1

while [ $attempt -le $max_attempts ]; do
    if docker compose exec -T db pg_isready -U theater_user -d theater_booking > /dev/null 2>&1; then
        print_success "Database is ready"
        break
    fi
    
    if [ $attempt -eq $max_attempts ]; then
        print_error "Database failed to start after $max_attempts attempts"
        exit 1
    fi
    
    print_status "Attempt $attempt/$max_attempts - waiting for database..."
    sleep 2
    ((attempt++))
done

# Run migrations
print_status "Running Django migrations..."
cd backend
./.venv/bin/python manage.py migrate
cd ..

# Create scripts directory and make scripts executable
mkdir -p scripts
chmod +x scripts/*.sh

print_success "🎉 Local development environment setup completed successfully!"
echo
echo -e "${GREEN}🚀 Quick Start Commands:${NC}"
echo -e "   ${BLUE}Backend:${NC}  ./scripts/dev-backend.sh"
echo -e "   ${BLUE}Frontend:${NC} ./scripts/dev-frontend.sh"
echo
echo -e "${GREEN}📚 Development URLs:${NC}"
echo -e "   ${BLUE}Backend API:${NC}     http://localhost:8000/api"
echo -e "   ${BLUE}Django Admin:${NC}    http://localhost:8000/admin"
echo -e "   ${BLUE}Frontend App:${NC}    http://localhost:3000"
echo
echo -e "${GREEN}🔧 Useful Commands:${NC}"
echo -e "   ${BLUE}Backend shell:${NC}   cd backend && ./.venv/bin/python manage.py shell"
echo -e "   ${BLUE}Create superuser:${NC} cd backend && ./.venv/bin/python manage.py createsuperuser"
echo -e "   ${BLUE}Run tests:${NC}       cd backend && ./.venv/bin/python manage.py test"
echo -e "   ${BLUE}Frontend lint:${NC}   npm run lint --prefix frontend"