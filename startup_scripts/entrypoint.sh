#!/bin/bash

# script with initial commands to start API

# Wait for the DB to be ready
echo "Waiting for the database to be ready..."
/startup_scripts/wait-for-it.sh db:5432 --timeout=60 --strict -- echo "Database is up, continuing..."

# Run migrations
echo "Running migrations..."
python /code/manage.py migrate

# generate user account fixtures
echo "Creating user accounts"
python /code/manage.py generate_user_fixtures
python /code/manage.py get_player_fixtures

# Load initial data from all apps' fixtures
echo "Loading initial data from all apps' fixtures..."
python /code/manage.py loaddata initial_data
python /code/manage.py loaddata player_data

# Start the Django development server
echo "Starting Django development server..."
python /code/manage.py runserver 0.0.0.0:8000
