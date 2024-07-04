import os
os.environ['OBJC_DISABLE_INITIALIZE_FORK_SAFETY'] = 'YES'
import io
import json
import logging
from firebase_functions import https_fn
from services.ocr_service import extract_receipt_data, extract_text
import tempfile

# Configure logging
logging.basicConfig(level=logging.INFO)

@https_fn.on_request()
def process_receipt(req: https_fn.Request) -> https_fn.Response:
    try:

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
        logging.info(f"Read {len(image_data)} bytes from file")

        # # Save the image data to a temporary file
        # with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
        #     temp_file.write(image_data)
        #     temp_filename = temp_file.name
        #
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
            response_data = {
                "message": "Receipt processed successfully",
                "receipt_data": parsed_data
            }
            
            return https_fn.Response(json.dumps(response_data), status=200, content_type='application/json')
        finally:
            # Clean up the temporary file
            logging.info("Temporary file cleaned up")
    except Exception as e:
        logging.error(f"Error in process_receipt: {str(e)}", exc_info=True)
        return https_fn.Response(json.dumps({"error": str(e)}), status=500, content_type='application/json')