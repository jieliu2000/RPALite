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
import locale
from unittest.mock import patch


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def get_test_app_and_description():
        dir_path = os.path.dirname(os.path.realpath(__file__))
        test_executable = os.path.abspath(os.path.join(dir_path, os.pardir,  os.pardir, "intes.exe"))
        return test_executable, "INTES*", "FLTK"

def download_test_app():
    check_file = os.path.isfile("intes.exe")
    if check_file:
        logger.info("Test application already exists.")
        return
    check_and_download_updates(GitHubRepo("jieliu2000", "intes"),  # Releases source
        SimpleSpec(">0.1"),  
        assets_mask=re.compile(".*\\.zip"),  # Download *.exe only
        downloads_dir=Path("../")
    )

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

    def test_add_chinese_support_if_needed_non_chinese_system(self):
        """Test _add_chinese_support_if_needed with non-Chinese system language"""
        print("Testing _add_chinese_support_if_needed with non-Chinese system...")
        
        with patch('locale.getlocale') as mock_getlocale, \
             patch('locale.getdefaultlocale') as mock_getdefaultlocale:
            # Mock English system
            mock_getlocale.return_value = ('en_US', 'UTF-8')
            mock_getdefaultlocale.return_value = ('en_US', 'UTF-8')
            
            # Test with EasyOCR
            languages = ['en']
            result = self.rpalite._add_chinese_support_if_needed(languages, 'easyocr')
            assert result == ['en']  # Should remain unchanged
            
            # Test with PaddleOCR
            result = self.rpalite._add_chinese_support_if_needed(languages, 'paddleocr')
            assert result == ['en']  # Should remain unchanged
            
        print("Finished testing _add_chinese_support_if_needed with non-Chinese system...")

    def test_add_chinese_support_if_needed_chinese_system_easyocr(self):
        """Test _add_chinese_support_if_needed with Chinese system and EasyOCR"""
        print("Testing _add_chinese_support_if_needed with Chinese system and EasyOCR...")
        
        with patch('locale.getlocale') as mock_getlocale, \
             patch('locale.getdefaultlocale') as mock_getdefaultlocale:
            # Mock Chinese system
            mock_getlocale.return_value = ('zh_CN', 'UTF-8')
            mock_getdefaultlocale.return_value = ('zh_CN', 'UTF-8')
            
            # Test with initial English only
            languages = ['en']
            result = self.rpalite._add_chinese_support_if_needed(languages, 'easyocr')
            assert 'en' in result
            assert 'ch_sim' in result
            assert len(result) == 2  # Only 'en' and 'ch_sim' for EasyOCR
            
            # Test with existing Chinese language
            languages = ['en', 'ch_sim']
            result = self.rpalite._add_chinese_support_if_needed(languages, 'easyocr')
            assert 'en' in result
            assert 'ch_sim' in result
            assert len(result) == 2  # Should not duplicate ch_sim
            
            # Test without English initially
            languages = ['fr']
            result = self.rpalite._add_chinese_support_if_needed(languages, 'easyocr')
            assert 'en' in result  # Should add 'en' for EasyOCR compatibility
            assert 'ch_sim' in result
            assert 'fr' in result
            assert len(result) == 3
            
        print("Finished testing _add_chinese_support_if_needed with Chinese system and EasyOCR...")

    def test_add_chinese_support_if_needed_chinese_system_paddleocr(self):
        """Test _add_chinese_support_if_needed with Chinese system and PaddleOCR"""
        print("Testing _add_chinese_support_if_needed with Chinese system and PaddleOCR...")
        
        with patch('locale.getlocale') as mock_getlocale, \
             patch('locale.getdefaultlocale') as mock_getdefaultlocale:
            # Mock Chinese system
            mock_getlocale.return_value = ('zh_TW', 'UTF-8')
            mock_getdefaultlocale.return_value = ('zh_TW', 'UTF-8')
            
            # Test with initial English only
            languages = ['en']
            result = self.rpalite._add_chinese_support_if_needed(languages, 'paddleocr')
            assert 'en' in result
            assert 'ch' in result
            assert len(result) == 2  # Only 'en' and 'ch' for PaddleOCR
            
            # Test with existing Chinese language
            languages = ['en', 'ch']
            result = self.rpalite._add_chinese_support_if_needed(languages, 'paddleocr')
            assert 'en' in result
            assert 'ch' in result
            assert len(result) == 2  # Should not duplicate ch
            
            # Test without English initially
            languages = ['fr']
            result = self.rpalite._add_chinese_support_if_needed(languages, 'paddleocr')
            assert 'ch' in result
            assert 'fr' in result
            assert len(result) == 2  # Only 'fr' and 'ch' for PaddleOCR
            
        print("Finished testing _add_chinese_support_if_needed with Chinese system and PaddleOCR...")

    def test_add_chinese_support_if_needed_various_chinese_variants(self):
        """Test _add_chinese_support_if_needed with various Chinese locale variants"""
        print("Testing _add_chinese_support_if_needed with various Chinese variants...")
        
        chinese_locales = ['zh_CN', 'zh_TW', 'zh_HK', 'zh_SG', 'zh', 'Chinese_China']
        
        for locale_name in chinese_locales:
            with patch('locale.getlocale') as mock_getlocale, \
                 patch('locale.getdefaultlocale') as mock_getdefaultlocale:
                mock_getlocale.return_value = (locale_name, 'UTF-8')
                mock_getdefaultlocale.return_value = (locale_name, 'UTF-8')
                
                languages = ['en']
                result = self.rpalite._add_chinese_support_if_needed(languages, 'easyocr')
                assert 'ch_sim' in result, f"Failed for locale: {locale_name}"
                assert len(result) >= 2, f"Not enough languages added for locale: {locale_name}"
                
        print("Finished testing _add_chinese_support_if_needed with various Chinese variants...")

    def test_add_chinese_support_if_needed_exception_handling(self):
        """Test _add_chinese_support_if_needed exception handling"""
        print("Testing _add_chinese_support_if_needed exception handling...")
        
        with patch('locale.getlocale') as mock_getlocale, \
             patch('locale.getdefaultlocale') as mock_getdefaultlocale:
            # Mock exception in both locale functions
            mock_getlocale.side_effect = Exception("Mocked exception")
            mock_getdefaultlocale.side_effect = Exception("Mocked exception")
            
            languages = ['en']
            result = self.rpalite._add_chinese_support_if_needed(languages, 'easyocr')
            assert result == ['en']  # Should return original list on exception
            
        print("Finished testing _add_chinese_support_if_needed exception handling...")

    def test_add_chinese_support_if_needed_none_locale(self):
        """Test _add_chinese_support_if_needed with None locale"""
        print("Testing _add_chinese_support_if_needed with None locale...")
        
        with patch('locale.getlocale') as mock_getlocale, \
             patch('locale.getdefaultlocale') as mock_getdefaultlocale:
            # Mock None locale
            mock_getlocale.return_value = (None, None)
            mock_getdefaultlocale.return_value = (None, None)
            
            languages = ['en']
            result = self.rpalite._add_chinese_support_if_needed(languages, 'easyocr')
            assert result == ['en']  # Should return original list when locale is None
            
        print("Finished testing _add_chinese_support_if_needed with None locale...")

    def test_add_chinese_support_if_needed_unsupported_ocr_engine(self):
        """Test _add_chinese_support_if_needed with unsupported OCR engine"""
        print("Testing _add_chinese_support_if_needed with unsupported OCR engine...")
        
        with patch('locale.getlocale') as mock_getlocale, \
             patch('locale.getdefaultlocale') as mock_getdefaultlocale:
            # Mock Chinese system
            mock_getlocale.return_value = ('zh_CN', 'UTF-8')
            mock_getdefaultlocale.return_value = ('zh_CN', 'UTF-8')
            
            languages = ['en']
            result = self.rpalite._add_chinese_support_if_needed(languages, 'unsupported_ocr')
            assert result == ['en']  # Should return original list for unsupported OCR engine
            
        print("Finished testing _add_chinese_support_if_needed with unsupported OCR engine...")


    @classmethod
    def teardown_class(cls):
        print("Tearing down the test class")
        test_app_and_description = get_test_app_and_description()
        application = cls.rpalite.find_application(test_app_and_description[1], test_app_and_description[2])
        if(application is not None):
            cls.rpalite.close_app(application)
        file = cls.rpalite.stop_screen_recording()
        print(f"Recording saved to: {file}")
