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

# Set Poetry to create the virtual environment inside the project directory
poetry config virtualenvs.in-project true

# Install dependencies using Poetry
poetry install --no-interaction --no-ansi

# Activate the virtual environment
source /app/.venv/bin/activate

# Run the command passed to docker run
exec "$@"
