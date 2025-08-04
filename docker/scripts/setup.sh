#!/bin/bash

# Theater Booking System Setup Script
# This script sets up the development environment

set -e

echo "🎭 Setting up Theater Booking System..."

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

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    print_error "Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if docker compose is available
if ! command -v docker compose &> /dev/null; then
    print_error "docker compose could not be found. Please install docker compose."
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    print_status "Creating .env file from template..."
    cp .env.example .env
    print_success ".env file created"
else
    print_warning ".env file already exists"
fi

# Create necessary directories
print_status "Creating necessary directories..."
mkdir -p logs
mkdir -p backend/staticfiles
mkdir -p backend/media
mkdir -p backend/logs

# Set permissions
chmod +x docker/scripts/*.sh

print_success "Directories created"

# Build and start services
print_status "Building Docker containers..."
docker compose build

print_status "Starting services..."
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

# Start backend services
print_status "Starting backend services..."
docker compose up -d backend celery

# Wait for backend to be ready
print_status "Waiting for backend to be ready..."
sleep 10

# Run Django migrations
print_status "Running Django migrations..."
docker compose exec -T backend python manage.py migrate

# Create superuser (optional)
read -p "Would you like to create a Django superuser? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_status "Creating Django superuser..."
    docker compose exec backend python manage.py createsuperuser
fi

# Start frontend
print_status "Installing frontend dependencies..."
docker compose run --rm frontend npm install

print_status "Starting frontend..."
docker compose up -d frontend

# Start nginx
print_status "Starting nginx..."
docker compose up -d nginx

# Health check
print_status "Performing health check..."
sleep 5

# Check services
services=("db" "redis" "backend" "frontend" "nginx")
all_healthy=true

for service in "${services[@]}"; do
    if docker compose ps | grep -q "${service}.*Up"; then
        print_success "$service is running"
    else
        print_error "$service is not running"
        all_healthy=false
    fi
done

if [ "$all_healthy" = true ]; then
    print_success "🎉 Theater Booking System setup completed successfully!"
    echo
    echo "🌐 Services are available at:"
    echo "   - Frontend: http://localhost:3000"
    echo "   - Backend API: http://localhost:8000/api"
    echo "   - Django Admin: http://localhost:8000/admin"
    echo "   - Full Application: http://localhost (via Nginx)"
    echo
    echo "📚 Useful commands:"
    echo "   - View logs: docker compose logs -f [service]"
    echo "   - Stop services: docker compose down"
    echo "   - Restart services: docker compose restart"
    echo "   - Django shell: docker compose exec backend python manage.py shell"
else
    print_error "Some services failed to start. Check logs with: docker compose logs"
    exit 1
fi