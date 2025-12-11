#!/bin/bash

# Start script for SportsMole Scraper API

echo "Starting SportsMole Scraper API..."
echo "=================================="

# Check if dependencies are installed
if ! python3 -c "import flask" 2>/dev/null; then
    echo "Dependencies not found. Installing..."
    pip install -r requirements.txt
fi

# Start the API
python3 api.py
