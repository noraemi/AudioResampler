#!/bin/bash
# set up local server

export FLASK_ENV="production"
export FLASK_APP="application.py"

flask run