import sys
import os
from firebase_functions import https_fn
from pathlib import Path

sys.path.insert(0, Path(__file__).parent.parent.parent.as_posix())
from backend.functions.controllers.messages_controller import addmessage

# The Firebase Admin SDK to access Cloud Firestore.
from firebase_admin import initialize_app

app = initialize_app()

# Import the OCR service
from backend.functions.data.ocr_data import (
    download_image,
    extract_text,
    parse_receipt_text,
    store_receipt_data,
)

@https_fn.on_request()
def process_receipt(req: https_fn.Request) -> https_fn.Response:
    """HTTP Cloud Function to process a receipt image."""
    bucket_name = req.args.get("bucket")
    source_blob_name = req.args.get("file")
    local_image_path = f"/tmp/{source_blob_name}"

    if not bucket_name or not source_blob_name:
        return https_fn.Response("Missing bucket or file parameter", status=400)

    # Download image from Firebase Storage
    download_image(bucket_name, source_blob_name, local_image_path)

    # Extract text using Google Vision API
    extracted_text = extract_text(local_image_path)
    if not extracted_text:
        return https_fn.Response("No text detected", status=400)

    # Parse the extracted text
    receipt_data = parse_receipt_text(extracted_text)

    # Store the parsed data in Firestore
    doc_ref = store_receipt_data("receipts", receipt_data)

    return https_fn.Response(f"Receipt processed and stored with ID: {doc_ref.id}", status=200)

