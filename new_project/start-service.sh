#!/bin/bash
cd /test-server
source venv/bin/activate
cd /test-server/test-virtual-machine-http/new_project
export FLASK_RUN_HOST=127.0.0.1
export FLASK_RUN_PORT=8080
flask run

