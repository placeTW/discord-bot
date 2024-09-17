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

# Activate the virtual environment
source $(poetry env info --path)/bin/activate

# Upgrade pip to the latest version
pip install --upgrade pip


# Run the command passed to docker run
exec "$@"