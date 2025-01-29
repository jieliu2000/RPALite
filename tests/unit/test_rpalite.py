from datetime import datetime
from RPALite import RPALite
import random
import pytest
import os
import logging
from semantic_version import SimpleSpec
from github_release_downloader import check_and_download_updates, GitHubRepo
from pathlib import Path
import re
import platform
import zipfile
import shutil
from github import Github
import requests


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def get_test_app_and_description():
        dir_path = os.path.dirname(os.path.realpath(__file__))
        test_executable = os.path.abspath(os.path.join(dir_path, os.pardir,  os.pardir, "intes.exe"))
        return test_executable, "INTES*", "FLTK"

def download_test_app():
    test_app_path = os.path.abspath("intes.exe")
    if os.path.isfile(test_app_path):
        logger.info("Test application already exists.")
        return

    try:
        # Initialize GitHub API
        g = Github()
        repo = g.get_repo("jieliu2000/intes")
        
        # Get the latest release
        latest_release = repo.get_latest_release()
        
        # Find the zip asset
        zip_asset = None
        for asset in latest_release.get_assets():
            if re.match(r".*\.zip", asset.name):
                zip_asset = asset
                break
        
        if not zip_asset:
            raise Exception("No zip file found in the latest release")
        
        # Download the zip file
        logger.info(f"Downloading {zip_asset.name}...")
        headers = {
            "Accept": "application/octet-stream",
        }
        response = requests.get(zip_asset.url, headers=headers, stream=True)
        
        # Save the zip file
        zip_path = os.path.abspath(zip_asset.name)
        with open(zip_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        # Extract the exe from zip
        logger.info(f"Extracting {zip_path}...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # Find the exe file in the zip
            exe_files = [f for f in zip_ref.namelist() if f.lower().endswith('.exe')]
            if not exe_files:
                raise Exception("No exe file found in the downloaded zip")
            
            # Extract the first exe file found
            exe_file = exe_files[0]
            with zip_ref.open(exe_file) as source, open(test_app_path, 'wb') as target:
                shutil.copyfileobj(source, target)
        
        # Set executable permissions (for Unix-like systems)
        os.chmod(test_app_path, 0o755)
        
        # Clean up the zip file
        os.remove(zip_path)
        logger.info("Test application downloaded and extracted successfully.")
        
    except Exception as e:
        logger.error(f"Failed to download and extract test application: {str(e)}")
        if os.path.exists(test_app_path):
            os.remove(test_app_path)
        raise

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
        download_test_app()


    def open_app(self):
        self.rpalite.run_command(get_test_app_and_description()[0]) 
        return self.rpalite.find_application(get_test_app_and_description()[1], get_test_app_and_description()[2])
     
    
    def test_clipboard(self):
        pass

    def test_click_image(self):
        pass

    def test_scroll(self):  
        pass
    
    def test_enter_in_field(self):
        app = self.open_app()
        self.rpalite.maximize_window(app)
        self.rpalite.click_by_text("Keyboard Test")
        self.rpalite.enter_in_field("Textbox 1", "1234567890")
        value = self.rpalite.get_text_field_value("Textbox 1")
        assert(value == "1234567890")
        self.close_app()
    
    def test_click_automate_id_notepad(self):
        if platform.system() != 'Windows':
            return
        
        self.rpalite.send_keys('{VK_LWIN down}{VK_LWIN up}')
        try:
            position = self.rpalite.validate_text_exists("Windows Server")
            # This case cannot run on windows server
            self.rpalite.send_keys('{VK_LWIN down}{VK_LWIN up}')

            if position is not None:
                return 
        except Exception as e:
            # not windows server
            print("not windows server")    
            
        self.rpalite.send_keys('{VK_LWIN down}{VK_LWIN up}')

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
