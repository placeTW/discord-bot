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

# Configure Poetry to create the virtual environment in the project directory
poetry config virtualenvs.in-project true

# Create/update the virtual environment and install dependencies
poetry install --no-interaction --no-ansi

# Make the virtual environment executable
chmod +x $(poetry env info --path)/bin/activate

# Activate the virtual environment
source $(poetry env info --path)/bin/activate

# Run the command passed to docker run
exec "$@"