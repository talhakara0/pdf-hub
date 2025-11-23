#!/bin/bash
# Activate virtual environment and run PDF Hub

# Get the directory of this script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Activate virtual environment
source "$DIR/venv/bin/activate"

# Run the application
python "$DIR/main.py"
