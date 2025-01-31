import cv2
from paddleocr import PaddleOCR
import numpy as np
from typing import List, Tuple, Optional
import logging

logger = logging.getLogger(__name__)

class PaddleOCRHandler:
    def __init__(self, languages: List[str] = ['en'], debug_mode: bool = False, confidence_threshold: float = 0.5):
        """
        Initialize PaddleOCR handler.
        
        Args:
            languages: List of languages to recognize (default: ['en'])
            debug_mode: Whether to enable debug mode (default: False)
        """
        self.languages = languages
        self.debug_mode = debug_mode
        self.confidence_threshold = confidence_threshold
        # Initialize PaddleOCR with specified languages
        self.ocr = PaddleOCR(lang='en', show_log=debug_mode)
        
    def find_texts_in_image(self, image):
        """
        Find text locations in an image using PaddleOCR.
        
        Args:
            image: PIL Image or numpy array
            text: Text to search for
            
        Returns:
            A list of tuples where each tuple contains:
            - A bounding box tuple (x, y, width, height) representing the text location
            - The recognized text string that contains the search text
            Returns None if:
            - The input image is invalid
            - No text is found that contains the search text
            - An error occurs during OCR processing
        """
        if isinstance(image, np.ndarray):
            img_array = image
        else:
            img_array = np.array(image)
            
        try:     
            # Perform OCR using PaddleOCR
            ocr_results = self.ocr.ocr(img_array, cls=True)
            
            if self.debug_mode:
                logger.debug(f"PaddleOCR results: {ocr_results}")
                
            results = []
            for line in ocr_results[0]:
                if line and len(line) >= 2:
                    bbox = line[0]
                    text_recognized = line[1][0]
                    confidence = line[1][1]
                    # filter out low confidence results
                    if confidence < self.confidence_threshold:
                        continue
                    results.append((bbox, text_recognized, confidence))
                    
            return results if results else None
            
        except Exception as e:
            logger.error(f"Error in PaddleOCR text recognition: {e}")
            return None
