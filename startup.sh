#!/bin/bash

export FLASK_APP=app.py
export FLASK_ENV=production

# Run Gunicorn on Azure-assigned port with 4 workers
gunicorn --bind 0.0.0.0:$PORT app:app --workers 4 --timeout 120
