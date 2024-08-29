from datetime import datetime
from RPALite import RPALite
import PIL
import platform
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def get_test_app_and_description():
        return "intes-go.exe", "INTES-GO*", "GLFW30"

class TestRPALite:

    @classmethod
    def setup_class(cls):
        logger.info("Setup class...")
        cls.rpalite = RPALite(debug_mode=False)

    def open_app(self):
        self.rpalite.run_command(get_test_app_and_description()[0]) 
        return self.rpalite.find_application(get_test_app_and_description()[1], get_test_app_and_description()[2])
     
    
    def test_clipboard(self):
        pass

    def test_click_image(self):
        pass

    def test_scroll(self):  
        pass


    def test_click_automate_id(self):
        pass

    def test_get_screen_size(self):
        size = self.rpalite.get_screen_size()
        assert(size[0] > 10 and size[1] > 10)

    def test_mouse_click(self):
        app = self.open_app()
        #self.rpalite.maximize_window(app)
        self.rpalite.click_by_text("Button 1")
        self.rpalite.validate_text_exists("Button 1 pressed")
        self.close_app()
        print("Finished testing mouse press move actions...")

    def test_find_window_by_title(self):
        pass

    def close_app(self):
        test_app_and_description = get_test_app_and_description()
        application = self.rpalite.find_application(test_app_and_description[1], test_app_and_description[2])
        if(application is not None):
            self.rpalite.close_app(application)
        logger.info("Application closed...")

    def test_init(self):
        print("Testing init...")
        assert self.rpalite is not None
        assert self.rpalite.platform == "Windows"
        print("Finished testing init...")
    
    
    def test_maximize_window_by_app(self):
        app = self.open_app()
        self.rpalite.maximize_window(app)
        window = app.windows()[0]
        client_rect = window.client_rect()
        logger.info(f"Client rect: {client_rect}")
        size = self.rpalite.get_screen_size()
        assert client_rect.right == size[0] and client_rect.bottom > size[1]- 100
        self.close_app()

    def test_run_command(self):
        print("Testing run command...")
        self.rpalite.run_command(get_test_app_and_description()[0]) 
        application = self.rpalite.find_application(get_test_app_and_description()[1], get_test_app_and_description()[2])
        assert application is not None
        self.close_app()
        print("Finished testing run command...")

    def test_sleep(self):
        print("Testing sleep...")
        start = datetime.now()
        self.rpalite.sleep(1)
        end = datetime.now()
        difference = end - start
        assert difference.total_seconds() >= 1

        rpalite = RPALite(step_pause_interval=5)
        start = datetime.now()
        rpalite.sleep()
        end = datetime.now()
        difference = end - start
        assert difference.total_seconds() >= 5
        print("Finished testing sleep...")


    @classmethod
    def teardown_class(cls):
        print("Tearing down the test class")
        test_app_and_description = get_test_app_and_description()
        application = cls.rpalite.find_application(test_app_and_description[1], test_app_and_description[2])
        if(application is not None):
            cls.rpalite.close_app(application)
