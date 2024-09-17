# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Install git and curl
RUN apt-get update && apt-get install -y git curl

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
ENV PATH="${PATH}:/root/.local/bin"

# Check poetry version
RUN poetry --version

# Set the working directory in the container
WORKDIR /app

# Copy the entrypoint script into the container
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Clone the repository (replace with your repository URL)
ENV REPO_URL=https://github.com/placeTW/discord-bot.git

# Set the entrypoint
ENTRYPOINT ["/entrypoint.sh"]

# Run the script when the container launches
CMD ["python", "main.py", "prod"]