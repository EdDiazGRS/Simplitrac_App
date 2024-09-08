from controllers.users_controller import update_user, create_new_user, get_existing_user, delete_user, \
    delete_transactions, delete_category
from controllers.ocr_controller import process_receipt
from flask import Flask, jsonify, request
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import logging
from flask_cors import CORS

load_dotenv()

# Fix for OCR functions
os.environ['OBJC_DISABLE_INITIALIZE_FORK_SAFETY'] = 'YES'

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)


@app.route('/test', methods=['GET'])
def test():
    print("Test endpoint hit")
    return "Test successful"


@app.route('/user/create', methods=['POST'])
def create_user():
    # data = request.json
    return create_new_user(request)


@app.route('/user/update', methods=['PUT'])
def update_user_route():
    user_id = request.args.get("user_id")
    print(f"Updating user: {user_id}")
    return update_user(request)


@app.route('/user/get', methods=['GET'])
def get_user():
    return get_existing_user(request)


@app.route('/user/delete', methods=['DELETE'])
def delete_user_route():
    return delete_user(request)


@app.route('/transactions/delete', methods=['DELETE'])
def delete_transactions_route():
    return delete_transactions(request)


@app.route('/category/delete', methods=['DELETE'])
def delete_category_route():
    return delete_category(request)


@app.route('/process_receipt', methods=['POST'])
def process_receipt_route():
    return process_receipt(request)


# Start the Flask app
if __name__ == '__main__':
    app.run(ssl_context=('fullchain.pem', 'privkey.pem'), port=5001)
