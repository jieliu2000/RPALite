from datetime import datetime
from RPALite import RPALite
import PIL
import platform

def get_test_app_and_description():
        return "notepad.exe", ".*Notepad.*", "Notepad"

class TestRPALite:

    @classmethod
    def setup_class(cls):
        cls.rpalite = RPALite(debug_mode=False)

    def open_app(self):
        self.rpalite.run_command(get_test_app_and_description()[0]) 
        return self.rpalite.find_application(get_test_app_and_description()[1], get_test_app_and_description()[2])
     
    def test_click_image(self):
        self.platform = platform.system()
        self.platform_release = platform.release()
        if(self.platform != 'Windows' and self.platform_release != '11'):
            # This image is a windows 11 start image. It doesn't work on other platforms.
            pass
        self.rpalite.click("image:./tests/unit/start.png")

    def test_scroll(self):
        app = self.open_app()
        self.rpalite.maximize_window(app)
        text = "Sample text for testing scroll:\n"
        for i in range(0, 50):
            text += "Line " + str(i) + "\n"
            self.rpalite.input_text(text)

        self.rpalite.click_by_position(100, 300)
        self.rpalite.scroll(20)
        self.rpalite.scroll(-20)
        pass


    def test_click_automate_id(self):
        app = self.rpalite.run_command('mspaint')
        app = self.rpalite.find_application(class_name= "MSPaintApp")
        self.rpalite.click('automateId:RotateDropdown', app = app)
        
        location = self.rpalite.validate_text_exists('Rotate 180°')
        assert location is not None, "Text not found"
        
        self.rpalite.close_app(app)


    def test_find_window_by_title(self):
        image = PIL.Image.open('./tests/unit/text_and_window2.png')
        window = self.rpalite.find_windows_by_title('Solution Explorer', image)
        assert window is not None

    def close_app(self):
        test_app_and_description = get_test_app_and_description()
        application = self.rpalite.find_application(test_app_and_description[1], test_app_and_description[2])
        if(application is not None):
            self.rpalite.close_app(application)

    def test_init(self):
        assert self.rpalite is not None
        assert self.rpalite.platform == "Windows"
    
    
    def test_maximize_window_by_app(self):
        app = self.open_app()
        self.rpalite.maximize_window(app)
        window = app.windows()[0]
        client_rect = window.client_rect()
        print(client_rect)
        self.close_app()


    def test_run_command(self):
        self.rpalite.run_command(get_test_app_and_description()[0]) 
        application = self.rpalite.find_application(get_test_app_and_description()[1], get_test_app_and_description()[2])
        assert application is not None
        self.close_app()

    def test_sleep(self):
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


    @classmethod
    def teardown_class(cls):
        print("Tearing down the test class")
        test_app_and_description = get_test_app_and_description()
        application = cls.rpalite.find_application(test_app_and_description[1], test_app_and_description[2])
        if(application is not None):
            cls.rpalite.close_app(application)
