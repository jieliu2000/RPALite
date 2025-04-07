import cv2
import numpy as np
from typing import List, Tuple, Optional
import logging
import math
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
        try:
            if self.debug_mode:
                cv2.imshow('shapes', np.array(parentImage)) 
                cv2.waitKey(self.debug_image_show_milliseconds)
                cv2.destroyAllWindows()

            gray = cv2.cvtColor(np.array(parentImage), cv2.COLOR_BGR2GRAY)
            
            target = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)
            
            # Use template matching to find the location of the image in the parent image
            result = cv2.matchTemplate(gray, target, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            top_left = max_loc
                
            # Get the size of the image
            image_size = image.size
            
            # Return the rectangle representing the location of the image in the parent image
            return (top_left[0], top_left[1], image_size[0], image_size[1])
        except Exception as e:
            logger.error(f"Error in find_image_location: {e}")
            return None
        finally:
            if self.debug_mode:
                cv2.destroyAllWindows()

    def find_all_image_locations(self, image, parentImage):
        if parentImage is None or image is None:
            return None
        # Find the location of the image in the parent image
        try:
            if self.debug_mode:
                cv2.imshow('shapes', np.array(parentImage)) 
                cv2.waitKey(self.debug_image_show_milliseconds)
                cv2.destroyAllWindows()

            gray = cv2.cvtColor(np.array(parentImage), cv2.COLOR_BGR2GRAY)
            
            target = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)
            
            # Use template matching to find the location of the image in the parent image
            result = cv2.matchTemplate(gray, target, cv2.TM_CCOEFF_NORMED)
            
            # find all the image locations in the parent image
            locations = np.where(result >= 0.9)
            h, w = target.shape

            # Sort and convert the locations to a list of tuples including height and width
            sorted_locations = sorted([(pt[0], pt[1], w, h) for pt in zip(*locations[::-1])], key=lambda y: y[1])

            return sorted_locations
        except Exception as e:
            logger.error(f"Error in find_all_image_locations: {e}")
            return None
        finally:
            if self.debug_mode:
                cv2.destroyAllWindows()
        
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
        try:
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
        except Exception as e:
            logger.error(f"Error in read_text: {e}")
            return None

    def find_texts_in_rects(self, image, text, filter_args_in_parent=None, rects=None):
        '''
        Returns the location information list, format is ((top_x, top_y, width, height), text) of the text in the image.
        '''
        if rects == None:
            return self.find_texts_in_image(image, text, filter_args_in_parent)
        
        if type(rects) == list and len(rects) > 0:    
            arr = self.read_text(image)
            if arr is None:
                return None
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
        if text_arr is None:
            return None
            
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

        if len(results) == 0:
            return None
        results = sorted(results, key=lambda l: l[2], reverse=True)
        return results


    def find_texts_in_image(self, image, text, filter_args_in_parent=None, rect=None):
        '''
        Returns the location information, format is (top_x, top_y, width, height) of the text in the image.
        If the text is not found, returns None.
        '''
        
        arr = self.read_text(image)
        
        return self.find_texts_in_array_and_rect(text, arr, image, filter_args_in_parent, rect)


    def validate_inside(self, outside, inside):
        # Check if the rectangle is inside the target rectangle. Paramete rect and target's formats are (x, y, width, height)
        return outside[0] <= inside[0] and outside[1] <= inside[1] and outside[0] + outside[2] >= inside[0] + inside[2] and outside[1] + outside[3] >= inside[1] + inside[3]

    def find_rects_outside_position(self, image, target):
        if target is None:
            return None
            
        try:
            img = np.array(image)
            # converting image into grayscale image 
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
          
            # setting threshold of gray image 
            edged = cv2.Canny(gray, 50, 200, apertureSize = 5) 

            # using a findContours() function 
            contours, _ = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
            
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
                img_copy = img.copy()
                cv2.drawContours(img_copy, approx_list, -1, (255, 0, 0), 1)
                cv2.imshow('target', img_copy) 
                cv2.waitKey(self.debug_image_show_milliseconds)
                cv2.destroyAllWindows()
                
            return targets
        except Exception as e:
            logger.error(f"Error in find_rects_outside_position: {e}")
            return None
        finally:
            if self.debug_mode:
                cv2.destroyAllWindows()
    

    def find_window_outside_position(self, image, target):
        if target is None:
            return None
            
        try:
            img = np.array(image)
            # converting image into grayscale image 
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
          
            # setting threshold of gray image 
            edged = cv2.Canny(gray, 50, 200, apertureSize = 5) 

            # using a findContours() function 
            contours, _ = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
            
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
                img_copy = img.copy()
                cv2.drawContours(img_copy, [target_information[0]], -1, (255, 0, 0), 1)
                cv2.imshow('target', img_copy) 
                cv2.waitKey(self.debug_image_show_milliseconds)
                cv2.destroyAllWindows()
       
            return target_information[1]
        except Exception as e:
            logger.error(f"Error in find_window_outside_position: {e}")
            return None
        finally:
            if self.debug_mode:
                cv2.destroyAllWindows()
    
    def find_texts_inside_rect(self, image, target_text, rect):
        if rect is None:
            return None
            
        try:
            text_arr = self.read_text(image)
            if text_arr is None:
                return None
                
            results = []
            (position, target_text) = None, None
            for r in text_arr:  
            
                if (rect is not None and self.check_point_inide_rect(r[0][0], rect) and self.check_point_inide_rect(r[0][2], rect)):
                    position = r[0]
                    target_text = r[1]
                    location = position[0][0], position[0][1], position[1][0]-position[0][0], position[3][1]-position[0][1]

                    results.append((location, target_text))

            if len(results) == 0:
                return None
            return results
        except Exception as e:
            logger.error(f"Error in find_texts_inside_rect: {e}")
            return None
    

    def find_window_near_position(self, image, target):
        return self.find_control_near_position(image, target)


    
    def find_control_near_position(self, image, target, left_or_top_label=False, text_label_match_ration=1.0):
        if target is None:
            return None
            
        try:
            img = np.array(image)
            # converting image into grayscale image 
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
          
            # setting threshold of gray image 
            edged = cv2.Canny(gray, 50, 150, apertureSize = 5) 
            # using a findContours() function 
            contours, _ = cv2.findContours(
                edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
            
            i = 0
            dist = 1000000
            a = 0
            target_information = None
            distance_threshold = 20
            
            # Use HoughLinesP to detect lines in the image, adjust parameters to detect isolated horizontal lines
            # Hough transform for line detection
            lines = cv2.HoughLinesP(edged, 1, np.pi/180, threshold=100, 
                                    minLineLength=50, maxLineGap=1)
      

            angle_threshold  = 10
            horizontal_lines = []
            other_lines = []
            
            if lines is not None:
                for line in lines:
                    x1, y1, x2, y2 = line[0]
                    dx = x2 - x1
                    dy = y2 - y1
                    if dx == 0 and dy == 0:
                        continue  # Ignore zero-length line segments
                    
                    # Calculate line angle (convert to 0-180 degrees)
                    angle = math.degrees(math.atan2(dy, dx)) % 180
                    
                    # Classify as horizontal line segments or other line segments
                    if (angle <= angle_threshold) or (angle >= 180 - angle_threshold):
                        if dx > 100:
                            horizontal_lines.append((x1, y1, x2, y2))
                    else:
                        other_lines.append((x1, y1, x2, y2))
        
            lines = horizontal_lines
            
           
            # Merge lines and contours into a single array and sort
            combined_elements = []
            if lines is not None:
                combined_elements.extend(('line', line) for line in lines)
            combined_elements.extend(('contour', c) for c in contours)
            
            # Unified sorting logic: Sort by y-coordinate in ascending order, for same y, rectangles come first, then by x-coordinate
            combined_elements.sort(key=lambda elem: (
                (elem[1][1] if elem[0] == 'line' else cv2.boundingRect(elem[1])[1]),  # y-coordinate
                1 if elem[0] == 'line' else 0,  # for same y-coordinate, rectangles come first
                elem[1][0] if elem[0] == 'line' else cv2.boundingRect(elem[1])[0]   # x-coordinate
            ))

            # Additional processing logic
            temp_contours = []
            current_y = None
            elements_to_remove = set()
            
            for i, elem in enumerate(combined_elements):
                elem_type, data = elem
                
                # Get y-coordinate of current element
                if elem_type == 'line':
                    y = data[1]  # Take y1 coordinate of the line
                else:
                    y = cv2.boundingRect(data)[1]
                    
                # If it's a contour
                if elem_type == 'contour':
                    if current_y is None or y != current_y:
                        # Start of a new row
                        current_y = y
                        temp_contours = [data]
                    else:
                        # Same row, add to temporary contours
                        temp_contours.append(data)
                        
                # If it's a line
                elif elem_type == 'line':
                    if y != current_y:
                        # Not in current row, skip
                        elements_to_remove.add(i)
                        continue
                        
                    # Check if it's contained by contours
                    x1, y1, x2, y2 = data
                    is_contained = False
                    for contour in temp_contours:
                        # Get contour boundaries
                        x, y, w, h = cv2.boundingRect(contour)
                        # Check if the line is inside the contour
                        if x <= x1 and x + w >= x2 and y <= y1 and y + h >= y2:
                            is_contained = True
                            break
                            
                    if is_contained:
                        elements_to_remove.add(i)
                        
            # Remove elements to exclude
            combined_elements = [elem for i, elem in enumerate(combined_elements) if i not in elements_to_remove]

            # Create image copy for display
            if self.debug_mode:
                display_image = img.copy()
                
                # Draw all detected lines
               
                for elem in combined_elements:
                    elem_type, data = elem
                    
                    # Get unified bounding box information
                    if elem_type == 'line':
                        # Generate rectangle area for line segments (simulate contour)
                        x1, y1, x2, y2 = data
                        # Draw line in red with width 1
                        cv2.line(display_image, (x1, y1), (x2, y2), (0, 0, 255), 1)
                
                cv2.imshow('Lines', display_image) 
                cv2.waitKey(self.debug_image_show_milliseconds)
                cv2.destroyAllWindows()


            for elem in combined_elements:
                elem_type, data = elem
                
                # Get unified bounding box information for elements
                if elem_type == 'line':
                    # Generate rectangle area for line segment (simulate contour)
                    x1, y1, x2, y2 = data
                    x, y, w, h = x1, y1 - 15, x2 - x1, 15
                    # Create simulated approximated contour (rectangle)
                    approx = np.array([[[x, y]], [[x + w, y]], [[x + w, y + h]], [[x, y + h]]], dtype=np.int32)
                else:  # contour
                    # Original contour processing logic
                    contour = data
                    perimeter = cv2.arcLength(contour, True)
                    approx = cv2.approxPolyDP(contour, 0.01 * perimeter, True)
                
                # Unified contour logic
                if len(approx) >= 4 and len(approx) <= 8:
                    x, y, w, h = cv2.boundingRect(approx)
                else:
                    continue

                if h < 10 or w < 10:
                    continue

                # Unified area relationship judgment
                target_area = target[2] * target[3]
                rect_area = w * h
                
                if target_area > rect_area:
                    rect_in_target = (x >= target[0] and y >= target[1] and 
                                    x + w <= target[0] + target[2] and 
                                    y + h <= target[1] + target[3])
                    if rect_in_target:
                        continue
                
                # Unified position relationship check
                target_in_rect = (target[0] >= x and target[1] >= y and
                                target[0] + target[2] <= x + w and
                                target[1] + target[3] <= y + h)
                
                if target_in_rect and abs(w - target[2]) < 40:
                    continue

                # Unified distance calculation (using contour method)
                dist_to_left_bottom = abs(cv2.pointPolygonTest(approx, (float(target[0]), float(target[1]+target[3])), True))
                dist_to_right_bottom = abs(cv2.pointPolygonTest(approx, (float(target[0]+target[2]), float(target[1]+target[3])), True))
                dist1 = min(dist_to_left_bottom, dist_to_right_bottom)

                # Unified weight adjustment logic
                multiple = 1

                if (abs(x - target[0]) < target[2] or abs(y - target[1]) < 50) and h/target[3] < 3:
                    multiple *= 0.5

                target_multiple = 1
                # Unified nested relationship check
                if target_information is not None:
                    current_control = target_information[1]
                    target_multiple = target_information[2]
                    if (x >= current_control[0] and y >= current_control[1] and 
                        x + w <= current_control[0] + current_control[2] and 
                        y + h <= current_control[1] + current_control[3]):
                        multiple_for_current_control = (w*h)/(current_control[2]*current_control[3])

                        if multiple_for_current_control < 0.3:
                            multiple_for_current_control = 0.5
                        elif multiple_for_current_control <= 0.85:
                            multiple_for_current_control = 0.85
                        else:
                            multiple_for_current_control = 1

                        multiple *= target_multiple * multiple_for_current_control
                                
                if (dist1 * multiple < dist * target_multiple) and ((not left_or_top_label) or (left_or_top_label and ((target[0] + target[2])/2 < x  or (target[1] + target[3])/2 < y ))):
                    dist = dist1 
                    target_information = (approx, (x, y, w, h), 0.5 if multiple <= 0.5 else 1)
                 
            # displaying the image after drawing contours 
            if(target_information is None):
                return None
                
            if self.debug_mode:
                img_copy = img.copy()
                cv2.drawContours(img_copy, [target_information[0]], -1, (0, 255, 0), 1)
                cv2.imshow('Targets', img_copy) 
                cv2.waitKey(self.debug_image_show_milliseconds)
                cv2.destroyAllWindows()
       
            return target_information[1]
        except Exception as e:
            logger.error(f"Error in find_control_near_position: {e}")
            return None
        finally:
            if self.debug_mode:
                cv2.destroyAllWindows()

