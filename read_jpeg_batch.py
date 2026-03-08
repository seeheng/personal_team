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

Use the following keys:
* no: The red number at the top right.
* account_of: The name/address on the 'FOR ACCOUNT OF' line.
* date_main: The date written at the bottom left.
* items: An array of objects: 'quantity' and 'description'. Pay close attention to hardware fractions (e.g., 3/8", 1/4", 7/8").
* per: The text on the 'PER' line.
* signature_present: True/False.
* recipient_date: The date next to the signature.

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