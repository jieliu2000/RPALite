#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RPALite Linux-specific functionality tests
Test Linux platform-specific features and environment adaptation
"""

import unittest
import platform
import os
import subprocess
import tempfile
from unittest.mock import patch, MagicMock, mock_open
import pytest

# 只在Linux环境下运行这些测试
pytestmark = pytest.mark.skipif(platform.system() != 'Linux', reason="Linux specific tests")

from RPALite import RPALite
from RPALite.linux_config import LinuxConfig, get_linux_config

class TestRPALiteLinux(unittest.TestCase):
    """Linux-specific functionality test class"""
    
    def setUp(self):
        """Test setup"""
        self.rpalite = None
        # Reset Linux config before each test
        import RPALite.linux_config
        RPALite.linux_config._linux_config = None

    def tearDown(self):
        """Test cleanup"""
        if self.rpalite:
            # Clean up possible screen recording threads
            if hasattr(self.rpalite, 'screen_recording_thread') and self.rpalite.screen_recording_thread:
                self.rpalite.stop_screen_recording()

    def test_linux_initialization(self):
        """Test Linux environment initialization"""
        with patch.dict(os.environ, {'DISPLAY': ':0', 'XDG_CURRENT_DESKTOP': 'GNOME'}):
            rpalite = RPALite(debug_mode=True)
            self.assertEqual(rpalite.platform, 'Linux')
            self.assertTrue(hasattr(rpalite, 'linux_config'))

    def test_linux_initialization_strict_mode(self):
        """Test initialization in strict mode"""
        # Test strict mode when dependencies are missing
        with patch('shutil.which', return_value=None):
            with self.assertRaises(Exception):
                RPALite(strict_mode=True)

    def test_linux_environment_detection(self):
        """测试Linux环境检测"""
        with patch.dict(os.environ, {
            'DISPLAY': ':0',
            'XDG_CURRENT_DESKTOP': 'GNOME',
            'WAYLAND_DISPLAY': ''
        }):
            rpalite = RPALite(debug_mode=True)
            # 应该成功初始化而不抛出异常
            self.assertIsNotNone(rpalite)

    def test_wayland_detection(self):
        """测试Wayland环境检测"""
        with patch.dict(os.environ, {
            'WAYLAND_DISPLAY': 'wayland-0',
            'XDG_CURRENT_DESKTOP': 'GNOME'
        }):
            with patch('robot.api.logger.warn') as mock_warn:
                rpalite = RPALite(debug_mode=True)
                # 应该发出Wayland警告
                mock_warn.assert_called()

    def test_send_keys_linux(self):
        """测试Linux键盘输入功能"""
        with patch('keyboard.send') as mock_send, \
             patch('keyboard.write') as mock_write:
            
            rpalite = RPALite()
            
            # 测试基本文本输入
            rpalite.send_keys("hello")
            mock_write.assert_called_with("hello", delay=0.1)
            
            # 测试特殊键
            rpalite.send_keys("{ENTER}")
            mock_send.assert_called_with("enter")
            
            # 测试组合键
            rpalite.send_keys("^c")
            mock_send.assert_called_with("ctrl+c")

    def test_mouse_operations_linux(self):
        """测试Linux鼠标操作"""
        with patch('mouse.move') as mock_move, \
             patch('mouse.click') as mock_click, \
             patch('mouse.wheel') as mock_wheel:
            
            rpalite = RPALite()
            
            # 测试鼠标移动
            rpalite.mouse_move(100, 200)
            mock_move.assert_called_with((100, 200))
            
            # 测试鼠标点击
            rpalite.click_by_position(150, 250)
            mock_move.assert_called()
            mock_click.assert_called()
            
            # 测试滚轮
            rpalite.scroll(3)
            mock_wheel.assert_called_with(3)

    def test_show_desktop_linux(self):
        """测试Linux显示桌面功能"""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value.returncode = 0
            
            rpalite = RPALite()
            rpalite.show_desktop()
            
            # 应该尝试调用系统命令
            mock_run.assert_called()

    def test_find_application_linux(self):
        """测试Linux应用程序查找"""
        mock_output = "12345\n67890\n"
        with patch('subprocess.run') as mock_run:
            mock_run.return_value.returncode = 0
            mock_run.return_value.stdout = mock_output
            
            rpalite = RPALite()
            app = rpalite.find_application("firefox")
            
            self.assertIsNotNone(app)
            self.assertIn('window_id', app)
            self.assertEqual(app['window_id'], '12345')

    def test_maximize_window_linux(self):
        """测试Linux窗口最大化"""
        app = {'window_id': '12345'}
        
        with patch('subprocess.run') as mock_run:
            mock_run.return_value.returncode = 0
            
            rpalite = RPALite()
            rpalite.maximize_window(app)
            
            # 应该尝试调用窗口操作命令
            mock_run.assert_called()

    def test_close_app_linux(self):
        """测试Linux应用关闭"""
        app = {'window_id': '12345'}
        
        with patch('subprocess.run') as mock_run:
            mock_run.return_value.returncode = 0
            
            rpalite = RPALite()
            rpalite.close_app(app)
            
            # 应该尝试调用关闭命令
            mock_run.assert_called()

class TestLinuxConfig(unittest.TestCase):
    """Linux configuration management tests"""
    
    def setUp(self):
        """Test setup"""
        # Use temporary directory for testing
        self.temp_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        """Test cleanup"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_linux_config_creation(self):
        """测试Linux配置创建"""
        config = LinuxConfig(config_dir=self.temp_dir)
        self.assertIsNotNone(config.distro)
        self.assertIsNotNone(config.desktop_env)
        self.assertIsInstance(config.available_tools, dict)

    def test_distro_detection(self):
        """测试发行版检测"""
        with patch('builtins.open', mock_open(read_data='ID=ubuntu\nNAME="Ubuntu"\n')):
            config = LinuxConfig(config_dir=self.temp_dir)
            self.assertEqual(config.distro, 'ubuntu')

    def test_desktop_environment_detection(self):
        """测试桌面环境检测"""
        with patch.dict(os.environ, {'XDG_CURRENT_DESKTOP': 'GNOME'}):
            config = LinuxConfig(config_dir=self.temp_dir)
            self.assertEqual(config.desktop_env, 'GNOME')

    def test_tool_availability_scan(self):
        """测试工具可用性扫描"""
        with patch('shutil.which') as mock_which:
            # 模拟xdotool可用，wmctrl不可用
            mock_which.side_effect = lambda x: '/usr/bin/xdotool' if x == 'xdotool' else None
            
            config = LinuxConfig(config_dir=self.temp_dir)
            self.assertTrue(config.available_tools['xdotool'])
            self.assertFalse(config.available_tools['wmctrl'])

    def test_install_command_generation(self):
        """测试安装命令生成"""
        config = LinuxConfig(config_dir=self.temp_dir)
        config.distro = 'ubuntu'
        
        install_cmd = config.get_install_command('xdotool')
        self.assertIn('apt-get install', install_cmd)
        self.assertIn('xdotool', install_cmd)

    def test_desktop_shortcuts(self):
        """测试桌面快捷键获取"""
        config = LinuxConfig(config_dir=self.temp_dir)
        config.desktop_env = 'GNOME'
        
        shortcuts = config.get_desktop_shortcuts('show_desktop')
        self.assertIsInstance(shortcuts, list)
        self.assertTrue(len(shortcuts) > 0)

    def test_config_persistence(self):
        """测试配置持久化"""
        config1 = LinuxConfig(config_dir=self.temp_dir)
        config1.set_user_preference('test_key', 'test_value')
        
        # 创建新实例，应该加载保存的配置
        config2 = LinuxConfig(config_dir=self.temp_dir)
        self.assertEqual(config2.get_user_preference('test_key'), 'test_value')

    def test_dependency_report(self):
        """测试依赖报告生成"""
        config = LinuxConfig(config_dir=self.temp_dir)
        report = config.generate_dependency_report()
        
        self.assertIn('RPALite Linux依赖报告', report)
        self.assertIn('发行版:', report)
        self.assertIn('桌面环境:', report)

    def test_global_config_instance(self):
        """测试全局配置实例"""
        # 重置全局实例
        import RPALite.linux_config
        RPALite.linux_config._linux_config = None
        
        config1 = get_linux_config()
        config2 = get_linux_config()
        
        # 应该返回同一个实例
        self.assertIs(config1, config2)

