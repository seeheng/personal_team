"""
Handwriting Recognition Skill Module

This module provides handwriting recognition capabilities for the personal assistant agent.
It uses PaddleOCR as the primary recognition engine with fallback to Tesseract.
"""

import logging
from .recognizer import HandwritingRecognizer
from .trainer import HandwritingTrainer
from .utils import PreprocessingPipeline

__version__ = "1.0.0"
__all__ = ["HandwritingRecognizer", "HandwritingTrainer", "PreprocessingPipeline"]

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

logger.info(f"Handwriting Recognition Skill v{__version__} initialized")
