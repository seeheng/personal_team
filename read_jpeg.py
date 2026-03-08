import argparse
import json
import os
import ollama

MODEL_NAME = "qwen2.5vl:7b"

EXTRACTION_PROMPT = """
Extract ONLY the handwritten text from this Delivery Note into a JSON object. 
Ignore all printed boilerplate text.

"SYSTEM INSTRUCTION: This is a stateless request. Analyze ONLY the pixels in the provided image. Disregard all previous names, dates, and items. If the visual evidence contradicts previous knowledge, follow the visual evidence."

Extraction Rules for Handwritten Fields:
- 'no': The red number at the top right.
- 'account_of': Extract the multi-line name and address after 'FOR ACCOUNT OF'.
- 'items': An array of objects containing 'quantity' and 'description'.
    * Unit Recognition: The first handwritten word is the unit. Be highly sensitive to "Tin", "Tins", "Unt" (unit), "Pcs", "Box", "Roll", or "Set". 
    * Handwriting Note: In these forms, "Tin" often starts with a large, loopy cursive 'T' that may resemble a 'Z' or a checkmark.
    * Multi-line Logic: If a line in the table has no unit/quantity at the start, append that text to the 'description' of the previous item (e.g., "High Gloss Signal Red" belongs to the Tin of Nippon Platone).
    * Format: Convert "1 Tin" or "1 Tins" into "1 tin". If the handwriting says "unt", normalize to "unit".
    * Dimensions: Ensure a space between whole numbers and fractions (e.g., "80 1/4"). Escape all inch symbols (\").
    *Distinguish between 'pc' (looks like a cursive 'p') and 'tin' (starts with a large cursive flourish). The first item in this specific image (85005) is '1 pc 1/2" Metco Garden Tap'.
- 'date_main': The handwritten date at the bottom left.
- 'per': The vehicle/reference number on the 'PER' line (e.g., "WMW 3365I").
- 'signature_present': true/false based on the recipient box.
- 'recipient_date': The date/shorthand written at the bottom right.

Return ONLY the raw JSON string.
"""

def describe_image_ollama(image_path):

    try:
        response = ollama.chat(
            model=MODEL_NAME,
                messages=[{
                   'role': 'user',
                   'content': EXTRACTION_PROMPT,
                   'images': [image_path]
                    }],
                options={'num_ctx': 4096} # Keeps memory usage stable on your RTX 3060
                
        )    
        return response  # Indent the JSON output for better readability
    except Exception as e:
        return f"Error processing image: {str(e)}"
# Usage
#print(describe_image_ollama("./henry/c.jpeg"))
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process a file.')
    parser.add_argument('filename', type=str, help='The name of the file to process')

    args = parser.parse_args()

    #process_file(args.filename)
    print(describe_image_ollama(args.filename))
        