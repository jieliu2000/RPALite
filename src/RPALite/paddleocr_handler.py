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
        
        # Initialize multiple PaddleOCR instances based on languages
        self.ocr_instances = []
        
        # Check if we have both English and other languages
        has_english = 'en' in languages
        has_other_languages = len(languages) > 1 or (len(languages) == 1 and languages[0] != 'en')
        
        for lang in languages:
            # Skip English initialization if we have other languages
            if lang == 'en' and has_other_languages:
                continue
                
            # Only initialize unique language instances
            if lang not in [ocr.lang for ocr in self.ocr_instances]:
                ocr = PaddleOCR(lang=lang, show_log=debug_mode)
                self.ocr_instances.append(ocr)
        
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
            all_results = []
            
            # Process image with each OCR instance
            for ocr in self.ocr_instances:
                ocr_results = ocr.ocr(img_array, cls=True)
                
                if self.debug_mode:
                    logger.debug(f"PaddleOCR results for {ocr.lang}: {ocr_results}")
                
                # Process results from this OCR instance
                if ocr_results and ocr_results[0]:
                    for line in ocr_results[0]:
                        if line and len(line) >= 2:
                            bbox = line[0]
                            text_recognized = line[1][0]
                            confidence = line[1][1]
                            
                            # Filter out low confidence results
                            if confidence >= self.confidence_threshold:
                                all_results.append((bbox, text_recognized, confidence))
            
            # Remove duplicate results (same text and similar bounding box)
            unique_results = self._remove_duplicate_results(all_results)
            
            return unique_results if unique_results else None
            
        except Exception as e:
            logger.error(f"Error in PaddleOCR text recognition: {e}")
            return None

    def _is_similar_bbox(self, bbox1, bbox2, threshold=5):
        """
        Check if two bounding boxes are similar within a given threshold.
        
        Args:
            bbox1: First bounding box [(x1,y1), (x2,y2), (x3,y3), (x4,y4)]
            bbox2: Second bounding box [(x1,y1), (x2,y2), (x3,y3), (x4,y4)]
            threshold: Maximum allowed difference in coordinates
            
        Returns:
            True if bounding boxes are similar, False otherwise
        """
        for p1, p2 in zip(bbox1, bbox2):
            if abs(p1[0] - p2[0]) > threshold or abs(p1[1] - p2[1]) > threshold:
                return False
        return True

    def _remove_duplicate_results(self, results):
        """
        Remove duplicate OCR results based on text and bounding box similarity.
        Keep only the result with highest confidence for similar text and bounding boxes.
        
        Args:
            results: List of OCR results
            
        Returns:
            List of unique OCR results
        """
        unique_results = []
        
        for new_result in results:
            new_bbox, new_text, new_confidence = new_result
            # Normalize text for comparison
            normalized_text = new_text.strip().lower()
            
            found_similar = False
            for i, existing_result in enumerate(unique_results):
                existing_bbox, existing_text, existing_confidence = existing_result
                
                # Check if text is the same and bounding boxes are similar
                if normalized_text == existing_text.strip().lower() and \
                   self._is_similar_bbox(new_bbox, existing_bbox):
                    # Keep the result with higher confidence
                    if new_confidence > existing_confidence:
                        unique_results[i] = new_result
                    found_similar = True
                    break
            
            if not found_similar:
                unique_results.append(new_result)
        
        return unique_results
