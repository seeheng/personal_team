import requests
import base64
import argparse

def describe_image_ollama(image_path):
    with open(image_path, "rb") as f:
        img_base64 = base64.b64encode(f.read()).decode('utf-8')

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "qwen2.5vl:7b",
            "prompt": "Transcribe the text in this image, no need to describe the image, just extract the text. If no text is detected, return an empty string.",
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