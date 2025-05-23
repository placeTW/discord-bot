# Use an official Python runtime as a parent image
FROM python:3.13-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
ENV PATH="${PATH}:/root/.local/bin"

# Set the working directory in the container
WORKDIR /app

# Copy the entrypoint script into the container
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Clone the repository (replace with your repository URL)
ENV REPO_URL=https://github.com/placeTW/discord-bot.git

# Set an environment variable for the mode (default to 'dev')
ENV APP_MODE=dev

# Set the entrypoint
ENTRYPOINT ["/entrypoint.sh"]

# Run the script when the container launches
CMD ["/bin/bash", "-c", "python main.py $APP_MODE"]