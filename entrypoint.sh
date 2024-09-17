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

# Verify Python version
python --version

# Create/update the virtual environment and install dependencies
poetry install --no-interaction --no-ansi

# Run the command passed to docker run
exec "$@"