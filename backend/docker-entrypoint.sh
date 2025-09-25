#!/bin/bash


# Run migrations
echo "Running migrations..."
python manage.py migrate --noinput

# Collect static files (bao gồm cả frontend static files)
echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting server..."
exec  gunicorn --bind 0.0.0.0:8000 core.wsgi:application