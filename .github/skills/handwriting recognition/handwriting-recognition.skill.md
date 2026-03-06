# Handwriting Recognition Skill

## Skill Metadata
```yaml
name: handwriting-recognition
version: 1.0.0
description: Recognizes and interprets handwritten text from images using machine learning models
agent: personal-assistant
category: image-processing
status: active
```

## Overview
This skill enables the personal assistant agent to:
- Recognize handwritten text from images
- Learn and improve from sample images in the `./samples` folder
- Support multiple handwriting styles and languages
- Extract and interpret handwritten notes
- Provide confidence scores for recognized text

## Capabilities

### Core Features
- **Text Recognition**: Extract handwritten text from images with high accuracy
- **Style Adaptation**: Learn from diverse handwriting samples
- **Multi-language Support**: Recognize handwriting in different languages
- **Confidence Scoring**: Provide reliability metrics for each recognition
- **Batch Processing**: Process multiple images efficiently

### Supported Input Formats
- PNG, JPG, JPEG, WebP, BMP
- Resolution: Minimum 150x150px, optimal 300+ dpi
- Color or grayscale images

## Dependencies

### Required Libraries
```python
# Core ML/Vision
opencv-python>=4.8.0      # Image processing
pillow>=10.0.0            # Image manipulation
numpy>=1.24.0             # Numerical computing

# Handwriting Recognition
pytesseract>=0.3.10       # OCR engine wrapper
paddleocr>=2.7.0          # Advanced OCR with handwriting support

# Deep Learning
tensorflow>=2.13.0        # Neural network framework
torch>=2.0.0              # Alternative ML framework

# Utilities
scikit-learn>=1.3.0       # Machine learning utilities
scipy>=1.11.0             # Scientific computing
```

### Optional Dependencies
```python
huggingface-hub>=0.17.0   # Access pre-trained models
onnx>=1.14.0              # Model format support
```

## Configuration

### config.json
```json
{
  "skill": "handwriting-recognition",
  "model": {
    "primary": "paddleocr",
    "fallback": "pytesseract",
    "pretrained_model_path": "./models/handwriting"
  },
  "training": {
    "enabled": true,
    "sample_path": "./samples/handwriting",
    "auto_improve": true,
    "batch_size": 32,
    "epochs": 50
  },
  "processing": {
    "image_preprocessing": true,
    "grayscale_conversion": true,
    "threshold_adjustment": true,
    "dpi_optimization": 300
  },
  "output": {
    "confidence_threshold": 0.7,
    "return_confidence": true,
    "return_bounding_boxes": false
  }
}
```

## Input/Output Specifications

### Input
```python
{
  "image_path": "path/to/image.jpg",  # Required: Local file path or URL
  "language": "en",                   # Optional: ISO 639-1 code (default: "en")
  "confidence_threshold": 0.7,        # Optional: Minimum confidence (0-1)
  "preprocess": True,                 # Optional: Apply preprocessing
  "batch_processing": False           # Optional: Batch mode for multiple images
}
```

### Output
```python
{
  "status": "success",
  "recognized_text": "The handwritten text content",
  "confidence": 0.92,
  "language": "en",
  "processing_time": 1.234,  # seconds
  "detailed_results": [
    {
      "text": "word1",
      "confidence": 0.95,
      "position": {"x": 10, "y": 20, "width": 50, "height": 30}
    }
  ],
  "metadata": {
    "image_size": {"width": 800, "height": 600},
    "model_used": "paddleocr",
    "preprocessing_applied": ["grayscale", "threshold"]
  }
}
```

## Usage Examples

### Basic Usage
```python
from skills.handwriting_recognition import HandwritingRecognizer

recognizer = HandwritingRecognizer()
result = recognizer.recognize("./samples/handwriting/note.jpg")
print(f"Text: {result['recognized_text']}")
print(f"Confidence: {result['confidence']}")
```

### Advanced Usage with Training
```python
from skills.handwriting_recognition import HandwritingRecognizer

recognizer = HandwritingRecognizer(config="./config.json")

# Train on sample images
recognizer.train_from_samples(
    sample_dir="./samples/handwriting",
    epochs=50,
    validation_split=0.2
)

# Recognize with custom settings
result = recognizer.recognize(
    image_path="./samples/handwriting/test.jpg",
    language="en",
    confidence_threshold=0.75
)

# Get detailed analysis
if result['status'] == 'success':
    print(f"Recognized: {result['recognized_text']}")
    print(f"Details: {result['detailed_results']}")
```

### Batch Processing
```python
recognizer = HandwritingRecognizer()

# Process multiple images
results = recognizer.recognize_batch(
    image_paths=[
        "./samples/handwriting/page1.jpg",
        "./samples/handwriting/page2.jpg",
        "./samples/handwriting/page3.jpg"
    ]
)

for img_path, result in zip(image_paths, results):
    print(f"{img_path}: {result['recognized_text']}")
```

