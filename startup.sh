#!/bin/bash
echo "Preparing persistent data folder..."
# Create persistent folder
mkdir -p /home/data

# Copy required files from wwwroot to persistent folder
cp /home/site/wwwroot/app.py /home/data/
cp /home/site/wwwroot/approval_model.pkl /home/data/
cp /home/site/wwwroot/label_map.pkl /home/data/
cp /home/site/wwwroot/prepare_data.py /home/data/
cp /home/site/wwwroot/request_types_approvals.xlsx /home/data/
cp /home/site/wwwroot/request_types_approvals_clean.csv /home/data/
cp /home/site/wwwroot/train_model.py /home/data/

echo "Starting Flask app..."
# Start Flask from the persistent folder
cd /home/data
gunicorn --bind 0.0.0.0 --timeout 600 app:app
