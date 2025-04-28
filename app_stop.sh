#!/bin/bash


cd /Users/danielgalvan/Python/testing_flask_file
source env/bin/activate

if test -f "flask_app.pid"; then
    pid=$(cat flask_app.pid)
    echo "Stopping Flask app with PID $pid"
    kill $pid
    rm flask_app.pid
    echo "Flask app stopped."

else
    echo "No PID file found. Flask app may not be running."
fi