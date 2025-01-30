import easyocr
import numpy as np
from typing import List, Tuple, Optional
import logging

logger = logging.getLogger(__name__)

class EasyOCRHandler:
    def __init__(self, languages: List[str] = ['en'], debug_mode: bool = False):
        self.languages = languages
        self.debug_mode = debug_mode
        self.reader = easyocr.Reader(self.languages)
        
    def find_texts_in_image(self, image):
        """
        Find text locations in an image using EasyOCR.
        
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
            results = self.reader.readtext(img_array)
            return results
            if self.debug_mode:
                logger.debug(f"EasyOCR results: {results}")
                
                
        except Exception as e:
            logger.error(f"Error in EasyOCR text recognition: {e}")
            return None 