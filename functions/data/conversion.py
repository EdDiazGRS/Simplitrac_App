import base64

def convert_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        base64_string = base64.b64encode(image_file.read()).decode('utf-8')
        return base64_string

def save_base64_to_file(base64_string, output_path):
    with open(output_path, "w") as output_file:
        output_file.write(base64_string)

if __name__ == "__main__":
    image_path = "/Users/eddiaz/Desktop/SimpliTrac/functions/services/R3.jpg"
    output_path = "/Users/eddiaz/Desktop/SimpliTrac/functions/services/R3_base64.txt"
    
    base64_image = convert_image_to_base64(image_path)
    save_base64_to_file(base64_image, output_path)
    
    print(f"Base64 string saved to {output_path}")
