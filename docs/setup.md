# Environment Setup Guide

This comprehensive guide covers setting up the theater ticket booking system development environment on different platforms.

## Prerequisites

### Required Software
- **Docker Desktop** (v20.10+) - [Download](https://www.docker.com/products/docker-desktop)
- **Docker Compose** (v2.0+) - Usually included with Docker Desktop
- **Git** (v2.20+) - [Download](https://git-scm.com/downloads)
- **Node.js** (v18+) - Optional, for local frontend development
- **Python** (v3.11+) - Optional, for local backend development

### System Requirements
- **RAM**: 8GB minimum, 16GB recommended
- **Storage**: 10GB free space for Docker images and volumes
- **OS**: Windows 10/11, macOS 10.15+, or Linux (Ubuntu 20.04+)

## Quick Setup (Recommended)

### 1. Clone Repository
```bash
git clone <repository-url>
cd TicketBooking
```

### 2. Automated Setup
```bash
# Make setup script executable
chmod +x docker/scripts/setup.sh

# Run the automated setup
./docker/scripts/setup.sh
```

The setup script will:
- Check system requirements
- Create environment files
- Build Docker containers
- Start all services
- Run database migrations
- Optionally create a superuser
- Perform health checks

### 3. Verify Installation
```bash
# Check all services are running
docker-compose ps

# Test API endpoint
curl http://localhost:8000/health/

# Access applications
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000/api
# Admin: http://localhost:8000/admin
```

## Manual Setup

If you prefer manual setup or need to troubleshoot:

### 1. Environment Configuration

Create environment file:
```bash
cp .env.example .env
```

Edit `.env` with your settings:
```bash
# Database Configuration
DB_NAME=theater_booking
DB_USER=theater_user
DB_PASSWORD=theater_pass_123
DB_HOST=db
DB_PORT=5432

# Redis Configuration
REDIS_URL=redis://redis:6379/0

# Django Configuration
SECRET_KEY=your-super-secret-key-here-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# CORS Configuration
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Frontend Configuration
VITE_API_URL=http://localhost:8000/api
VITE_WS_URL=ws://localhost:8000/ws

# Payment Gateway (VNPAY)
VNPAY_TMN_CODE=your-vnpay-merchant-code
VNPAY_SECRET_KEY=your-vnpay-secret-key
VNPAY_RETURN_URL=http://localhost:3000/payment/return
VNPAY_SANDBOX=True

# Email Configuration (for production)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-email-password

# File Upload
MAX_UPLOAD_SIZE=10485760  # 10MB
ALLOWED_IMAGE_TYPES=jpeg,jpg,png,webp

# Security (production only)
SECURE_SSL_REDIRECT=False
SECURE_HSTS_SECONDS=0
SECURE_CONTENT_TYPE_NOSNIFF=True
SECURE_BROWSER_XSS_FILTER=True

# Logging
LOG_LEVEL=INFO
LOG_FILE_MAX_SIZE=10485760  # 10MB
LOG_BACKUP_COUNT=5
```

### 2. Create Required Directories
```bash
mkdir -p logs
mkdir -p backend/staticfiles
mkdir -p backend/media
mkdir -p backend/logs
```

### 3. Build and Start Services

#### Start Infrastructure Services
```bash
# Start database and Redis
docker-compose up -d db redis

# Wait for services to be healthy
docker-compose ps
```

#### Build and Start Backend
```bash
# Build backend container
docker-compose build backend

# Start backend service
docker-compose up -d backend

# Check backend logs
docker-compose logs -f backend
```

#### Setup Database
```bash
# Run database migrations
docker-compose exec backend python manage.py migrate

# Create superuser (interactive)
docker-compose exec backend python manage.py createsuperuser

# Load sample data (if available)
docker-compose exec backend python manage.py loaddata fixtures/sample_data.json
```

#### Start Background Services
```bash
# Start Celery worker
docker-compose up -d celery

# Start Celery beat (for scheduled tasks)
docker-compose up -d celery-beat  # if configured
```

#### Build and Start Frontend
```bash
# Build frontend container
docker-compose build frontend

# Install dependencies
docker-compose run --rm frontend npm install

# Start frontend development server
docker-compose up -d frontend
```

#### Start Web Server
```bash
# Start Nginx reverse proxy
docker-compose up -d nginx
```

## Platform-Specific Instructions

### Windows Setup

#### Using WSL2 (Recommended)
```powershell
# Install WSL2 if not already installed
wsl --install

# Update WSL2
wsl --update

# Set WSL2 as default
wsl --set-default-version 2

# Clone repository in WSL2
wsl
cd /home/yourusername
git clone <repository-url>
cd TicketBooking
```

#### Native Windows
```powershell
# Use PowerShell as Administrator
# Ensure Docker Desktop is running
docker --version
docker-compose --version

# Clone repository
git clone <repository-url>
cd TicketBooking

# Run setup script
./docker/scripts/setup.sh
```

### macOS Setup

#### Using Homebrew
```bash
# Install Docker Desktop via Homebrew
brew install --cask docker

# Start Docker Desktop
open /Applications/Docker.app

# Clone and setup
git clone <repository-url>
cd TicketBooking
chmod +x docker/scripts/setup.sh
./docker/scripts/setup.sh
```

#### Manual Installation
1. Download Docker Desktop from the official website
2. Install and start Docker Desktop
3. Follow the quick setup instructions above

### Linux Setup

#### Ubuntu/Debian
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Clone and setup
git clone <repository-url>
cd TicketBooking
./docker/scripts/setup.sh
```

#### CentOS/RHEL/Fedora
```bash
# Install Docker
sudo yum install -y docker
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Follow Ubuntu instructions for setup
```

## Local Development (Without Docker)

For developers who prefer local development without Docker:

### Backend Setup

#### Prerequisites
```bash
# Install Python 3.11+
python --version

# Install PostgreSQL
# macOS: brew install postgresql
# Ubuntu: sudo apt-get install postgresql postgresql-contrib
# Windows: Download from https://www.postgresql.org/

# Install Redis
# macOS: brew install redis
# Ubuntu: sudo apt-get install redis-server
# Windows: Download from https://redis.io/
```

#### Setup Steps
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements/development.txt

# Create PostgreSQL database
createdb theater_booking

# Set environment variables
export DJANGO_SETTINGS_MODULE=config.settings.development
export DATABASE_URL=postgresql://username:password@localhost/theater_booking
export REDIS_URL=redis://localhost:6379/0

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver 0.0.0.0:8000
```

### Frontend Setup

#### Prerequisites
```bash
# Install Node.js 18+
node --version
npm --version
```

#### Setup Steps
```bash
cd frontend

# Install dependencies
npm install

# Set environment variables
cp .env.example .env.local
# Edit .env.local with your API URLs

# Start development server
npm run dev
```

## IDE Configuration

### Visual Studio Code

#### Recommended Extensions
```json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.pylint",
    "ms-python.black-formatter",
    "vue.volar",
    "bradlc.vscode-tailwindcss",
    "ms-vscode.vscode-typescript-next",
    "ms-vscode-remote.remote-containers",
    "ms-azuretools.vscode-docker"
  ]
}
```

#### Settings
```json
{
  "python.defaultInterpreterPath": "./backend/venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.formatting.provider": "black",
  "typescript.preferences.includePackageJsonAutoImports": "on",
  "vue.codeActions.enabled": true,
  "tailwindCSS.includeLanguages": {
    "vue": "html"
  }
}
```

### PyCharm

#### Configuration
1. Open backend directory as Python project
2. Set interpreter to virtual environment
3. Configure database connection
4. Enable Django support
5. Set Django settings module

### WebStorm

#### Configuration
1. Open frontend directory as project
2. Enable Vue.js plugin
3. Configure TypeScript service
4. Set up ESLint and Prettier
5. Configure Tailwind CSS

## Development Services

### Database Management

#### pgAdmin (Web-based PostgreSQL client)
```yaml
# Add to docker-compose.yml
pgadmin:
  image: dpage/pgadmin4:latest
  environment:
    PGADMIN_DEFAULT_EMAIL: admin@example.com
    PGADMIN_DEFAULT_PASSWORD: admin
  ports:
    - "5050:80"
  depends_on:
    - db
```

Access at: http://localhost:5050

#### Redis Commander (Web-based Redis client)
```yaml
# Add to docker-compose.yml
redis-commander:
  image: rediscommander/redis-commander:latest
  environment:
    REDIS_HOSTS: "local:redis:6379"
  ports:
    - "8081:8081"
  depends_on:
    - redis
```

Access at: http://localhost:8081

### Monitoring Tools

#### Celery Flower (Task monitoring)
```yaml
# Add to docker-compose.yml
flower:
  build:
    context: ./backend
    dockerfile: Dockerfile
  command: celery -A config flower --port=5555
  ports:
    - "5555:5555"
  environment:
    - DATABASE_URL=postgresql://theater_user:theater_pass@db:5432/theater_booking
    - REDIS_URL=redis://redis:6379/0
  depends_on:
    - redis
    - celery
```

Access at: http://localhost:5555

## Troubleshooting

### Common Issues

#### Docker Issues
```bash
# Docker daemon not running
sudo systemctl start docker  # Linux
# Start Docker Desktop on Windows/macOS

# Port already in use
docker-compose down
lsof -i :3000  # Find process using port
kill -9 <PID>  # Kill process

# Container won't start
docker-compose logs <service-name>
docker-compose restart <service-name>

# Volume permission issues (Linux)
sudo chown -R $USER:$USER .
```

#### Database Issues
```bash
# Can't connect to database
docker-compose logs db
docker-compose exec db pg_isready -U theater_user

# Migration issues
docker-compose exec backend python manage.py migrate --fake-initial
docker-compose exec backend python manage.py migrate --run-syncdb

# Reset database
docker-compose down -v
docker-compose up -d db
docker-compose exec backend python manage.py migrate
```

#### Frontend Issues
```bash
# Module not found errors
docker-compose run --rm frontend npm install
docker-compose restart frontend

# Build failures
docker-compose run --rm frontend npm run build
docker-compose logs frontend

# TypeScript errors
docker-compose run --rm frontend npx tsc --noEmit
```

#### Network Issues
```bash
# Services can't communicate
docker network ls
docker network inspect ticketbooking_default

# DNS resolution issues
docker-compose exec backend nslookup db
docker-compose exec frontend nslookup backend
```

### Performance Issues

#### Slow Container Startup
```bash
# Check system resources
docker system df
docker system prune  # Clean up unused resources

# Optimize Dockerfiles
# Use multi-stage builds
# Minimize layer count
# Use .dockerignore files
```

#### Database Performance
```bash
# Check database connections
docker-compose exec db psql -U theater_user -d theater_booking -c "SELECT * FROM pg_stat_activity;"

# Monitor query performance
docker-compose exec db psql -U theater_user -d theater_booking -c "SELECT query, mean_time, calls FROM pg_stat_statements ORDER BY mean_time DESC LIMIT 10;"
```

## Production Considerations

### Environment Variables
```bash
# Production environment
DEBUG=False
SECRET_KEY=<strong-random-key>
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:pass@prod-db:5432/theater_booking
REDIS_URL=redis://prod-redis:6379/0
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
```

### Security Checklist
- [ ] Change default passwords
- [ ] Use strong SECRET_KEY
- [ ] Enable SSL/TLS
- [ ] Configure proper CORS settings
- [ ] Set up firewall rules
- [ ] Enable security headers
- [ ] Regular security updates

### Monitoring Setup
- [ ] Application monitoring (APM)
- [ ] Error tracking (Sentry)
- [ ] Log aggregation (ELK/Fluentd)
- [ ] Database monitoring
- [ ] Server monitoring
- [ ] Uptime monitoring

## Next Steps

After successful setup:

1. **Explore the Application**
   - Register a user account
   - Access admin panel with superuser
   - Test API endpoints
   - Review code structure

2. **Development Workflow**
   - Read [Development Workflow](development.md)
   - Set up your IDE
   - Run tests
   - Make your first contribution

3. **Learn the Architecture**
   - Review [Architecture Documentation](architecture.md)
   - Understand data models
   - Study API design
   - Learn about real-time features

4. **Testing**
   - Run backend tests
   - Run frontend tests
   - Write new tests
   - Set up CI/CD pipeline