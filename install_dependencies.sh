#!/bin/bash
VENV_DIR="venv"
REQ_FILE="requirements.txt"

# Navigate to the client directory and install dependencies
echo "Installing dependencies for client..."
if [ -d "./client" ]; then
  echo "REMOVING CLIENT DIRECTORY"
  rm -r "client"
  echo "CLIENT DIRECTORY REMOVED"
fi

cd ./frontend || exit
echo "Current working directory":
pwd

if [ ! "package.json" ]; then
  echo "NO JSON FILE FOUND"
else
  npm install
fi
cd ..

echo "Current working directory"
pwd


# Navigate to the backend directory and install dependencies
echo "Creating python3 virtual environment for server..."
cd ./backend/functions || exit
echo "Current working directory"
pwd

if [ -d "$VENV_DIR" ]; then
  echo "Virtual environment already exists"
else
  echo "Creating virtual environment..."
  python3.12 -m venv venv
c  echo "Virtual environment created"
fi

echo "Installing dependencies for server..."
if [ ! "$REQ_FILE" ]; then
  echo "Requirements file not found"
  echo "$REQ_FILE"
else
  pip install -r requirements.txt
fi
#cd ../..
#echo "Dependencies installed for both client and server."

## Create .env file from GH Secrets
#echo "Creating .env file with secrets"
#chmod 755 fetch_secrets.sh
#./fetch_secrets.sh
#echo ".env file created"

