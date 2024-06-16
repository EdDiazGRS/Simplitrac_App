# backend/functions/data/ocr_data.py
import os
import re
from datetime import datetime
from google.cloud import vision
from google.cloud import storage
from firebase_admin import firestore, credentials, initialize_app
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords

# Set the path to your service account key file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/eddiaz/Desktop/simplitracapp-1846334f37cc.json"

# Check if the default app is already initialized
# cred = credentials.Certificate(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
# initialize_app(cred)

# Download NLTK data
nltk.download('punkt')
nltk.download('stopwords')

# Initialize Vision and Firestore clients
vision_client = vision.ImageAnnotatorClient()
storage_client = storage.Client()
firestore_client = firestore.client()

def download_image(bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)
    print(f"Blob {source_blob_name} downloaded to {destination_file_name}.")

def extract_text(image_path):
    """Detects text in the file."""
    with open(image_path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = vision_client.text_detection(image=image)
    texts = response.text_annotations
    if not texts:
        return None
    return texts[0].description

def parse_receipt_text(text):
    """Parse the extracted text to find key data using regex and NLP."""
    data = {
        "date": extract_date(text),
        "total": extract_total(text),
        "items": extract_items(text),
    }
    return data

def extract_date(text):
    """Extract date using regex."""
    date_patterns = [
        r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',
        r'\b\d{4}[/-]\d{1,2}[/-]\d{1,2}\b',
        r'\b\d{1,2}\s+\w+\s+\d{4}\b',
    ]
    for pattern in date_patterns:
        match = re.search(pattern, text)
        if match:
            return match.group()
    return None

def extract_total(text):
    """Extract total amount using regex."""
    total_patterns = [
        r'\btotal\s*[:\s]*\d+[.,]?\d*\b',
        r'\bamount\s*[:\s]*\d+[.,]?\d*\b',
        r'\bsubtotal\s*[:\s]*\d+[.,]?\d*\b',
    ]
    for pattern in total_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group().split()[-1].replace(',', '')
    return None

def extract_items(text):
    """Extract items using NLP techniques."""
    stop_words = set(stopwords.words('english'))
    sentences = sent_tokenize(text)
    items = []
    for sentence in sentences:
        words = word_tokenize(sentence)
        words = [word for word in words if word.lower() not in stop_words and word.isalpha()]
        if len(words) > 1:  # Assuming item descriptions are usually more than one word
            items.append(' '.join(words))
    return items

def store_receipt_data(collection_name, document_data):
    """Stores the parsed receipt data into Firestore."""
    doc_ref = firestore_client.collection(collection_name).add(document_data)
    return doc_ref
