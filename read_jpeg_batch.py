import os
import ollama

# Configuration
INPUT_FOLDER = "handwritten_forms"   # Put your images here
OUTPUT_FOLDER = "extracted_data"     # Where JSON files will be saved
MODEL_NAME = "qwen2.5vl:7b"

# Ensure output directory exists
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Optimized Prompt for the specific Delivery Note layout
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

def batch_process():
    # Loop through common image formats
    for filename in os.listdir(INPUT_FOLDER):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(INPUT_FOLDER, filename)
            print(f"Processing {filename}...")

            try:
                response = ollama.chat(
                    model=MODEL_NAME,
                    messages=[{
                        'role': 'user',
                        'content': EXTRACTION_PROMPT,
                        'images': [image_path]
                    }]
                )

                # Save output as .json file
                output_name = os.path.splitext(filename)[0] + ".json"
                with open(os.path.join(OUTPUT_FOLDER, output_name), "w") as f:
                    f.write(response['message']['content'])
                
                print(f"Successfully saved to {output_name}")

            except Exception as e:
                print(f"Failed to process {filename}: {str(e)}")

if __name__ == "__main__":
    batch_process()