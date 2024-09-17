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

# Verify Poetry version
poetry --version

# Configure Poetry to create virtual environments inside the project directory
poetry config virtualenvs.in-project true --local

# Create/update the virtual environment and install dependencies
echo "Installing dependencies..."
poetry install --no-interaction --no-ansi

# Activate the virtual environment
echo "Activating virtual environment..."
source $(poetry env info --path)/bin/activate

# Change the permissions of virtual environment scripts
echo "Changing permissions of virtual environment scripts..."
chmod -R +x $(poetry env info --path)/bin

# Run the command passed to docker run
echo "Running command..."
exec "$@"