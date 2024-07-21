import os
import io
import json
import logging
from google.cloud import vision
from openai import OpenAI

# Set up logging
logging.basicConfig(level=logging.INFO)

# Set the path to your Google Cloud service account key file
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/eddiaz/Desktop/simplitracapp-428d927d2e98.json'

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def extract_text(image_path):
    """Detects text in the file."""
    vision_client = vision.ImageAnnotatorClient()

    # Read the image file
    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    
    logging.info("Detecting text in picture")
    response = vision_client.text_detection(image=image)
    logging.info(f"Response received: {response}")
    
    texts = response.text_annotations
    
    if not texts:
        logging.info("No text detected in the image")
        return None
    else:
        detected_text = texts[0].description
        logging.info(f"Detected text: {detected_text}")
        return detected_text

def process_receipt(extracted_text):
    """Process the extracted text using OpenAI API."""
    prompt = f"""
    Given this extracted text from a receipt:
    {extracted_text}
    Return a JSON object with the vendor name, date, amount, and category from this list of categories : (Vehicle
Insurance/health, Rent/mortgage, Meals, Travels, Supplies, Cellphone, Utilities
). Do not include any Markdown formatting or code block syntax in your response.
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

# Path to your local image file
image_path = '/Users/eddiaz/Desktop/SimpliTrac/functions/services/R4.jpg'

# Test the function
if __name__ == "__main__":
    if not os.path.exists(image_path):
        logging.error(f"Image file not found: {image_path}")
    else:
        extracted_text = extract_text(image_path)
        if extracted_text:
            print(f"Extracted text:\n{extracted_text}")
            
            processed_result = process_receipt(extracted_text)
            if processed_result:
                print("Processed result:")
                print(json.dumps(processed_result, indent=2))
            else:
                print("Failed to process the receipt.")
        else:
            print("No text was extracted from the image.")