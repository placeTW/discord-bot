# Use an official Python runtime as a parent image
FROM python:3.11-alpine

# Install system dependencies
RUN apk update && apk add --no-cache \
    git \
    curl \
    bash

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
CMD ["/bin/bash", "-c", "python main.py"]
