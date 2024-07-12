#!/bin/bash
# This script is used to redeploy the Flask application. Here is what it does:
# 1. Fetches the latest changes from the main branch of the repository.
# 2. Resets the local repository to match the main branch.
# 3. Installs the required dependencies.
# 4. Starts the Flask application in a tmux session.

PROJECT_DIR="/root/portfolio-Site"
VENV_PATH="$PROJECT_DIR/python3-virtualenv"
tmux kill-server

cd "$PROJECT_DIR"
git fetch && git reset --hard origin/main

source "$VENV_PATH/bin/activate"
pip install -r requirements.txt

tmux new-session -d -s flask_session "cd $PROJECT_DIR && source $VENV_PATH/bin/activate && flask run --host=0.0.0.0"
