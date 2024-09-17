# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Install git and curl
RUN apt-get update && apt-get install -y git curl

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
ENV PATH="${PATH}:/root/.local/bin"

# Set the working directory in the container
WORKDIR /app

# Copy the entrypoint script into the container
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Set default environment variables
ENV REPO_URL=https://github.com/yourusername/your-repo.git

# Set the entrypoint
ENTRYPOINT ["/entrypoint.sh"]

# Set the default command
CMD ["poetry", "run", "python", "your_script.py"]