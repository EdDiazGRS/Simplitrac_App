import io
import logging
from PIL import Image
from firebase_functions import https_fn
from services.ocr_service import extract_receipt_data, extract_text
from repository.ocr_repository import store_receipt_data
import tempfile
import os
import base64

# Configure logging
logging.basicConfig(level=logging.INFO)

def process_receipt(req: https_fn.Request) -> https_fn.Response:
    try:
        logging.info("Starting process_receipt function")
        
        # Check if the request contains JSON data
        if not req.is_json:
            return https_fn.Response("Request must be JSON", status=400)
        
        # Get the JSON data
        data = req.get_json()
        
        # Check if the 'image' field exists in the JSON data
        if 'image' not in data:
            return https_fn.Response("Image blob is required", status=400)
        
        # Get the base64 encoded image blob
        image_blob_base64 = data['image']
        
        logging.info("Image blob received, processing image")
        
        try:
            # Decode the base64 string to bytes
            image_blob = base64.b64decode(image_blob_base64)
        except:
            return https_fn.Response("Invalid base64 encoded image", status=400)
        
        # Open the image from the blob
        try:
            img = Image.open(io.BytesIO(image_blob))
        except:
            return https_fn.Response("Invalid image format", status=400)
        
        # Resize the image
        img.thumbnail((800, 800))  # Reduced to 800x800 max
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG', quality=70)
        img_byte_arr = img_byte_arr.getvalue()
        
        logging.info("Image resized")
        
        # Save resized image to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
            temp_file.write(img_byte_arr)
            temp_filename = temp_file.name
        
        try:
            logging.info("Extracting text from image")
            # Extract text from the image
            extracted_text = extract_text(temp_filename)
            if not extracted_text:
                return https_fn.Response("No text detected in the image", status=400)
            
            logging.info("Parsing extracted text")
            # Parse the extracted text
            parsed_data = extract_receipt_data(extracted_text)
            
            logging.info("Storing parsed data")
            # Store the parsed data
            doc_ref = store_receipt_data("receipts", parsed_data)
            
            if not doc_ref:
                return https_fn.Response("Failed to store receipt data", status=500)
            
            logging.info(f"Receipt processed and stored successfully with ID: {doc_ref.id}")
            return https_fn.Response(f"Receipt processed and stored with ID: {doc_ref.id}", status=200)
        
        finally:
            # Clean up the temporary file
            os.unlink(temp_filename)
            logging.info("Temporary file cleaned up")
    
    except Exception as e:
        logging.error(f"Error in process_receipt: {str(e)}", exc_info=True)
        return https_fn.Response(f"An error occurred: {str(e)}", status=500)
