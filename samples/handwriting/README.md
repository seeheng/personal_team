# Handwriting Recognition Samples

This directory contains sample handwritten images for training and validation.

## Directory Structure

```
handwriting/
├── training/
│   ├── english/           # English handwriting samples
│   │   ├── sample_001.jpg
│   │   ├── sample_001.txt (ground truth)
│   │   └── ...
│   └── multilingual/      # Non-English language samples
│       ├── sample_001.jpg
│       ├── sample_001.txt (ground truth)
│       └── ...
├── validation/            # Validation/test samples
│   ├── sample_001.jpg
│   └── ...
└── metadata.json          # Dataset metadata
```

## How to Add Samples

1. **Create Sample Image**: Take or scan a handwritten note/text
2. **Save Image**: Save as `sample_XXX.jpg` in appropriate folder
3. **Create Annotation**: Create `sample_XXX.txt` containing the ground truth text
4. **Update Metadata**: The `metadata.json` will auto-update when training

### Example

```
training/english/
├── sample_001.jpg        (Image of handwritten: "Hello World")
└── sample_001.txt        (Contains: "Hello World")
```

## Sample Requirements

- **Image Quality**: Clear, legible handwriting
- **Resolution**: Minimum 200x200 pixels, optimal 300+ dpi
- **Format**: PNG, JPG, or WebP
- **Text**: Mixed content (words, sentences, numbers)
- **Diversity**: Various handwriting styles and ink colors

## Annotation Format

Text files should contain:
- Exact transcription of handwritten text
- UTF-8 encoding
- One line per sample (or multiple lines if handwriting spans multiple lines)

## Sample Categories

### English Training Samples (`training/english/`)
- Print handwriting
- Cursive handwriting
- Mixed script
- Common words and phrases

### Multilingual Samples (`training/multilingual/`)
- Spanish samples
- French samples
- German samples
- Asian language samples (Chinese, Japanese, Korean)
- Arabic samples

### Validation Samples (`validation/`)
- Holdout test set for model evaluation
- Not used in training
- Used to assess model performance

---

**Note**: No sample images are included by default. Add your own handwritten images to train the model effectively.
