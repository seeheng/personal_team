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
In the description field, the first word is usually 'unit'

Use the following keys:Extract ONLY the handwritten text from this Delivery Note into a JSON object. 
Ignore all printed boilerplate text.

Key Layout Constraints:
- 'no': The red number at the top right (e.g., "85027").
- 'account_of': Extract the multi-line name and address after 'FOR ACCOUNT OF'.
- 'items': An array of objects:'quoatity' and 'description'. 
    * Note: Thefirst word in handwriting is usually "unit".
    * Logic: If a line in the table has no quantity, append its text to the 'description' of the previous item.
    * Dimensions: Ensure all inch symbols (") are properly escaped with a backslash (") within the JSON string values so the output remains valid JSON. Ensure fractions (1/2, 3/4, 3/8, 7/8) have a space after the whole number.
- 'date_main': The handwritten date at the bottom left (e.g., "3/01/2028").
- 'per': The vehicle number or reference written on the 'PER' line.
- 'signature_present': Return true if the 'SIGNATURE OF RECIPIENT' area is signed.
- 'recipient_date': The date written at the very bottom right.

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