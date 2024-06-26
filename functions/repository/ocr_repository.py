# ocr_repository.py

from firebase_admin import firestore

firestore_client = firestore.client()

def store_receipt_data(collection_name, document_data):
    """Stores the parsed receipt data into Firestore."""
    try:
        doc_ref = firestore_client.collection(collection_name).add(document_data)
        print(f"Document added with ID: {doc_ref.id}")
        return doc_ref
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
