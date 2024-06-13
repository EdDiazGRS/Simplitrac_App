import firebase_functions as functions
import firebase_admin
from firebase_functions import firestore_fn, https_fn


# The Firebase Admin SDK to access Cloud Firestore.
from firebase_admin import firestore
import google.cloud.firestore

from backend.functions.models.Response import Response


async def add_document(collection_name: str, document) -> Response:
    """
    Take the document and add it to the specified collection
    """
    result = Response()

    firestore_client: google.cloud.firestore.Client = firestore.client()

    # Push the new message into Cloud Firestore using the Firebase Admin SDK.

    try:
        _, doc_ref = firestore_client.collection(collection_name).add(document)

        if doc_ref:
            result.set_payload(payload=doc_ref)
        else:
            error: str = "Could not add a document"
            result.set_errors(error=error)
    except:
        error: str = "Could not add a document"
        result.set_errors(error=error)

    return result
