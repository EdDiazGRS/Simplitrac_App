# ocr_controller.py

from firebase_functions import https_fn
from services.ocr_service import extract_text, parse_receipt_text
from repository.ocr_repository import store_receipt_data
from typing import Union
import json

@https_fn.on_request()
def process_receipt(req: https_fn.Request) -> https_fn.Response:
    """
    Process a receipt image: extract text, parse the receipt, and store the data in Firestore.

    :param req: The request must contain the image path or image data.
    :return: https_fn.Response
    """
    try:
        data = req.get_json()
        image_path = data.get("image_path")
        if not image_path:
            return generate_http_response("Image path is required", 400)

        # Extract text from the image
        extracted_text = extract_text(image_path)
        if not extracted_text:
            return generate_http_response("No text detected in the image", 400)

        # Parse the extracted text
        parsed_data = parse_receipt_text(extracted_text)
        
        # Store the parsed data
        doc_ref = store_receipt_data("receipts", parsed_data)
        if not doc_ref:
            return generate_http_response("Failed to store receipt data", 500)
        
        return https_fn.Response(f"Receipt processed and stored with ID: {doc_ref.id}", 200)
    
    except Exception as e:
        return generate_http_response(f"An error occurred: {str(e)}", 500)


def generate_http_response(message: Union[str, list], code: int) -> https_fn.Response:
    if isinstance(message, list):
        result_message: str = ""
        result_message = result_message.join(", ")
        return https_fn.Response(
            response=json.dumps({'error': result_message}),
            status=code
        )
    else:
        return https_fn.Response(
            response=json.dumps({'error':message}),
            status=code
        )
