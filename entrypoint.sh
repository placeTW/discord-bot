#!/bin/bash
set -e

# Clone the repository if it doesn't exist
if [ ! -d "/app/.git" ]; then
    echo "Cloning repository..."
    git clone ${REPO_URL} .
    echo "Repository cloned successfully."
else
    echo "Repository already exists. Pulling latest changes..."
    git pull
fi

# Create a virtual environment with venv in the app directory
python3 -m venv /app/.venv

# Activate the virtual environment
poetry shell

# Install dependencies using Poetry
poetry install --no-interaction --no-ansi

# Run the command passed to docker run
exec "$@"