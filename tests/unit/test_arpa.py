from datetime import datetime
from RPALite import RPALite
import random
import pytest
import os
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def get_test_app_and_description():
        dir_path = os.path.dirname(os.path.realpath(__file__))
        test_executable = os.path.abspath(os.path.join(dir_path, os.pardir,  os.pardir, "intes.exe"))
        return test_executable, "INTES*", "FLTK"

class TestRPALite:

    @classmethod
    def setup_class(cls):
        logger.info("Setup class...")
        cls.rpalite = RPALite(debug_mode=False)
        dir_path = os.path.dirname(os.path.realpath(__file__))
        test_path = os.path.abspath(os.path.join(dir_path, os.pardir))
        recording_path = os.path.join(test_path, "recording")
        if not os.path.exists(recording_path):
            os.makedirs(recording_path)
        target_video = os.path.join(recording_path, 'test.avi')
        cls.rpalite.start_screen_recording(target_video)

    def open_app(self):
        self.rpalite.run_command(get_test_app_and_description()[0]) 
        return self.rpalite.find_application(get_test_app_and_description()[1], get_test_app_and_description()[2])
     
    
    def test_clipboard(self):
        pass

    def test_click_image(self):
        pass

    def test_scroll(self):  
        pass

    
    def test_click_automate_id_notepad(self):
        
        self.rpalite.send_keys('{VK_LWIN down}{VK_LWIN up}')
        try:
            position = self.rpalite.validate_text_exists("Window Server")
            # This case cannot run on windows server
            if position is not None:
                self.rpalite.send_keys('{VK_LWIN down}M{VK_LWIN up}')
                return 
        except Exception as e:
            # not windows server
            print("not windows server")    
            
        self.rpalite.send_keys('{VK_LWIN down}M{VK_LWIN up}')

        self.rpalite.run_command("notepad.exe")
        app = self.rpalite.find_application(".*Notepad")
        assert app is not None
        self.rpalite.maximize_window(app)

        self.rpalite.click("automateId:File", app= app)
        
        self.rpalite.validate_text_exists("Page setup")
        
        self.rpalite.click("Exit", app= app)

        with pytest.raises(AssertionError):
            self.rpalite.validate_text_exists("Page setup")
       
        self.rpalite.close_app(app)    

    def test_get_screen_size(self):
        size = self.rpalite.get_screen_size()
        assert(size[0] > 200 and size[1] > 200)

    def test_validate_text_exists(self):
        with pytest.raises(AssertionError):
            self.rpalite.validate_text_exists("")
        
        app = self.open_app()
        #self.rpalite.maximize_window(app)
        with pytest.raises(AssertionError):
            self.rpalite.validate_text_exists("Dummy Text")
        
        position = self.rpalite.validate_text_exists("Mouse Test Canvas")
        assert(len(position)> 0)

        self.close_app()

    def test_mouse_click(self):
        app = self.open_app()
        self.rpalite.maximize_window(app)
        self.rpalite.click_by_text("Button B")
        self.rpalite.validate_text_exists("Button B clicked")

        with pytest.raises(AssertionError):
            self.rpalite.validate_text_exists("Button A clicked")
        
        self.close_app()
        print("Finished testing mouse press move actions...")

    def test_find_window_by_title(self):
        
        app = self.open_app()
        windows = self.rpalite.find_windows_by_title("Mouse Test Canvas")
        assert len(windows) > 0

        window = windows[0]
        assert window is not None
        assert window[2]> 100
        assert window[3] > 80
        self.close_app()
        print("Finished testing mouse press move actions...")
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
        file = cls.rpalite.stop_screen_recording()
        print(f"Recording saved to: {file}")
