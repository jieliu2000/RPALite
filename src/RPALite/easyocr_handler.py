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
        
    def find_texts_in_image(self, image, text: str) -> Optional[List[Tuple[Tuple[int, int, int, int], str]]]:
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
            if self.debug_mode:
                logger.debug(f"EasyOCR results: {results}")
                
            matches = []
            for (bbox, text_recognized, prob) in results:
                if text.lower() in text_recognized.lower():
                    # Convert bbox to (x, y, width, height)
                    x_min = int(min(bbox[0][0], bbox[1][0], bbox[2][0], bbox[3][0]))
                    y_min = int(min(bbox[0][1], bbox[1][1], bbox[2][1], bbox[3][1]))
                    x_max = int(max(bbox[0][0], bbox[1][0], bbox[2][0], bbox[3][0]))
                    y_max = int(max(bbox[0][1], bbox[1][1], bbox[2][1], bbox[3][1]))
                    matches.append(((x_min, y_min, x_max - x_min, y_max - y_min), text_recognized))
                    
            return matches if matches else None
            
        except Exception as e:
            logger.error(f"Error in EasyOCR text recognition: {e}")
            return None 