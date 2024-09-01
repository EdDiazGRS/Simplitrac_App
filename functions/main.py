from controllers.users_controller import update_user, create_new_user, get_existing_user, delete_user, \
    delete_transactions, delete_category
from controllers.ocr_controller import process_receipt
from flask import Flask, jsonify, request
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Fix for OCR functions
os.environ['OBJC_DISABLE_INITIALIZE_FORK_SAFETY'] = 'YES'

# Initialize Flask app
app = Flask(__name__)


@app.route('/user/create', methods=['POST'])
def create_user():
    data = request.json
    return create_new_user(data)


@app.route('/user/update', methods=['PUT'])
def update_user_route():
    data = request.json
    return update_user(data)


@app.route('/user/get', methods=['GET'])
def get_user():
    user_id = request.args.get('id')
    return get_existing_user(user_id)


@app.route('/user/delete', methods=['DELETE'])
def delete_user_route():
    user_id = request.args.get('id')
    return delete_user(user_id)


@app.route('/transactions/delete', methods=['DELETE'])
def delete_transactions_route():
    user_id = request.args.get('user_id')
    return delete_transactions(user_id)


@app.route('/category/delete', methods=['DELETE'])
def delete_category_route():
    category_id = request.args.get('category_id')
    return delete_category(category_id)


@app.route('/process-receipt', methods=['POST'])
def process_receipt_route():
    image_data = request.files['image']
    return process_receipt(image_data)


# Start the Flask app
if __name__ == '__main__':
    app.run(debug=True)  # Remove debug=True in production
