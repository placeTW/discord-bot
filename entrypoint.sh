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

# Allow poetry to create a virtual environment in the project directory
export POETRY_VIRTUALENVS_IN_PROJECT=true

# Activate the virtual environment
source $(poetry env info --path)/bin/activate

# Create/update the virtual environment and install dependencies
poetry install --no-interaction --no-ansi

# Run the command passed to docker run
exec "$@"