#!/bin/bash
# This script is used to redeploy the Flask application using Docker.
# Here is what it does:
# 1. Navigate to the project directory.
# 2. Fetch the latest changes from the main branch of the GitHub repository.
# 3. Reset the local repository to match the main branch.
# 4. Take down the existing Docker containers to prevent out of memory issues.
# 5. Rebuild and start the Docker containers in detached mode.

PROJECT_DIR="/root/portfolio-Site"

# Navigate to the project directory
cd "$PROJECT_DIR"

# Fetch and reset to the latest changes from GitHub
git fetch && git reset --hard origin/main

# Take down existing Docker containers
docker compose -f docker-compose.prod.yml down

# Rebuild and start Docker containers in detached mode
docker compose -f docker-compose.prod.yml up -d --build
