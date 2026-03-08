import requests
import base64
import argparse

PROMPT = """
Extract ONLY the handwritten text from this Delivery Note into a JSON object. 
Ignore all printed boilerplate text.

Key Layout Constraints:
- 'no': The red number at the top right (e.g., "85027").
- 'account_of': Extract the multi-line name and address after 'FOR ACCOUNT OF'.
- 'items': An array of objects:'quoatity' and 'description'. 
    * Note: The first word in handwriting is usually "unit", "pcs", "tin", "box", "pallet", "set".
    * Logic: If a line in the table has no quantity, append its text to the 'description' of the previous item.
    * Dimensions: Ensure all inch symbols (") are properly escaped with a backslash (") within the JSON string values so the output remains valid JSON. Ensure fractions (1/2, 3/4, 3/8, 7/8) have a space after the whole number.
- 'date_main': The handwritten date at the bottom left (e.g., "3/01/2028").
- 'per': The vehicle number or reference written on the 'PER' line.
- 'signature_present': Return true if the 'SIGNATURE OF RECIPIENT' area is signed.
- 'recipient_date': The date written at the very bottom right.

Return ONLY the raw JSON string.
"""

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