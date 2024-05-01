#!/bin/sh


echo "Waiting for postgres..."


while ! nc -z backend-db 5432; do
    sleep 0.1
done


echo "PostgreSQL started"

# Start the final_model.py in the background
echo "Starting final_model.py..."
nohup python3 final_model.py > final_model.log 2>&1 &

# Start the Flask application
echo "Starting Flask app..."

python3 manage.py run -h 0.0.0.0

exec "$@"
