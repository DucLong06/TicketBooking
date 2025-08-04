#!/bin/bash

# Theater Booking System - Service Testing Script
# Tests if frontend and backend services are running properly

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[TEST]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[PASS]${NC} $1"
}

print_error() {
    echo -e "${RED}[FAIL]${NC} $1"
}

echo -e "${BLUE}🧪 Testing Theater Booking System Services...${NC}"
echo

# Test backend
print_status "Testing Django backend..."
if curl -s -f http://localhost:8000/ > /dev/null; then
    print_success "Backend is responding on http://localhost:8000"
else
    print_error "Backend is not responding on http://localhost:8000"
fi

# Test Django admin
if curl -s -w "%{http_code}" http://localhost:8000/admin/ -o /dev/null | grep -q "302"; then
    print_success "Django admin is accessible at http://localhost:8000/admin"
else
    print_error "Django admin is not accessible"
fi

# Test frontend
print_status "Testing Vue frontend..."
if curl -s -f http://localhost:3000/ > /dev/null; then
    print_success "Frontend is responding on http://localhost:3000"
else
    print_error "Frontend is not responding on http://localhost:3000"
fi

# Check if Vue app structure exists
if curl -s http://localhost:3000/ | grep -q 'id="app"'; then
    print_success "Vue app div is present"
else
    print_error "Vue app div is missing"
fi

if curl -s http://localhost:3000/ | grep -q 'main.ts'; then
    print_success "Vue main.ts script is loading"
else
    print_error "Vue main.ts script is not loading"
fi

# Test database connectivity
print_status "Testing database services..."
if docker compose ps | grep -q "theater_db.*Up"; then
    print_success "PostgreSQL database is running"
else
    print_error "PostgreSQL database is not running"
fi

if docker compose ps | grep -q "theater_redis.*Up"; then
    print_success "Redis is running"
else
    print_error "Redis is not running"
fi

echo
echo -e "${GREEN}✅ Service Testing Complete!${NC}"
echo
echo -e "${BLUE}📍 Access URLs:${NC}"
echo -e "   Frontend: ${GREEN}http://localhost:3000${NC}"
echo -e "   Backend:  ${GREEN}http://localhost:8000${NC}"
echo -e "   Admin:    ${GREEN}http://localhost:8000/admin${NC}"