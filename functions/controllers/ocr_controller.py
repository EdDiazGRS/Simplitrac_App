import base64
import os

from models.transaction import Transaction

os.environ['OBJC_DISABLE_INITIALIZE_FORK_SAFETY'] = 'YES'
import io
import json
import logging
from firebase_functions import https_fn
from services.ocr_service import extract_receipt_data, extract_text
import tempfile
from functools import wraps

# Configure logging
logging.basicConfig(level=logging.INFO)


def cors_enabled_function(func):
    """Decorator for enabling Cross-Origin Resource Sharing (CORS) on Firebase HTTP functions.

    This decorator adds the necessary CORS headers to allow cross-origin requests
    to your Firebase function endpoints. It handles both the preflight OPTIONS
    request and modifies the response headers of the decorated function to ensure
    proper CORS support.

    Args:
        func: The Firebase HTTP function to be wrapped.
    """
    @wraps(func)
    def wrapper(req, *args, **kwargs):
        if req.method == 'OPTIONS':
            headers = {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'PUT, POST, GET, DELETE, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type, Authorization'
            }
            print("Inside cors function")
            return https_fn.Response('', 204, headers)

        # Call the original function
        response = func(req, *args, **kwargs)

        # Ensure the response has the CORS headers
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    return wrapper


@cors_enabled_function
@https_fn.on_request()
def process_receipt(req: https_fn.Request) -> https_fn.Response:
    try:

        # data = req.data
        #
        # # Decode the bytes object to string
        # base64_string = data.decode('utf-8')
        #
        # if base64_string.startswith("data:image/png;base64,"):
        #     base64_string = base64_string[len("data:image/png;base64,"):]
        #
        # # Decode the base64 string
        # image_data = base64.b64decode(base64_string)
        # print(image_data)
        #
        # # base64_string = data.get("imageData")
        # # image = base64.b64decode(base64_string)
        # # image_data = image
        # # print(image_data)
        if 'file' not in req.files:
            logging.warning("No file found in request")
            return https_fn.Response(json.dumps({"error": "Image file is required"}), status=400, content_type='application/json')

        file = req.files['file']
        if file.filename == '':
            logging.warning("Empty filename received")
            return https_fn.Response(json.dumps({"error": "No selected file"}), status=400, content_type='application/json')

        logging.info(f"Received file: {file.filename}")

        # Read the file content
        image_data = file.read()

        # # Save the image data to a temporary file
        # with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
        #     temp_file.write(image_data)
        #     temp_filename = temp_file.name

        try:
            # Extract text using OCR service
            logging.info("Extracting text from image...")
            extracted_text = extract_text(image_data)
            if not extracted_text:
                return https_fn.Response(json.dumps({"error": "No text detected in the image"}), status=400, content_type='application/json')
            
            logging.info("Parsing extracted text...")
            parsed_data = extract_receipt_data(extracted_text)
            logging.info(f"Parsed data: {parsed_data}")
            
            # Prepare the response data
            transaction = Transaction(parsed_data)
            
            return https_fn.Response(json.dumps(transaction.serialize()), status=200, content_type='application/json')
        finally:
            # Clean up the temporary file
            logging.info("Processing image complete")
    except Exception as e:
        logging.error(f"Error in process_receipt: {str(e)}", exc_info=True)
        return https_fn.Response(json.dumps({"error": str(e)}), status=500, content_type='application/json')