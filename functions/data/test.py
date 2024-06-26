import json
import os
import firebase_admin
from firebase_admin import firestore, credentials
from dotenv import load_dotenv

# Load environment variables
env_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
print(f"Loading .env file from: {env_path}")
load_dotenv(env_path)

firebase_service_account = os.getenv('SECRET_KEY_FOR_FIREBASE')
print(f"Firebase Service Account: {firebase_service_account}")

if not firebase_service_account:
    raise ValueError("SECRET_KEY_FOR_FIREBASE environment variable is not set or is empty")

firebase_config = json.loads(firebase_service_account)
cred = credentials.Certificate(firebase_config)
firebase_admin.initialize_app(cred)

db = firestore.client()

# Test Firestore connection
try:
    # Add a document to a test collection
    doc_ref = db.collection('testCollection').document('testDocument')
    doc_ref.set({
        'name': 'Test User',
        'timestamp': firestore.SERVER_TIMESTAMP
    })
    print("Document added to Firestore successfully.")
except Exception as e:
    print(f"Error adding document to Firestore: {e}")
