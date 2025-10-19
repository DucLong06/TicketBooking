#!/bin/bash

case "$1" in
  start-db)
    echo "🗄️  Starting Database & Redis..."
    docker compose -f docker-compose.db.yml up -d
    echo "✅ Database started!"
    ;;
    
  stop-db)
    echo "⏸️  Stopping Database & Redis..."
    docker compose -f docker-compose.db.yml down
    echo "✅ Database stopped!"
    ;;

  create-network)
    echo "Create network"
    docker network create booking_network_prod
   
    ;;
  

  build-frontend)
    echo "🔨 Building Frontend..."
    docker compose -f docker-compose.prod.yml build frontend_builder
    docker compose -f docker-compose.prod.yml up frontend_builder
    echo "✅ Frontend built!"
    ;;

  start-app)
    echo "🚀 Starting Application..."
    echo "Building frontend..."
    docker compose -f docker-compose.prod.yml up frontend_builder
    # Start backend
    echo "Starting backend..."
    docker compose -f docker-compose.prod.yml up -d backend celery_worker celery_beat
    echo "✅ Application started!"
    echo "Access: http://localhost:8000"
    ;;
    
  stop-app)
    echo "⏸️  Stopping Application..."
    docker compose -f docker-compose.prod.yml down
    echo "✅ Application stopped!"
    ;;
    
  restart-app)
    echo "🔄 Restarting Application..."
    docker compose -f docker-compose.prod.yml down
    docker compose -f docker-compose.prod.yml up frontend_builder
    docker compose -f docker-compose.prod.yml up -d backend celery_worker celery_beat
    echo "✅ Application restarted!"
    ;;

  restart-backend)
    echo "🔄 Restarting Backend only..."
    docker compose -f docker-compose.prod.yml restart backend celery_worker celery_beat
    echo "✅ Backend restarted!"
    ;;

  rebuild-all)
    echo "🔨 Rebuilding everything..."
    docker compose -f docker-compose.prod.yml down
    docker compose -f docker-compose.prod.yml build --no-cache
    docker compose -f docker-compose.prod.yml up frontend_builder
    docker compose -f docker-compose.prod.yml up -d backend celery_worker celery_beat
    echo "✅ Rebuild completed!"
    ;;
    
  logs-app)
    docker compose -f docker-compose.prod.yml logs -f backend celery_worker celery_beat
    ;;

  logs-backend)
    docker compose -f docker-compose.prod.yml logs -f backend
    ;;
    
  logs-db)
    docker compose -f docker-compose.db.yml logs -f
    ;;
    
  backup-db)
    echo "💾 Backing up database..."
    mkdir -p ./backups
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    docker exec booking_db_prod pg_dump -U booking_user booking_db_prod > ./backups/backup_${TIMESTAMP}.sql
    echo "✅ Backup saved: ./backups/backup_${TIMESTAMP}.sql"
    ;;
    
  restore-db)
    if [ -z "$2" ]; then
      echo "❌ Please provide backup file: ./manage-prod.sh restore-db backups/backup_file.sql"
      exit 1
    fi
    echo "📥 Restoring database from $2..."
    docker exec -i booking_db_prod psql -U booking_user booking_db_prod < $2
    echo "✅ Database restored!"
    ;;
    
  migrate)
    echo "🗄️  Running migrations..."
    docker compose -f docker-compose.prod.yml exec backend python manage.py migrate
    echo "✅ Migrations completed!"
    ;;
    
  collectstatic)
    echo "📁 Collecting static files..."
    docker compose -f docker-compose.prod.yml exec backend python manage.py collectstatic --noinput
    echo "✅ Static files collected!"
    ;;
    
  shell)
    docker compose -f docker-compose.prod.yml exec backend python manage.py shell
    ;;
    
  bash)
    docker compose -f docker-compose.prod.yml exec backend bash
    ;;
    
  status)
    echo "📊 Database Status:"
    docker compose -f docker-compose.db.yml ps
    echo ""
    echo "📊 Application Status:"
    docker compose -f docker-compose.prod.yml ps
    ;;
    
  *)
    echo "Usage: ./manage-prod.sh {command}"
    echo ""
    echo "Database Commands:"
    echo "  start-db         - Start database and Redis"
    echo "  stop-db          - Stop database and Redis"
    echo "  logs-db          - View database logs"
    echo "  backup-db        - Backup database"
    echo "  restore-db       - Restore database from backup"
    echo ""
    echo "Application Commands:"
    echo "  build-frontend   - Build frontend only"
    echo "  start-app        - Build frontend & start backend"
    echo "  stop-app         - Stop application"
    echo "  restart-app      - Restart application"
    echo "  restart-backend  - Restart backend only"
    echo "  rebuild-all      - Rebuild everything from scratch"
    echo "  logs-app         - View all application logs"
    echo "  logs-backend     - View backend logs"
    echo "  migrate          - Run database migrations"
    echo "  collectstatic    - Collect static files"
    echo "  shell            - Django shell"
    echo "  bash             - Backend bash shell"
    echo ""
    echo "Other:"
    echo "  status           - Show status of all services"
    exit 1
    ;;
esac