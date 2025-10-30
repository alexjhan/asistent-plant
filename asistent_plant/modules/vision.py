"""
Computer Vision Module
Analyzes screen content and detects UI elements
"""

import cv2
import numpy as np
from PIL import Image
from typing import Dict, List, Optional, Tuple

try:
    import pytesseract
    PYTESSERACT_AVAILABLE = True
except ImportError:
    PYTESSERACT_AVAILABLE = False
    print("Warning: pytesseract not available. OCR features will be limited.")

try:
    import mss
    MSS_AVAILABLE = True
except ImportError:
    MSS_AVAILABLE = False
    print("Warning: mss not available. Screen capture will use fallback.")


class VisionModule:
    """
    Computer vision module for screen analysis and element detection.
    """

    def __init__(self):
        """Initialize the vision module."""
        if MSS_AVAILABLE:
            self.sct = mss.mss()
        else:
            self.sct = None
        self.last_screenshot = None

    def capture_screen(self, region: Optional[Dict] = None) -> np.ndarray:
        """
        Capture the screen or a region of it.
        
        Args:
            region: Optional dictionary with 'left', 'top', 'width', 'height'
            
        Returns:
            Screen capture as numpy array
        """
        if not MSS_AVAILABLE or self.sct is None:
            # Return dummy image for testing
            print("Warning: Screen capture not available")
            return np.zeros((100, 100, 3), dtype=np.uint8)
        
        if region is None:
            # Capture entire screen (primary monitor)
            monitor = self.sct.monitors[1]
        else:
            monitor = {
                'left': region.get('left', 0),
                'top': region.get('top', 0),
                'width': region['width'],
                'height': region['height']
            }
        
        screenshot = self.sct.grab(monitor)
        img = np.array(screenshot)
        # Convert BGRA to RGB
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)
        self.last_screenshot = img
        return img

    def find_text_on_screen(self, text: str, region: Optional[Dict] = None) -> List[Dict]:
        """
        Find text on the screen using OCR.
        
        Args:
            text: Text to search for
            region: Optional region to search in
            
        Returns:
            List of dictionaries with location and confidence
        """
        if not PYTESSERACT_AVAILABLE:
            print("Warning: OCR not available")
            return []
        
        img = self.capture_screen(region)
        
        # Use pytesseract to detect text
        data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
        
        results = []
        text_lower = text.lower()
        
        for i, word in enumerate(data['text']):
            if word and text_lower in word.lower():
                x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
                conf = data['conf'][i]
                
                results.append({
                    'text': word,
                    'x': x + w // 2,  # Center x
                    'y': y + h // 2,  # Center y
                    'width': w,
                    'height': h,
                    'confidence': conf
                })
        
        return results

    def find_button(self, button_text: str) -> Optional[Dict]:
        """
        Find a button by its text label.
        
        Args:
            button_text: Text on the button
            
        Returns:
            Dictionary with button location or None
        """
        results = self.find_text_on_screen(button_text)
        if results:
            # Return the first match with highest confidence
            return max(results, key=lambda x: x['confidence'])
        return None

    def find_image_on_screen(self, template_path: str, threshold: float = 0.8) -> List[Dict]:
        """
        Find an image template on the screen using template matching.
        
        Args:
            template_path: Path to the template image
            threshold: Matching threshold (0-1)
            
        Returns:
            List of matches with locations
        """
        screen = self.capture_screen()
        template = cv2.imread(template_path)
        
        if template is None:
            raise ValueError(f"Could not load template image: {template_path}")
        
        # Convert to grayscale for matching
        screen_gray = cv2.cvtColor(screen, cv2.COLOR_RGB2GRAY)
        template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        
        # Perform template matching
        result = cv2.matchTemplate(screen_gray, template_gray, cv2.TM_CCOEFF_NORMED)
        
        # Find all matches above threshold
        locations = np.where(result >= threshold)
        matches = []
        
        h, w = template_gray.shape
        for pt in zip(*locations[::-1]):
            matches.append({
                'x': pt[0] + w // 2,
                'y': pt[1] + h // 2,
                'width': w,
                'height': h,
                'confidence': result[pt[1], pt[0]]
            })
        
        return matches

    def detect_ui_elements(self, element_type: str = "all") -> List[Dict]:
        """
        Detect UI elements on the screen using edge detection and contours.
        
        Args:
            element_type: Type of elements to detect ('button', 'field', 'all')
            
        Returns:
            List of detected elements with locations
        """
        img = self.capture_screen()
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        
        # Apply edge detection
        edges = cv2.Canny(gray, 50, 150)
        
        # Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        elements = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            
            # Filter by size (ignore very small elements)
            if w > 20 and h > 10:
                element = {
                    'x': x + w // 2,
                    'y': y + h // 2,
                    'width': w,
                    'height': h,
                    'type': self._classify_element(w, h)
                }
                
                if element_type == "all" or element['type'] == element_type:
                    elements.append(element)
        
        return elements

    def _classify_element(self, width: int, height: int) -> str:
        """
        Classify UI element based on dimensions.
        
        Args:
            width: Element width
            height: Element height
            
        Returns:
            Element type string
        """
        aspect_ratio = width / height if height > 0 else 0
        
        if 1.5 <= aspect_ratio <= 5 and height < 50:
            return "button"
        elif aspect_ratio > 5 and height < 40:
            return "field"
        elif aspect_ratio < 1.5:
            return "icon"
        else:
            return "unknown"

    def get_screen_region(self, x: int, y: int, width: int, height: int) -> np.ndarray:
        """
        Get a specific region of the screen.
        
        Args:
            x, y: Top-left coordinates
            width, height: Region dimensions
            
        Returns:
            Region as numpy array
        """
        region = {
            'left': x,
            'top': y,
            'width': width,
            'height': height
        }
        return self.capture_screen(region)

    def get_color_at_position(self, x: int, y: int) -> Tuple[int, int, int]:
        """
        Get the RGB color at a specific screen position.
        
        Args:
            x, y: Screen coordinates
            
        Returns:
            RGB tuple
        """
        if self.last_screenshot is None:
            self.capture_screen()
        
        if (0 <= y < self.last_screenshot.shape[0] and 
            0 <= x < self.last_screenshot.shape[1]):
            return tuple(self.last_screenshot[y, x])
        
        return (0, 0, 0)

    def save_screenshot(self, filepath: str, region: Optional[Dict] = None):
        """
        Save a screenshot to file.
        
        Args:
            filepath: Path to save the image
            region: Optional region to capture
        """
        img = self.capture_screen(region)
        img_pil = Image.fromarray(img)
        img_pil.save(filepath)

    def find_element_by_color(self, color: Tuple[int, int, int], 
                              tolerance: int = 30) -> List[Dict]:
        """
        Find elements on screen by color.
        
        Args:
            color: RGB color to search for
            tolerance: Color matching tolerance
            
        Returns:
            List of matching regions
        """
        img = self.capture_screen()
        
        # Create color mask
        lower = np.array([max(0, c - tolerance) for c in color])
        upper = np.array([min(255, c + tolerance) for c in color])
        
        mask = cv2.inRange(img, lower, upper)
        
        # Find contours in mask
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        results = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if w > 5 and h > 5:  # Filter tiny regions
                results.append({
                    'x': x + w // 2,
                    'y': y + h // 2,
                    'width': w,
                    'height': h
                })
        
        return results

    def wait_for_element(self, text: str, timeout: int = 30, 
                         check_interval: float = 0.5) -> Optional[Dict]:
        """
        Wait for an element with specific text to appear on screen.
        
        Args:
            text: Text to search for
            timeout: Maximum time to wait in seconds
            check_interval: Time between checks in seconds
            
        Returns:
            Element dictionary or None if timeout
        """
        import time
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            results = self.find_text_on_screen(text)
            if results:
                return results[0]
            time.sleep(check_interval)
        
        return None
