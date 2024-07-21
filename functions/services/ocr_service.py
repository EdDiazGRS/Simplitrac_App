import io
import json
import logging
import os
import re
from typing import Optional, Dict
from datetime import datetime
from google.cloud import vision
# from google.cloud import storage
from firebase_admin import firestore, credentials, initialize_app
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from openai import OpenAI


# Load environment variables
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = os.path.join(os.path.dirname(__file__), '../.env')
load_dotenv(env_path)

curr_path = os.path.dirname(__file__)
root_path = f'{curr_path}/../'

# Get the service account credentials from the environment variable
env_string = os.getenv("SECRET_KEY_FOR_FIREBASE")

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Append to NLTK paths
nltk.data.path.append(f'{root_path}nltk_data')


@lambda _: _()
def find_files():
    if env_string:
        try:
            env_json = json.loads(env_string)

            json_file_path = f'{root_path}temp_google_credentials.json'

            if not os.path.exists(json_file_path):
                with open(json_file_path, 'w') as temp_file:
                    json.dump(env_json, temp_file)

            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.abspath(json_file_path)
        except json.JSONDecodeError:
            print("Invalid JSON in SECRET_KEY_FOR_FIREBASE environment variable")
    else:
        print("SECRET_KEY_FOR_FIREBASE not found in environment variables")

    # Function to check if NLTK data packages are downloaded


def check_nltk_data(package):
    try:
        nltk.data.find(f'{package}')
        return True
    except LookupError:
        return False


# Download NLTK data if not already present
if not check_nltk_data('tokenizers/punkt'):
    nltk.download('punkt')
if not check_nltk_data('corpora/stopwords'):
    nltk.download('stopwords')

# # Initialize Vision client
# client = vision.ImageAnnotatorClient()

# def extract_text(image_path):
#     """Extracts text from the image using Google Cloud Vision API."""
#     with io.open(image_path, 'rb') as image_file:
#         content = image_file.read()

#     image = vision.Image(content=content)
#     response = client.text_detection(image=image)
#     texts = response.text_annotations

#     if texts:
#         return texts[0].description
#     return None

# def extract_receipt_data(text):
#     """Parses the extracted text to find key receipt data."""
#     # Implement your parsing logic here
#     # This is a placeholder implementation
#     lines = text.split('\n')
#     data = {
#         'store_name': lines[0] if lines else '',
#         'date': '',
#         'total': '',
#         'items': []
#     }

#     for line in lines[1:]:
#         if 'date' in line.lower():
#             data['date'] = line
#         elif 'total' in line.lower():
#             data['total'] = line
#         else:
#             data['items'].append(line)

#     return data
# Initialize Vision and Firestore clients


# storage_client = storage.Client()

def extract_text(image_file):
    vision_client = vision.ImageAnnotatorClient()

    """Detects text in the file."""
    image = vision.Image(content=image_file)

    logging.info("Detecting text in picture")

    response = vision_client.text_detection(image=image)
    logging.info(response.text_annotations)
    texts = response.text_annotations
    if not texts:
        return None
    else:
       
        return texts[0].description 
    
