from datetime import datetime
from RPALite import RPALite
import PIL
import platform

def get_test_app_and_description():
        return "intes-go.exe", "INTES-GO*", "GLFW30"

class TestRPALite:

    @classmethod
    def setup_class(cls):
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

    def test_mouse_press_move_actions(self):
        app = self.open_app()
        self.rpalite.maximize_window(app)
        text = "Sample text for testing scroll:\n"
        self.rpalite.input_text(text)
        self.rpalite.click_by_text("Sample")
        self.rpalite.mouse_press()

        location = self.rpalite.validate_text_exists("scroll")

        self.rpalite.mouse_move(location[0], location[1])
        self.rpalite.mouse_release()
        self.rpalite.sleep(20)
        self.close_app()
        print("Finished testing mouse press move actions...")

    def test_find_window_by_title(self):
        pass

    def close_app(self):
        test_app_and_description = get_test_app_and_description()
        application = self.rpalite.find_application(test_app_and_description[1], test_app_and_description[2])
        if(application is not None):
            self.rpalite.close_app(application)

    def test_init(self):
        print("Testing init...")
        assert self.rpalite is not None
        assert self.rpalite.platform == "Windows"
        print("Finished testing init...")
    
    
    def test_maximize_window_by_app(self):
        print("Testing maximize window by app...")
        app = self.open_app()
        self.rpalite.maximize_window(app)
        window = app.windows()[0]
        client_rect = window.client_rect()
        print(client_rect)
        self.close_app()
        print("Finished testing maximize window by app...")

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
