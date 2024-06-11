#!/bin/bash
VENV_DIR="venv"
REQ_FILE="requirements.txt"

# Navigate to the client directory and install dependencies
echo "Installing dependencies for client..."
cd ./client || exit
if [ ! -d "$REQ_FILE" ]; then
  echo "Requirements file not found"
else
  pip install -r requirements.txt
fi
cd ..

# Navigate to the backend directory and install dependencies
echo "Creating python3 virtual environment for server..."
cd ./backend/functions || exit
if [ -d "$VENV_DIR" ]; then
  echo "Virtual environment already exists"
else
  echo "Creating virtual environment..."
  python3.12 -m venv venv
  source venv/bin/activate
  echo "Virtual environment created"
fi

echo "Installing dependencies for server..."
pip install -r ./backend/functions/requirements.txt
echo "Dependencies installed for both client and server."

## Create .env file from GH Secrets
#echo "Creating .env file with secrets"
#chmod 755 fetch_secrets.sh
#./fetch_secrets.sh
#echo ".env file created"