def process_receipt_image(extracted_text):
    """Process the extracted text using OpenAI API."""
    list_of_categories = "Vehicle, Insurance/health, Rent/mortgage, Meals, Travels, Supplies, Cellphone, Utilities"
    prompt = f"""
    Given this extracted text from a receipt:
    {extracted_text}
    Return a JSON object with the vendor name, date, amount, and category from this list of categories : ({list_of_categories}). Do not include any Markdown formatting or code block syntax in your response.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a skilled financial professional with detailed accounting skills."},
                {"role": "user", "content": prompt}
            ]
        )
        
        # Extract the content from the response
        result = response.choices[0].message.content
        
        # Attempt to parse the result as JSON
        try:
            parsed_result = json.loads(result)
            return parsed_result
        except json.JSONDecodeError:
            logging.error("Failed to parse the OpenAI response as JSON")
            return result  # Return the raw string if it's not valid JSON

    except Exception as e:
        logging.error(f"Error in OpenAI API call: {str(e)}")
        return None


# def parse_receipt_text(text):
#     """Parse the extracted text to find key data using regex and NLP."""
#     subtotal, tax, total = extract_total(text)
#     date = extract_date(text)

#     print("Extracted Date:", date)
#     print("Extracted Subtotal:", subtotal)
#     print("Extracted Tax:", tax)
#     print("Extracted Total:", total)

#     data = {
#         "date": date,
#         "subtotal": subtotal,
#         "tax": tax,
#         "total": total,

#     }
#     return data

# def extract_date(text):
#     """Extract date using regex."""
#     date_patterns = [
#         r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',
#         r'\b\d{4}[/-]\d{1,2}[/-]\d{1,2}\b',
#         r'\b\d{1,2}\s+\w+\s+\d{4}\b',
#         r'\d{1,2}/\d{1,2}/\d{4}',  # MM/DD/YYYY
#         r'\d{1,2}-\d{1,2}-\d{4}',  # MM-DD-YYYY
#         r'\d{1,2}/\d{1,2}/\d{2}',  # MM/DD/YY
#         r'\d{1,2}-\d{1,2}-\d{2}',  # MM-DD-YY
#     ]
    # for pattern in date_patterns:
    #     match = re.search(pattern, text)
    #     if match:
    #         return match.group()
    # return None


# def extract_receipt_data(text: str) -> Dict[str, Optional[str]]:
#     lines = text.split('\n')
#     data = {
#         'date': None,
#         'subtotal': None,
#         'tax': None,
#         'total': None,
#         'store_name': None,
#         'created_at': None,
#         'vendor': None,
#         'amount': None
#     }

    # #Extract store name (usually in the first few lines)
    # for i, line in enumerate(lines[:5]):
    #     if len(line.strip()) > 0 and not re.search(r'\d', line):  # Look for non-empty lines without numbers
    #         data['store_name'] = line.strip()
    #         break
    #     if i == 4 and not data['store_name']:  # If no store name found in first 5 lines, use the first non-empty line
    #         for line in lines:
    #             if len(line.strip()) > 0:
    #                 data['store_name'] = line.strip()
    #                 break

    # # Extract date
    # date_pattern = r'\b\d{1,2}[/.-]\d{1,2}[/.-]\d{2,4}\b'
    # for line in lines:
    #     date_match = re.search(date_pattern, line)
    #     if date_match:
    #         data['date'] = date_match.group()
    #         break

    # Extract subtotal, tax, and total
    # subtotal_found = False
    # for i, line in enumerate(lines):
    #     # Subtotal
    #     if re.search(r'\b(Subtotal|Sub[ -]?total|Items\s+Subtotal)\b', line, re.IGNORECASE) and not subtotal_found:
    #         subtotal_match = re.search(r'\$?(\d+\.\d{2})', line)
    #         if subtotal_match:
    #             data['subtotal'] = subtotal_match.group(1)
    #             subtotal_found = True
    #         elif i + 1 < len(lines):
    #             subtotal_match = re.search(r'\$?(\d+\.\d{2})', lines[i + 1])
    #             if subtotal_match:
    #                 data['subtotal'] = subtotal_match.group(1)
    #                 subtotal_found = True

        # # Tax
        # if re.search(r'\b(Tax|Sales\s+Tax)\b', line, re.IGNORECASE):
        #     tax_match = re.search(r'\$?(\d+\.\d{2})', line)
        #     if tax_match:
        #         data['tax'] = tax_match.group(1)
        #     elif i + 1 < len(lines):
        #         tax_match = re.search(r'\$?(\d+\.\d{2})', lines[i + 1])
        #         if tax_match:
        #             data['tax'] = tax_match.group(1)

        # # Total
        # if re.search(r'\b(Total|Grand\s+Total)\b', line, re.IGNORECASE):
        #     total_matches = re.findall(r'\$?(\d+\.\d{2})', line)
        #     if total_matches:
        #         data['total'] = total_matches[-1]  # Take the last match if multiple found
        #     elif i + 1 < len(lines):
        #         total_matches = re.findall(r'\$?(\d+\.\d{2})', lines[i + 1])
        #         if total_matches:
        #             data['total'] = total_matches[-1]  # Take the last match if multiple found

    # # If tax is not found, try to calculate it
    # if data['subtotal'] and data['total'] and not data['tax']:
    #     try:
    #         subtotal = float(data['subtotal'])
    #         total = float(data['total'])
    #         calculated_tax = total - subtotal
    #         data['tax'] = f"{calculated_tax:.2f}"
    #     except ValueError:
    #         pass

    # data['created_at'] = data.get("date")
    # data['vendor'] = data.get("store_name")
    # data['amount'] = data.get("total")

    # return data


# def store_receipt_data(collection_name, document_data):
#     """Stores the parsed receipt data into Firestore."""
#     doc_ref = firestore_client.collection(collection_name).add(document_data)
#     return doc_ref

# Test the updated code with the provided images
# if __name__ == "__main__":
#     image_paths = ["/Users/eddiaz/Desktop/SimpliTrac/functions/services/R3.jpg"]
#     for image_path in image_paths:
#         text = extract_text(image_path)
#         print("Extracted text:")
#         print(text)
#         print("\nParsing receipt data...")
#         parsed_data = extract_receipt_data(text)
#         print("\nParsed Receipt Data:", parsed_data)