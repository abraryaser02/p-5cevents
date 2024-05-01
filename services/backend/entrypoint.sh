#!/bin/sh

# Create directory if it doesn't exist
mkdir -p /usr/src/app

# Redirect stdout and stderr to a log file
exec > /usr/src/app/entrypoint.log 2>&1

echo "Waiting for Postgres to start..."
while ! nc -z backend-db 5432; do
    sleep 0.5
done
echo "Postgres started."

echo "Recreating Database..."
python manage.py recreate_db

echo "Starting final_model.py in the background..."
nohup python final_model.py > /dev/null 2>&1 &

echo "Starting Flask app..."
export FLASK_RUN_PORT=5001  # Set Flask app to run on port 5001
exec python manage.py run -h 0.0.0.0 -p 5001
