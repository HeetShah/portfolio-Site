#!/bin/bash

PROJECT_DIR="/root/portfolio-Site"
VENV_PATH="$PROJECT_DIR/python3-virtualenv"
tmux kill-server

cd "$PROJECT_DIR"
git fetch && git reset --hard origin/main

source "$VENV_PATH/bin/activate"
pip install -r requirements.txt

tmux new-session -d -s flask_session "cd $PROJECT_DIR && source $VENV_PATH/bin/activate && flask run --host=0.0.0.0"
