#!/bin/bash
# set up local server
source env/bin/activate

export FLASK_ENV="production"
export FLASK_APP="application.py"

flask run