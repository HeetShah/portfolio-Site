#!/bin/bash
# This script is used to redeploy the Flask application using systemd. Here is what it does:
# 1. Navigate to the project directory.
# 2. Fetch the latest changes from the main branch of the GitHub repository.
# 3. Reset the local repository to match the main branch.
# 4. Install the required Python dependencies.
# 5. Restart the 'myportfolio' service to apply the changes.

PROJECT_DIR="/root/portfolio-Site"
VENV_PATH="$PROJECT_DIR/python3-virtualenv"

# Navigate to the project directory
cd "$PROJECT_DIR"

# Fetch and reset to the latest changes from GitHub
git fetch && git reset --hard origin/main

# Activate virtual environment and install dependencies
source "$VENV_PATH/bin/activate"
pip install -r requirements.txt

# Restart the 'myportfolio' service to apply new changes
sudo systemctl restart myportfolio.service
