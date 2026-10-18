#!/bin/bash

# Activate the virtual environment
if [ -d "Data/TranslateVenv" ]; then
    echo "Activating TranslateVenv..."
    source Data/TranslateVenv/bin/activate
else
    echo "Virtual environment TranslateVenv not found. Please run start.sh first."
    exit 1
fi

cd Data

python3 interface.py

echo "Running interface.py..."