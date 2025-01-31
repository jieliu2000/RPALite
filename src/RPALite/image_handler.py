import cv2
import numpy as np
from typing import List, Tuple, Optional
import logging
from difflib import SequenceMatcher

logger = logging.getLogger(__name__)

class ImageHandler:
    def __init__(self, debug_mode: bool = False, ocr_engine: str = "paddleocr", languages: List[str] = ['en'], debug_image_show_seconds=5):
        '''
        Initialize the ImageHandler class. This class use EasyOCR for text OCR. About language codes please check https://www.jaided.ai/easyocr/'''
        self.debug_mode = debug_mode
        self.languages = languages
        self.debug_image_show_milliseconds = debug_image_show_seconds * 1000
        # Initialize OCR handler based on selected engine
        if ocr_engine.lower() == "paddleocr":
            from .paddleocr_handler import PaddleOCRHandler
            self.ocr_handler = PaddleOCRHandler(languages, debug_mode)
        else:
            from .easyocr_handler import EasyOCRHandler
            self.ocr_handler = EasyOCRHandler(languages, debug_mode)
        pass
    
    def check_point_inide_rect(self, point, rect):
        '''Check if a point is in a rect. The point's coordinates are (x, y). The rect's coordinates are (x, y, width, height).'''
        if point is None or rect is None:
            return False
        # If the point is inside the rectangle
        return rect[0] <= point[0] and rect[1] <= point[1] and rect[0] + rect[2] >= point[0] and rect[1] + rect[3] >= point[1]

    def check_point_inide_rects(self, point, rects):
        '''Check if a point is in the rects list. The point's coordinates are (x, y). The rects's coordinates are (x, y, width, height).'''
        if point is None or rects is None or len(rects) == 0:
            return False
        
        for rect in rects:
            if self.check_point_inide_rect(point, rect):
                return True
        return False
        
    
    def find_image_location(self, image, parentImage):
        if parentImage is None or image is None:
            return None
        # Find the location of the image in the parent image
        if self.debug_mode:
            cv2.imshow('shapes', np.array(parentImage)) 
            cv2.waitKey(self.debug_image_show_milliseconds)

        gray = cv2.cvtColor(np.array(parentImage), cv2.COLOR_BGR2GRAY)
        
        target = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)
        
        # Use template matching to find the location of the image in the parent image
        # result = cv2.matchTemplate(gray, target, cv2.TM_CCOEFF_NORMED)
        result = cv2.matchTemplate(gray, target, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        top_left = max_loc
            
        # Get the size of the image
        image_size = image.size
        
        # Return the rectangle representing the location of the image in the parent image
        return (top_left[0], top_left[1], image_size[0], image_size[1]) 

        pass

    def find_all_image_locations(self, image, parentImage):
        if parentImage is None or image is None:
            return None
        # Find the location of the image in the parent image
        if self.debug_mode:
            cv2.imshow('shapes', np.array(parentImage)) 
            cv2.waitKey(self.debug_image_show_milliseconds)

        gray = cv2.cvtColor(np.array(parentImage), cv2.COLOR_BGR2GRAY)
        
        target = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)
        
        # Use template matching to find the location of the image in the parent image
        # result = cv2.matchTemplate(gray, target, cv2.TM_CCOEFF_NORMED)
        result = cv2.matchTemplate(gray, target, cv2.TM_CCOEFF_NORMED)
        
        # find all the image locations in the parent image
        locations = np.where(result >= 0.9)
        h, w = target.shape

        # Sort and convert the locations to a list of tuples including height and width
        sorted_locations = sorted([(pt[0], pt[1], w, h) for pt in zip(*locations[::-1])], key=lambda y: y[1])

        return sorted_locations
        
    def find_text_in_array(self, text, arrays, windows):
        '''
        Returns the location information, format is (top_x, top_y, width, height) of the text. This function will first iterate over the arrays, find matched text and check it is in the window. If the matched text is in the window, the function will return the text location. If no matched text found returns None.
        '''
        for r in arrays:
            if text in r[1] and self.check_point_inide_rects(r[0][0], windows):
                return r[0][0]        
        return None
    

    def check_text_and_filter_in_window(self, image, arrays, position, text, filter_args_in_parent, rect=None):
        if filter_args_in_parent is None:
            return True
        windows = self.find_rects_outside_position(image, (position[0][0], position[0][1], position[1][0] - position[0][0], position[2][1] - position[0][1]))
        if windows is None or len(windows) == 0:
            return False
        
        for filter_text in filter_args_in_parent:
            location = self.find_text_in_array(filter_text, arrays, windows)
            if location is not None:
                return True
        return False
    


    def read_text(self, image):
        
        img_array = np.array(image)
        
        cv_image = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)        
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        
        blurred = cv2.GaussianBlur(gray, (3, 3), 0)
        
        low_contrast_mask = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                                cv2.THRESH_BINARY_INV, 11, 2)
        
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        enhanced_borders = cv2.morphologyEx(low_contrast_mask, cv2.MORPH_CLOSE, kernel)
        
        enhanced_borders = cv2.cvtColor(enhanced_borders, cv2.COLOR_GRAY2BGR)
        enhanced_borders = cv2.GaussianBlur(enhanced_borders, (3, 3), 0)
        img_array = cv2.addWeighted(cv_image, 0.9, enhanced_borders, 0.1, 0)

        arr = self.ocr_handler.find_texts_in_image(image)
        return arr

    def find_texts_in_rects(self, image, text, filter_args_in_parent=None, rects=None):
        '''
        Returns the location information list, format is ((top_x, top_y, width, height), text) of the text in the image.
        '''
        if rects == None:
            return self.find_texts_in_image(image, text, filter_args_in_parent)
        
        if type(rects) == list and len(rects) > 0:    
            arr = self.read_text(image)        
            for rect in rects:
                loc = self.find_texts_in_array_and_rect(text, arr, image, filter_args_in_parent, rect)
                if loc is not None:
                    return loc  
        else:
            return self.find_texts_in_image(image, text, filter_args_in_parent, rects)
  
      
        
    def find_texts_in_array_and_rect(self, text, text_arr, image, filter_args_in_parent=None, rect = None):
        '''
        Returns the location information, format is (top_x, top_y, width, height, ratio) of the text in the image.
        '''
        results = []
        (position, target_text, best_ratio) = None, None, 0
        for r in text_arr:  
            ratio = SequenceMatcher(None, r[1], text).ratio()
            if  text in r[1]: 
                if ((rect is not None and self.check_point_inide_rect(r[0][0], rect)) or rect is None) and self.check_text_and_filter_in_window(image, text_arr, r[0], r[1], filter_args_in_parent, rect): 
                    position = r[0]
                    target_text = r[1]
                    location = position[0][0], position[0][1], position[1][0]-position[0][0], position[3][1]-position[0][1]

                    results.append( (location, target_text, 1))

            elif ratio > best_ratio and ratio > 0.75 and ((rect is not None and self.check_point_inide_rect(r[0][0], rect)) or rect is None) and self.check_text_and_filter_in_window(image, text_arr, r[0], r[1], filter_args_in_parent, rect):
                best_ratio = ratio
                target_text = r[1]
                position = r[0]
                
                location = position[0][0], position[0][1], position[1][0]-position[0][0], position[3][1]-position[0][1]

                results.append((location, target_text, ratio))
        #cv2.destroyAllWindows()

        if len(results) == 0:
            return None
        results = sorted(results, key=lambda l: l[2], reverse=True)
        return results


    def find_texts_in_image(self, image, text, filter_args_in_parent=None, rect=None):
        '''
        Returns the location information, format is (top_x, top_y, width, height) of the text in the image.
        If the text is not found, returns None.
        '''
        if self.debug_mode:
            cv2.imshow('shapes', np.array(image)) 
            cv2.waitKey(0)
        
        arr = self.read_text(image)
        
        return self.find_texts_in_array_and_rect(text, arr, image, filter_args_in_parent, rect)


    def validate_inside(self, outside, inside):
        # Check if the rectangle is inside the target rectangle. Paramete rect and target's formats are (x, y, width, height)
        return outside[0] <= inside[0] and outside[1] <= inside[1] and outside[0] + outside[2] >= inside[0] + inside[2] and outside[1] + outside[3] >= inside[1] + inside[3]

    def find_rects_outside_position(self, image, target):
        img = np.array(image)
        # converting image into grayscale image 
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
      
        # setting threshold of gray image 
        edged = cv2.Canny(gray, 50, 200, apertureSize = 5) 

        # using a findContours() function 
        contours, _ = cv2.findContours( edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
        
        targets = []
        approx_list = []
       
        # list for storing names of shapes 
        for contour in contours: 
            # Approximate contour to a polygon
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.01 * perimeter, True)

            # Calculate aspect ratio and bounding box
            if len(approx) >= 4:
                x, y, w, h = cv2.boundingRect(approx)

                if(h<10 or w<10):
                    #ignore too small shapes
                    continue
        
                if(self.validate_inside((x, y, w, h), target)):
                    approx_list.append(approx)
                    targets.append((x, y, w, h))

        
        if(targets is None or len(targets)==0):
            return None
        if self.debug_mode:
            cv2.drawContours(img, approx_list, -1, (255, 0, 0), 1)
            cv2.imshow('target', img) 
            cv2.waitKey(self.debug_image_show_milliseconds)
        return targets
    

    def find_window_outside_position(self, image, target):
        img = np.array(image)
        # converting image into grayscale image 
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
      
        # setting threshold of gray image 
        edged = cv2.Canny(gray, 50, 200, apertureSize = 5) 

        # using a findContours() function 
        contours, _ = cv2.findContours( edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
        
        i = 0
        dist = 1000000
        a = 0
        target_information = None

        if self.debug_mode:
                cv2.drawContours(img, contours, -1, (0, 255, 0), 1)  
                cv2.imshow('shapes', img) 
                cv2.waitKey(0)
        # list for storing names of shapes 
        for contour in contours: 
            # Approximate contour to a polygon
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.01 * perimeter, True)

            # Calculate aspect ratio and bounding box
            if len(approx) >= 4:
                x, y, w, h = cv2.boundingRect(approx)

                if(h<10 or w<10):
                    #ignore too small shapes
                    continue

                dist1 = abs(cv2.pointPolygonTest(contour,(float(target[0]), float(target[1])),True))
        
                if(self.validate_inside((x, y, w, h), target) and dist1 < dist):
                    dist = dist1
                    target_information = approx, (x, y, w, h)
        
        if(target_information is None):
            return None
        if self.debug_mode:
            cv2.drawContours(img, [target_information[0]], -1, (255, 0, 0), 1)
            cv2.imshow('target', img) 
            cv2.waitKey(self.debug_image_show_milliseconds)
   
        return target_information[1]
    
    def find_texts_inside_rect(self, image, target_text, rect):
        if self.debug_mode:
                    cv2.imshow('shapes', np.array(image)) 
                    cv2.waitKey(0)
        
        text_arr = self.read_text(image)
        results = []
        (position, target_text) = None, None
        for r in text_arr:  
        
            if (rect is not None and self.check_point_inide_rect(r[0][0], rect)  and self.check_point_inide_rect(r[0][2], rect)) :
                position = r[0]
                target_text = r[1]
                location = position[0][0], position[0][1], position[1][0]-position[0][0], position[3][1]-position[0][1]

                results.append( (location, target_text))

          
        #cv2.destroyAllWindows()

        if len(results) == 0:
            return None
        return results
    

    def find_window_near_position(self, image, target):
        return self.find_control_near_position(image, target)

    def find_control_near_position(self, image, target, left_or_top_label = False):
        img = np.array(image)
        # converting image into grayscale image 
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
      
        # setting threshold of gray image 
        edged = cv2.Canny(gray, 50, 200, apertureSize = 5) 

        # using a findContours() function 
        contours, _ = cv2.findContours( 
            edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
        
        i = 0
        dist = 1000000
        a = 0
        target_information = None
        # list for storing names of shapes 
        for contour in contours: 
            # Approximate contour to a polygon
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.01 * perimeter, True)

            # Calculate aspect ratio and bounding box
            if len(approx) == 4:
                x, y, w, h = cv2.boundingRect(approx)

                if(h<10 and w<10):
                    #ignore too small shapes
                    continue

                dist_to_left_bottom = abs(cv2.pointPolygonTest(contour,(float(target[0]), float(target[1]+target[3])),True))
                dist_to_right_bottom = abs(cv2.pointPolygonTest(contour,(float(target[0]+target[2]), float(target[1]+target[3])),True))

                dist1 = dist_to_left_bottom 
                if dist_to_right_bottom < dist1:
                    dist1 = dist_to_right_bottom

                if(dist1 < dist) and ((left_or_top_label == False) or (left_or_top_label and ((target[0] + target[2])/2 < x  or (target[1] + target[3])/2 < y ))):
                    dist = dist1
                    target_information = approx, (x, y, w, h)
        # displaying the image after drawing contours 
        if(target_information is None):
            return None
        if self.debug_mode:
            cv2.drawContours(img, [target_information[0]], -1, (0, 255, 0), 1)
            cv2.imshow('shapes', img) 
            cv2.waitKey(self.debug_image_show_milliseconds)
   
        return target_information[1]
    