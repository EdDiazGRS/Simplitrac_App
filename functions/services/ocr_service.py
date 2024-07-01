import os
import re
from typing import Optional, Dict
from datetime import datetime
from google.cloud import vision
from google.cloud import storage
from firebase_admin import firestore, credentials, initialize_app
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords

# Set the path to your service account key file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/eddiaz/Desktop/simplitracapp-1846334f37cc.json"

# Download NLTK data
nltk.download('punkt')
nltk.download('stopwords')

# Initialize Vision and Firestore clients
vision_client = vision.ImageAnnotatorClient()
storage_client = storage.Client()

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
    subtotal, tax, total = extract_total(text)
    date = extract_date(text)
    
    print("Extracted Date:", date)
    print("Extracted Subtotal:", subtotal)
    print("Extracted Tax:", tax)
    print("Extracted Total:", total)
    
    data = {
        "date": date,
        "subtotal": subtotal,
        "tax": tax,
        "total": total,
    
    }
    return data

def extract_date(text):
    """Extract date using regex."""
    date_patterns = [
        r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',
        r'\b\d{4}[/-]\d{1,2}[/-]\d{1,2}\b',
        r'\b\d{1,2}\s+\w+\s+\d{4}\b',
        r'\d{1,2}/\d{1,2}/\d{4}',  # MM/DD/YYYY
        r'\d{1,2}-\d{1,2}-\d{4}',  # MM-DD-YYYY
        r'\d{1,2}/\d{1,2}/\d{2}',  # MM/DD/YY
        r'\d{1,2}-\d{1,2}-\d{2}',  # MM-DD-YY
    ]
    for pattern in date_patterns:
        match = re.search(pattern, text)
        if match:
            return match.group()
    return None

def extract_receipt_data(text: str) -> Dict[str, Optional[str]]:
    lines = text.split('\n')
    data = {
        'date': None,
        'subtotal': None,
        'tax': None,
        'total': None,
        'store_name': None,
    }

    # Extract store name (usually in the first few lines)
    for i, line in enumerate(lines[:5]):
        if len(line.strip()) > 0 and not re.search(r'\d', line):  # Look for non-empty lines without numbers
            data['store_name'] = line.strip()
            break
        if i == 4 and not data['store_name']:  # If no store name found in first 5 lines, use the first non-empty line
            for line in lines:
                if len(line.strip()) > 0:
                    data['store_name'] = line.strip()
                    break

    # Extract date
    date_pattern = r'\b\d{1,2}[/.-]\d{1,2}[/.-]\d{2,4}\b'
    for line in lines:
        date_match = re.search(date_pattern, line)
        if date_match:
            data['date'] = date_match.group()
            break

    # Extract subtotal, tax, and total
    subtotal_found = False
    for i, line in enumerate(lines):
        # Subtotal
        if re.search(r'\b(Subtotal|Sub[ -]?total|Items\s+Subtotal)\b', line, re.IGNORECASE) and not subtotal_found:
            subtotal_match = re.search(r'\$?(\d+\.\d{2})', line)
            if subtotal_match:
                data['subtotal'] = subtotal_match.group(1)
                subtotal_found = True
            elif i + 1 < len(lines):
                subtotal_match = re.search(r'\$?(\d+\.\d{2})', lines[i+1])
                if subtotal_match:
                    data['subtotal'] = subtotal_match.group(1)
                    subtotal_found = True

        # Tax
        if re.search(r'\b(Tax|Sales\s+Tax)\b', line, re.IGNORECASE):
            tax_match = re.search(r'\$?(\d+\.\d{2})', line)
            if tax_match:
                data['tax'] = tax_match.group(1)
            elif i + 1 < len(lines):
                tax_match = re.search(r'\$?(\d+\.\d{2})', lines[i+1])
                if tax_match:
                    data['tax'] = tax_match.group(1)

        # Total
        if re.search(r'\b(Total|Grand\s+Total)\b', line, re.IGNORECASE):
            total_matches = re.findall(r'\$?(\d+\.\d{2})', line)
            if total_matches:
                data['total'] = total_matches[-1]  # Take the last match if multiple found
            elif i + 1 < len(lines):
                total_matches = re.findall(r'\$?(\d+\.\d{2})', lines[i+1])
                if total_matches:
                    data['total'] = total_matches[-1]  # Take the last match if multiple found

    # If tax is not found, try to calculate it
    if data['subtotal'] and data['total'] and not data['tax']:
        try:
            subtotal = float(data['subtotal'])
            total = float(data['total'])
            calculated_tax = total - subtotal
            data['tax'] = f"{calculated_tax:.2f}"
        except ValueError:
            pass

    return data
   


def store_receipt_data(collection_name, document_data):
    """Stores the parsed receipt data into Firestore."""
    doc_ref = firestore_client.collection(collection_name).add(document_data)
    return doc_ref

# Test the updated code with the provided images
if __name__ == "__main__":
    image_paths = ["/Users/eddiaz/Desktop/SimpliTrac/functions/services/R3.jpg"]
    for image_path in image_paths:
        text = extract_text(image_path)
        print("Extracted text:")
        print(text)
        print("\nParsing receipt data...")
        parsed_data = extract_receipt_data(text)
        print("\nParsed Receipt Data:", parsed_data)

