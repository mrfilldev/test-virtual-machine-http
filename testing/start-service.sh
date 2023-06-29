#!/bin/bash
cd /home/mrfilldev/test-server/
source venv/bin/activate
cd /home/mrfilldev/test-server/test-virtual-machine-http/new_project
export FLASK_RUN_HOST=127.0.0.1

# DEV = 9999
#export FLASK_RUN_PORT=9999

# PROD = 6666
export FLASK_RUN_PORT=6666

#export FLASK_RUN_PORT=8080

flask run

