"""
Utility functions for handwriting recognition

Includes image preprocessing, data validation, and helper functions.
"""

import cv2
import numpy as np
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class PreprocessingPipeline:
    """Handles image preprocessing for optimal OCR results."""
    
    def __init__(self, config: Dict):
        """Initialize preprocessing pipeline with configuration."""
        self.config = config
        self.processing_config = config.get('processing', {})
    
    def preprocess(self, image: np.ndarray) -> np.ndarray:
        """
        Apply preprocessing pipeline to image.
        
        Args:
            image (np.ndarray): Input image
        
        Returns:
            np.ndarray: Preprocessed image
        """
        if image is None:
            return None
        
        # Convert to grayscale if configured
        if self.processing_config.get('grayscale_conversion', True):
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply denoising
        image = cv2.medianBlur(image, 5)
        
        # Apply thresholding if configured
        if self.processing_config.get('threshold_adjustment', True):
            image = self._adaptive_threshold(image)
        
        # Upscale if needed
        dpi = self.processing_config.get('dpi_optimization', 300)
        image = self._upscale_image(image, dpi)
        
        logger.debug("Image preprocessing completed")
        return image
    
    def _adaptive_threshold(self, image: np.ndarray) -> np.ndarray:
        """Apply adaptive thresholding for better text extraction."""
        # Use Otsu's method for automatic threshold calculation
        _, binary = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return binary
    
    def _upscale_image(self, image: np.ndarray, target_dpi: int = 300) -> np.ndarray:
        """Upscale image if resolution is too low."""
        height, width = image.shape[:2]
        
        # If image is small, upscale it
        if height < 150 or width < 150:
            scale = max(1, 300 / min(height, width))
            new_height = int(height * scale)
            new_width = int(width * scale)
            image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
            logger.debug(f"Image upscaled from {width}x{height} to {new_width}x{new_height}")
        
        return image


class DataValidation:
    """Validation utilities for input data."""
    
    @staticmethod
    def validate_image_path(path: str) -> bool:
        """Validate if image path is valid and supported."""
        from pathlib import Path
        
        supported_formats = {'.jpg', '.jpeg', '.png', '.bmp', '.webp', '.tiff'}
        path_obj = Path(path)
        
        return path_obj.exists() and path_obj.suffix.lower() in supported_formats
    
    @staticmethod
    def validate_language_code(lang_code: str) -> bool:
        """Validate if language code is valid ISO 639-1 code."""
        valid_codes = {'en', 'es', 'fr', 'de', 'it', 'pt', 'ru', 'ja', 'zh', 'ar', 'ko'}
        return lang_code.lower() in valid_codes


class MetricsCalculator:
    """Calculate performance metrics for recognition."""
    
    @staticmethod
    def calculate_accuracy(predicted_text: str, ground_truth: str) -> float:
        """
        Calculate character-level accuracy.
        
        Args:
            predicted_text (str): OCR predicted text
            ground_truth (str): Correct text
        
        Returns:
            float: Accuracy score (0-1)
        """
        if len(ground_truth) == 0:
            return 1.0 if len(predicted_text) == 0 else 0.0
        
        matches = sum(c1 == c2 for c1, c2 in zip(predicted_text, ground_truth))
        return matches / len(ground_truth)
    
    @staticmethod
    def calculate_wer(predicted_text: str, ground_truth: str) -> float:
        """
        Calculate Word Error Rate.
        
        Args:
            predicted_text (str): OCR predicted text
            ground_truth (str): Correct text
        
        Returns:
            float: WER score
        """
        pred_words = predicted_text.split()
        truth_words = ground_truth.split()
        
        if len(truth_words) == 0:
            return 0.0 if len(pred_words) == 0 else float('inf')
        
        # Simple edit distance calculation
        from difflib import SequenceMatcher
        matcher = SequenceMatcher(None, pred_words, truth_words)
        matching_words = sum(block.size for block in matcher.get_matching_blocks())
        
        errors = len(truth_words) - matching_words
        return errors / len(truth_words)


def log_recognition_result(image_path: str, result: Dict):
    """Log recognition result for debugging."""
    if result['status'] == 'success':
        logger.info(
            f"Recognition successful: {image_path} | "
            f"Confidence: {result['confidence']:.2%} | "
            f"Time: {result['processing_time']:.3f}s"
        )
    else:
        logger.error(f"Recognition failed for {image_path}: {result['message']}")
