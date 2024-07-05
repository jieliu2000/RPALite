from RPALite import ImageHandler
import PIL
import logging

logger = logging.getLogger(__name__)


class TestImageHandler:
    
    
    @classmethod
    def setup_class(cls):
        cls.handler = ImageHandler(debug_mode=False)

    def test_find_text_in_image(self):
        image = PIL.Image.open('./tests/unit/text_and_window.png')
        location = self.handler.find_text_in_image(image, "Welcome")
        assert location is not None, "Welcome text not found in the image"
        assert location[0] > 0 and location[1] > 0 and location[2]>0 and location[3] > 0, "Coordinates of Welcome text are not valid"

        location = self.handler.find_text_in_image(image, "Welcome", ["dummy_text"])
        assert location is None, "Welcome with dummy_text should not be found in the image"

        location = self.handler.find_text_in_image(image, "Text File")
        assert location is not None, "Text File text not found in the image"

        location = self.handler.find_text_in_image(image, "Text File", ["Built-In"])
        assert location is not None, "'Text File' with 'Built-In' should be found in the image"

        location = self.handler.find_text_in_image(image, "Text File", ["dummy_text"])
        assert location is None, "'Text File' with 'dummy_text' should not be found in the image"

    def test_find_window_outside_position(self):
        image = PIL.Image.open('./tests/unit/text_and_window.png')
        
        location = self.handler.find_text_in_image(image, "Welcome")
        logger.debug(f"Welcome text found at {location}")
        window = self.handler.find_window_outside_position(image, location)
        assert window is None, "The window should not be found"

        location = self.handler.find_text_in_image(image, "Learn the Fundamentals")
        window = self.handler.find_window_outside_position(image, location)
        assert window is not None, "The window should be found"

    def test_find_control_near_position(self):
        image = PIL.Image.open('./tests/unit/text_and_window.png')
        location = self.handler.find_text_in_image(image, "Welcome")
        logger.debug(f"Welcome text found at {location}")
        assert location is not None, "Welcome text not found in the image"

        control = self.handler.find_control_near_position(image, location)
        logger.debug(f"Control found at {control}")


    def test_find_image_location(self):
        start_img = PIL.Image.open('./tests/unit/start.png')
        screen = PIL.Image.open('./tests/unit/screen.png')

         # Find the location of the start image on the screen
        start_location = self.handler.find_image_location( start_img, screen)
        logger.debug(f"Start image found at {start_location}")
        assert start_location is not None, "Start image not found on the screen"