## Sample Data Structure

The skill expects sample images in this structure:
```
./samples/handwriting/
├── training/
│   ├── english/
│   │   ├── sample_001.jpg
│   │   ├── sample_002.jpg
│   │   └── annotations_001.txt
│   └── other_languages/
│       └── sample_*.jpg
├── validation/
│   └── sample_*.jpg
└── metadata.json
```

### metadata.json Format
```json
{
  "total_samples": 150,
  "languages": ["en", "es", "fr"],
  "styles": ["cursive", "print", "mixed"],
  "last_updated": "2026-03-06",
  "training_status": "ready"
}
```

## Integration with Personal Assistant

### Register Skill
Add to `personal-assistant.agent.md`:
```markdown
### Available Skills
- handwriting-recognition: Recognize and interpret handwritten text
```

### Usage in Agent
```python
@skill("handwriting-recognition")
def process_handwritten_note(image_path):
    """
    Process a handwritten note image and extract text.
    
    Args:
        image_path: Path to the image file
    
    Returns:
        Recognized text with confidence scores
    """
    recognizer = HandwritingRecognizer()
    return recognizer.recognize(image_path)
```

## Implementation Guide

### Phase 1: Setup (Weeks 1-2)
1. Install dependencies
2. Set up directory structure
3. Configure environment variables
4. Download pre-trained models

### Phase 2: Core Implementation (Weeks 3-4)
1. Create `HandwritingRecognizer` class
2. Implement image preprocessing pipeline
3. Integrate OCR engines
4. Add error handling and logging

### Phase 3: Training (Weeks 5-6)
1. Collect and annotate sample images
2. Implement training pipeline
3. Create model evaluation metrics
4. Fine-tune hyperparameters

### Phase 4: Integration (Week 7)
1. Register with agent
2. Create API endpoints
3. Add documentation
4. Implement caching

## Performance Considerations

### Optimization Tips
- Use GPU acceleration when available
- Implement image caching
- Batch process multiple images
- Preprocess images to optimal size
- Use model quantization for faster inference

### Expected Performance
- Single image recognition: 0.5-2 seconds
- Accuracy on clean images: 95%+
- Accuracy on complex handwriting: 80-90%
- Batch processing speedup: 3-5x

## Error Handling

### Common Issues
```python
# Issue: Low confidence score
# Solution: Improve image quality or adjust threshold

# Issue: Unsupported language
# Solution: Check language code or add language support

# Issue: Out of memory on large images
# Solution: Reduce image resolution or batch size
```

## Python Implementation Template

```python
# skills/handwriting_recognition/__init__.py
import cv2
import logging
from paddleocr import PaddleOCR
from pathlib import Path

logger = logging.getLogger(__name__)

class HandwritingRecognizer:
    def __init__(self, config_path="./config.json"):
        self.config = self._load_config(config_path)
        self.ocr = PaddleOCR(use_angle_cls=True, lang='en')
        
    def recognize(self, image_path, **kwargs):
        """Recognize handwritten text from image."""
        try:
            image = cv2.imread(str(image_path))
            results = self.ocr.ocr(image, cls=True)
            return self._format_results(results, image_path)
        except Exception as e:
            logger.error(f"Recognition failed: {e}")
            return {"status": "error", "message": str(e)}
    
    def _format_results(self, results, image_path):
        """Format OCR results into standardized output."""
        text_list = []
        confidences = []
        
        for line in results:
            for word_info in line:
                text_list.append(word_info[1])
                confidences.append(word_info[2])
        
        return {
            "status": "success",
            "recognized_text": " ".join(text_list),
            "confidence": sum(confidences) / len(confidences) if confidences else 0,
            "detailed_results": results
        }
```

## Testing

### Unit Tests
```python
# tests/test_handwriting_recognition.py
import pytest
from skills.handwriting_recognition import HandwritingRecognizer

def test_recognize_simple_text():
    recognizer = HandwritingRecognizer()
    result = recognizer.recognize("./samples/handwriting/simple.jpg")
    assert result['status'] == 'success'
    assert len(result['recognized_text']) > 0
    assert 0 <= result['confidence'] <= 1
```

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Module not found | Missing dependencies | Run `pip install -r requirements.txt` |
| Low accuracy | Poor image quality | Improve image resolution or contrast |
| Slow processing | Large image size | Resize image or use GPU |
| Memory error | Large batch | Reduce batch size |
| Language not supported | Missing language model | Download language pack |

## Future Enhancements

- Real-time handwriting recognition from camera feed
- Support for mathematical symbols and equations
- Signature verification
- Handwriting style classification
- Multi-page document processing
- Integration with cloud OCR services

---

**Last Updated**: March 6, 2026  
**Maintained By**: Personal Assistant Team  
**License**: MIT
