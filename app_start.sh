#!/bin/bash

cd /Users/danielgalvan/Python/testing_flask_file

source env/bin/activate
echo "Virtual environment activated."
export FLASK_APP=app.py
export FLASK_PORT=8448

if [ -f flask_app.pid ]; then
    echo "Stopping existing Flask app..."
    kill $(cat flask_app.pid)
    rm flask_app.pid
    echo "Existing Flask app stopped."
fi
    echo "Existing Flask app stopped."
flask run --host=0.0.0 --port=$FLASK_PORT &
pid=$! 
echo $pid > flask_app.pid
echo "Flask app started with PID $pid"
echo "Flask app is running on port $FLASK_PORT"