#!/bin/bash

# Theater Booking System - Setup Testing Script
# This script tests the setup without starting all services

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[TEST]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[PASS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[FAIL]${NC} $1"
}

print_header() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE} 🎭 THEATER BOOKING SYSTEM TEST SUITE${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo
}

# Test results tracking
total_tests=0
passed_tests=0
failed_tests=0

run_test() {
    local test_name="$1"
    local test_command="$2"
    
    total_tests=$((total_tests + 1))
    print_status "Running: $test_name"
    
    if eval "$test_command" > /dev/null 2>&1; then
        print_success "$test_name"
        passed_tests=$((passed_tests + 1))
        return 0
    else
        print_error "$test_name"
        failed_tests=$((failed_tests + 1))
        return 1
    fi
}

print_header

# Test 1: Docker availability
print_status "Testing Docker environment..."
run_test "Docker daemon is running" "docker info"
run_test "Docker Compose is available" "docker compose version"

# Test 2: Project structure
print_status "Testing project structure..."
run_test "Backend directory exists" "[ -d backend ]"
run_test "Frontend directory exists" "[ -d frontend ]"
run_test "Docker configuration exists" "[ -f docker-compose.yml ]"
run_test "Environment template exists" "[ -f .env.example ]"

# Test 3: Backend structure
print_status "Testing backend structure..."
run_test "Django manage.py exists" "[ -f backend/manage.py ]"
run_test "Django settings exist" "[ -f backend/config/settings/base.py ]"
run_test "Requirements file exists" "[ -f backend/requirements/base.txt ]"
run_test "Backend Dockerfile exists" "[ -f backend/Dockerfile ]"

# Test 4: Frontend structure
print_status "Testing frontend structure..."
run_test "Package.json exists" "[ -f frontend/package.json ]"
run_test "Vite config exists" "[ -f frontend/vite.config.ts ]"
run_test "TailwindCSS config exists" "[ -f frontend/tailwind.config.js ]"
run_test "Frontend Dockerfile exists" "[ -f frontend/Dockerfile ]"

# Test 5: Docker Compose validation
print_status "Testing Docker Compose configuration..."
run_test "Docker Compose config is valid" "docker compose config --quiet"
run_test "All services are defined" "docker compose config --services | grep -q backend && docker compose config --services | grep -q frontend && docker compose config --services | grep -q db && docker compose config --services | grep -q redis"

# Test 6: Environment configuration
print_status "Testing environment configuration..."
if [ -f .env ]; then
    run_test ".env file exists" "true"
    run_test "Database URL in .env" "grep -q 'DATABASE_URL' .env"
    run_test "Redis URL in .env" "grep -q 'REDIS_URL' .env"
else
    print_warning ".env file not found - will be created during setup"
fi

# Test 7: Scripts and permissions
print_status "Testing scripts and permissions..."
run_test "Setup script exists" "[ -f docker/scripts/setup.sh ]"
run_test "Setup script is executable" "[ -x docker/scripts/setup.sh ]"
run_test "Test script is executable" "[ -x docker/scripts/test-setup.sh ]"

# Test 8: Documentation
print_status "Testing documentation..."
run_test "Main README exists" "[ -f README.md ]"
run_test "Documentation directory exists" "[ -d docs ]"
run_test "API documentation exists" "[ -f docs/api.md ]"
run_test "Architecture documentation exists" "[ -f docs/architecture.md ]"

# Test 9: Django app structure
print_status "Testing Django app structure..."
run_test "Venues app exists" "[ -d backend/apps/venues ]"
run_test "Events app exists" "[ -d backend/apps/events ]"
run_test "Bookings app exists" "[ -d backend/apps/bookings ]"
run_test "Payments app exists" "[ -d backend/apps/payments ]"

# Test 10: Vue app structure
print_status "Testing Vue app structure..."
run_test "Vue components directory exists" "[ -d frontend/src/components ]"
run_test "Vue views directory exists" "[ -d frontend/src/views ]"
run_test "Pinia stores directory exists" "[ -d frontend/src/stores ]"
run_test "Services directory exists" "[ -d frontend/src/services ]"

# Test 11: Network configuration
print_status "Testing network configuration..."
run_test "Nginx config exists" "[ -f docker/nginx/nginx.conf ]"
run_test "Nginx default config exists" "[ -f docker/nginx/default.conf ]"

echo
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE} TEST RESULTS SUMMARY${NC}"
echo -e "${BLUE}========================================${NC}"
echo -e "Total tests: ${total_tests}"
echo -e "${GREEN}Passed: ${passed_tests}${NC}"
echo -e "${RED}Failed: ${failed_tests}${NC}"

if [ $failed_tests -eq 0 ]; then
    echo
    print_success "🎉 All tests passed! Your theater booking system is ready for development."
    echo
    echo "Next steps:"
    echo "1. Run: cp .env.example .env"
    echo "2. Run: ./docker/scripts/setup.sh"
    echo "3. Open: http://localhost:3000"
    echo
    exit 0
else
    echo
    print_error "❌ Some tests failed. Please check the issues above before proceeding."
    echo
    exit 1
fi