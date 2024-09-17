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
export POETRY_VIRTUALENVS_OPTIONS_ALWAYS_COPY=true

# Set the permissions of the virtual environment directory
chmod -R 777 $(poetry env info --path)

# Create/update the virtual environment and install dependencies
poetry install --no-interaction --no-ansi

# Activate the virtual environment
source $(poetry env info --path)/bin/activate

# Run the command passed to docker run
exec "$@"