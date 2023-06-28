#!/bin/bash
cd /home/mrfilldev/test-server/
source venv/bin/activate
cd /home/mrfilldev/test-server/test-virtual-machine-http/production
export FLASK_RUN_HOST=127.0.0.1
export FLASK_RUN_PORT=6666
flask run
