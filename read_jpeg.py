import requests
import base64
import argparse

PROMPT = "Extract only the handwritten text from this Delivery Note into a JSON object. The form is from Henry Trading Co., SDN. BHD.. Ignore all printed boilerplate text." \
"Use the following keys:" \
"No: The red number at the top right." \
"account_of: The name and address on the 'FOR ACCOUNT OF' line." \
"date_main: The date written at the bottom left." \
"items: An array of objects, each containing 'quantity' and 'description'. Pay close attention to fractions like 3/8'"' or 1/4'"'." \
"per: The text written on the 'PER' line." \
"signature_present: True/False." \
"recipient_date: The date written next to the signature." \
"If a word is truly illegible, write 'UNCERTAIN' after your best guess. Return ONLY the JSON." 

def describe_image_ollama(image_path):
    with open(image_path, "rb") as f:
        img_base64 = base64.b64encode(f.read()).decode('utf-8')

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "qwen2.5vl:7b",
            "prompt": PROMPT,
            "stream": False,
            "images": [img_base64]
        }
    )
    return response.json().get("response")

# Usage
#print(describe_image_ollama("./henry/c.jpeg"))
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process a file.')
    parser.add_argument('filename', type=str, help='The name of the file to process')

    args = parser.parse_args()

    #process_file(args.filename)
    print(describe_image_ollama(args.filename))