#!/bin/bash

echo "================================"
echo "JanSahayak - Starting Web Server"
echo "================================"
echo

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Virtual environment not found!"
    echo "Please run setup first."
    exit 1
fi

# Activate virtual environment
source .venv/bin/activate

# Start Flask app
echo "Starting Flask application..."
echo
python app.py
