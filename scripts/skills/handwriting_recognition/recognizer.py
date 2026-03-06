"""
Core Handwriting Recognition Engine

Provides the main HandwritingRecognizer class that handles OCR operations.
"""

import cv2
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Union
from datetime import datetime

logger = logging.getLogger(__name__)


class HandwritingRecognizer:
    """
    Main class for recognizing handwritten text from images.
    
    Attributes:
        config (dict): Configuration dictionary
        ocr_engine (str): Primary OCR engine to use
        confidence_threshold (float): Minimum confidence score
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the HandwritingRecognizer.
        
        Args:
            config_path (str, optional): Path to configuration JSON file
        """
        self.config = self._load_config(config_path)
        self.ocr_engine = self.config.get('model', {}).get('primary', 'paddleocr')
        self.confidence_threshold = self.config.get('output', {}).get('confidence_threshold', 0.7)
        self.ocr = None
        self._initialize_ocr()
        logger.info(f"HandwritingRecognizer initialized with {self.ocr_engine}")
    
    def _load_config(self, config_path: Optional[str] = None) -> dict:
        """Load configuration from JSON file or use defaults."""
        default_config = {
            "skill": "handwriting-recognition",
            "model": {
                "primary": "paddleocr",
                "fallback": "pytesseract"
            },
            "processing": {
                "image_preprocessing": True,
                "grayscale_conversion": True,
                "threshold_adjustment": True,
                "dpi_optimization": 300
            },
            "output": {
                "confidence_threshold": 0.7,
                "return_confidence": True,
                "return_bounding_boxes": False
            }
        }
        
        if config_path and Path(config_path).exists():
            try:
                with open(config_path, 'r') as f:
                    user_config = json.load(f)
                    default_config.update(user_config)
                    logger.info(f"Config loaded from {config_path}")
            except Exception as e:
                logger.warning(f"Failed to load config from {config_path}: {e}")
        
        return default_config
    
    def _initialize_ocr(self):
        """Initialize the OCR engine."""
        try:
            if self.ocr_engine == "paddleocr":
                try:
                    from paddleocr import PaddleOCR
                    self.ocr = PaddleOCR(
                        use_angle_cls=True,
                        lang='en',
                        use_gpu=False
                    )
                    logger.info("PaddleOCR initialized successfully")
                except ImportError:
                    logger.warning("PaddleOCR not installed, falling back to pytesseract")
                    self._initialize_pytesseract()
            else:
                self._initialize_pytesseract()
        except Exception as e:
            logger.error(f"OCR initialization failed: {e}")
            raise
    
    def _initialize_pytesseract(self):
        """Initialize pytesseract as fallback."""
        try:
            import pytesseract
            self.ocr = pytesseract
            self.ocr_engine = "pytesseract"
            logger.info("Pytesseract initialized as fallback")
        except ImportError:
            logger.error("Neither PaddleOCR nor Pytesseract is available")
            raise
    
    def recognize(
        self,
        image_path: Union[str, Path],
        language: str = "en",
        confidence_threshold: Optional[float] = None,
        preprocess: bool = True
    ) -> Dict:
        """
        Recognize handwritten text from an image.
        
        Args:
            image_path (str or Path): Path to the image file
            language (str): ISO 639-1 language code (default: "en")
            confidence_threshold (float, optional): Override default threshold
            preprocess (bool): Apply preprocessing to image
        
        Returns:
            dict: Recognition results with text and confidence
        """
        start_time = datetime.now()
        
        try:
            # Validate image path
            image_path = Path(image_path)
            if not image_path.exists():
                return {
                    "status": "error",
                    "message": f"Image file not found: {image_path}",
                    "processing_time": 0
                }
            
            # Load and preprocess image
            image = cv2.imread(str(image_path))
            if image is None:
                return {
                    "status": "error",
                    "message": f"Failed to load image: {image_path}",
                    "processing_time": 0
                }
            
            if preprocess and self.config.get('processing', {}).get('image_preprocessing'):
                from .utils import PreprocessingPipeline
                preprocessor = PreprocessingPipeline(self.config)
                image = preprocessor.preprocess(image)
            
            # Run OCR
            results = self._run_ocr(image)
            
            # Format results
            threshold = confidence_threshold or self.confidence_threshold
            formatted_results = self._format_results(results, image, image_path, threshold)
            
            # Calculate processing time
            processing_time = (datetime.now() - start_time).total_seconds()
            formatted_results['processing_time'] = processing_time
            
            logger.info(f"Recognition completed for {image_path} in {processing_time:.3f}s")
            
            return formatted_results
        
        except Exception as e:
            logger.error(f"Recognition failed for {image_path}: {e}")
            return {
                "status": "error",
                "message": str(e),
                "processing_time": (datetime.now() - start_time).total_seconds()
            }
    
    def _run_ocr(self, image) -> List:
        """Run OCR on the image."""
        if self.ocr_engine == "paddleocr" and self.ocr:
            return self.ocr.ocr(image, cls=True)
        else:
            # Fallback to pytesseract
            import pytesseract
            from PIL import Image
            import numpy as np
            pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            text = pytesseract.image_to_string(pil_image)
            return [[[(0, 0), text, 0.9]]]  # Format to match PaddleOCR
    
    def _format_results(self, results: List, image, image_path: Path, threshold: float) -> Dict:
        """Format OCR results into standardized output."""
        text_list = []
        detailed_results = []
        confidences = []
        
        if not results or not results[0]:
            return {
                "status": "success",
                "recognized_text": "",
                "confidence": 0.0,
                "language": "en",
                "detailed_results": [],
                "metadata": {
                    "image_size": {"width": image.shape[1], "height": image.shape[0]},
                    "model_used": self.ocr_engine,
                    "preprocessing_applied": ["grayscale", "threshold"] if self.config.get('processing', {}).get('image_preprocessing') else [],
                    "image_path": str(image_path)
                }
            }
        
        for line in results:
            for word_info in line:
                if len(word_info) >= 3:
                    text = word_info[1]
                    confidence = float(word_info[2])
                    
                    if confidence >= threshold:
                        text_list.append(text)
                        confidences.append(confidence)
                        
                        detailed_results.append({
                            "text": text,
                            "confidence": confidence,
                            "position": {
                                "x": int(word_info[0][0][0]) if word_info[0] else 0,
                                "y": int(word_info[0][0][1]) if word_info[0] else 0
                            }
                        })
        
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0
        
        return {
            "status": "success",
            "recognized_text": " ".join(text_list),
            "confidence": round(avg_confidence, 4),
            "language": "en",
            "detailed_results": detailed_results,
            "metadata": {
                "image_size": {"width": image.shape[1], "height": image.shape[0]},
                "model_used": self.ocr_engine,
                "preprocessing_applied": ["grayscale", "threshold"] if self.config.get('processing', {}).get('image_preprocessing') else [],
                "image_path": str(image_path)
            }
        }
    
    def recognize_batch(
        self,
        image_paths: List[Union[str, Path]],
        **kwargs
    ) -> List[Dict]:
        """
        Recognize text from multiple images.
        
        Args:
            image_paths (list): List of paths to image files
            **kwargs: Additional arguments to pass to recognize()
        
        Returns:
            list: List of recognition results
        """
        results = []
        for image_path in image_paths:
            result = self.recognize(image_path, **kwargs)
            results.append(result)
        
        logger.info(f"Batch processing completed for {len(image_paths)} images")
        return results
