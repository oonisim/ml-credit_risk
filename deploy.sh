#!/usr/bin/env bash
printf "\n\n"
chmod u+x ./deployment/deploy.sh
./deployment/infra/sh/deploy.sh

chmod u+x ./deployment/feast/feature_repository/deploy.sh
./deployment/feast/feature_repository/deploy.sh

echo
echo "Create and activate a Python virtual environment and " \
     "run 'pip install -r requirements.txt' to install Python dependencies."
echo "Then run 'python -m notebook' to start the Jupyter Notebook."