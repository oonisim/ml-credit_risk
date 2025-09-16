#!/usr/bin/env bash
printf "\n\n"
chmod u+x ./deployment/deploy.sh
./deployment/deploy.sh

echo
echo "Create and activate a Python virtual environment and " \
     "run 'pip install -r requirements.txt' to install Python dependencies."
echo "Then run 'python -m notebook' to start the Jupyter Notebook."