class TestLinuxIntegration(unittest.TestCase):
    """Linux集成测试"""
    
    def test_end_to_end_workflow(self):
        """测试端到端工作流"""
        with patch('subprocess.run') as mock_run, \
             patch('pyautogui.screenshot') as mock_screenshot, \
             patch('keyboard.write') as mock_keyboard:
            
            # 模拟成功的系统调用
            mock_run.return_value.returncode = 0
            mock_run.return_value.stdout = "12345\n"
            
            # 模拟截图
            mock_image = MagicMock()
            mock_image.size = (1920, 1080)
            mock_screenshot.return_value = mock_image
            
            rpalite = RPALite(debug_mode=True)
            
            # 测试完整工作流：显示桌面 -> 运行命令 -> 输入文本 -> 截图
            rpalite.show_desktop()
            rpalite.run_command("gedit")
            rpalite.input_text("Hello Linux!")
            screenshot = rpalite.take_screenshot()
            
            # 验证操作被调用
            mock_run.assert_called()
            mock_keyboard.assert_called_with("Hello Linux!", delay=0.2)
            mock_screenshot.assert_called()

if __name__ == '__main__':
    # 只在Linux环境下运行测试
    if platform.system() == 'Linux':
        unittest.main()
    else:
        print("跳过Linux特定测试 - 不在Linux环境中") 