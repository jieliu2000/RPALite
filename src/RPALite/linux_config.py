#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RPALite Linux Configuration Management Module
Provides Linux platform-specific configuration and environment management functionality
"""

import os
import subprocess
import shutil
import logging
from typing import Dict, List, Optional, Tuple
import json
from pathlib import Path

logger = logging.getLogger(__name__)

class LinuxConfig:
    """Linux platform configuration manager"""
    
    DEFAULT_TOOLS = {
        'xdotool': {
            'command': 'xdotool',
            'install_ubuntu': 'sudo apt-get install -y xdotool',
            'install_centos': 'sudo yum install -y xdotool',
            'install_fedora': 'sudo dnf install -y xdotool',
            'install_arch': 'sudo pacman -S xdotool',
            'description': 'Window operation and keyboard/mouse simulation tool'
        },
        'wmctrl': {
            'command': 'wmctrl',
            'install_ubuntu': 'sudo apt-get install -y wmctrl',
            'install_centos': 'sudo yum install -y wmctrl',
            'install_fedora': 'sudo dnf install -y wmctrl',
            'install_arch': 'sudo pacman -S wmctrl',
            'description': 'Window manager control tool'
        },
        'xwininfo': {
            'command': 'xwininfo',
            'install_ubuntu': 'sudo apt-get install -y x11-utils',
            'install_centos': 'sudo yum install -y xorg-x11-utils',
            'install_fedora': 'sudo dnf install -y xorg-x11-utils',
            'install_arch': 'sudo pacman -S xorg-xwininfo',
            'description': 'Window information query tool'
        },
        'xprop': {
            'command': 'xprop',
            'install_ubuntu': 'sudo apt-get install -y x11-utils',
            'install_centos': 'sudo yum install -y xorg-x11-utils',
            'install_fedora': 'sudo dnf install -y xorg-x11-utils',
            'install_arch': 'sudo pacman -S xorg-xprop',
            'description': 'Window property query tool'
        }
    }
    
    DESKTOP_SHORTCUTS = {
        'GNOME': {
            'show_desktop': ['ctrl+alt+d', 'super+d'],
            'minimize_all': ['ctrl+alt+d'],
            'switch_workspace': ['ctrl+alt+left', 'ctrl+alt+right']
        },
        'KDE': {
            'show_desktop': ['ctrl+alt+d', 'meta+d'],
            'minimize_all': ['ctrl+alt+d'],
            'switch_workspace': ['ctrl+f1', 'ctrl+f2']
        },
        'XFCE': {
            'show_desktop': ['ctrl+alt+d'],
            'minimize_all': ['ctrl+alt+d'],
            'switch_workspace': ['ctrl+alt+left', 'ctrl+alt+right']
        },
        'Unity': {
            'show_desktop': ['ctrl+alt+d', 'super+d'],
            'minimize_all': ['ctrl+alt+d'],
            'switch_workspace': ['ctrl+alt+left', 'ctrl+alt+right']
        }
    }
    
    def __init__(self, config_dir: Optional[str] = None):
        """
        Initialize Linux configuration manager
        
        Parameters
        ----------
        config_dir : str, optional
            Configuration file directory, defaults to .rpalite in user home directory
        """
        if config_dir is None:
            self.config_dir = Path.home() / '.rpalite'
        else:
            self.config_dir = Path(config_dir)
        
        self.config_dir.mkdir(exist_ok=True)
        self.config_file = self.config_dir / 'linux_config.json'
        
        self.distro = self._detect_linux_distro()
        self.desktop_env = self._detect_desktop_environment()
        self.available_tools = self._scan_available_tools()
        
        # Load or create configuration
        self.config = self._load_config()
    
    def _detect_linux_distro(self) -> str:
        """Detect Linux distribution"""
        try:
            # Try to read /etc/os-release
            with open('/etc/os-release', 'r') as f:
                for line in f:
                    if line.startswith('ID='):
                        distro = line.split('=')[1].strip().strip('"')
                        return distro.lower()
        except FileNotFoundError:
            pass
        
        # Fallback detection methods
        distro_files = {
            'ubuntu': '/etc/lsb-release',
            'debian': '/etc/debian_version',
            'centos': '/etc/centos-release',
            'fedora': '/etc/fedora-release',
            'arch': '/etc/arch-release',
            'opensuse': '/etc/SuSE-release'
        }
        
        for distro, file_path in distro_files.items():
            if os.path.exists(file_path):
                return distro
        
        return 'unknown'
    
    def _detect_desktop_environment(self) -> str:
        """Detect desktop environment"""
        env_vars = [
            'XDG_CURRENT_DESKTOP',
            'DESKTOP_SESSION',
            'GDMSESSION'
        ]
        
        for var in env_vars:
            value = os.environ.get(var)
            if value:
                # Handle composite values like "ubuntu:GNOME"
                if ':' in value:
                    value = value.split(':')[-1]
                return value.upper()
        
        # Try detection through processes
        try:
            result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
            if result.returncode == 0:
                processes = result.stdout.lower()
                if 'gnome-session' in processes:
                    return 'GNOME'
                elif 'kded' in processes or 'plasma' in processes:
                    return 'KDE'
                elif 'xfce' in processes:
                    return 'XFCE'
        except Exception:
            pass
        
        return 'UNKNOWN'
    
    def _scan_available_tools(self) -> Dict[str, bool]:
        """Scan available tools in the system"""
        available = {}
        for tool_name, tool_info in self.DEFAULT_TOOLS.items():
            available[tool_name] = shutil.which(tool_info['command']) is not None
        return available
    
    def _load_config(self) -> Dict:
        """Load configuration file"""
        default_config = {
            'distro': self.distro,
            'desktop_env': self.desktop_env,
            'available_tools': self.available_tools,
            'preferred_tools': self._get_preferred_tools(),
            'timeouts': {
                'command_timeout': 10,
                'window_operation_timeout': 5,
                'screenshot_timeout': 3
            },
            'retry_counts': {
                'window_find_retry': 3,
                'command_retry': 2
            },
            'user_preferences': {
                'auto_install_missing_tools': False,
                'show_tool_suggestions': True,
                'use_fallback_methods': True
            }
        }
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                # Merge default config with loaded config
                default_config.update(loaded_config)
            except Exception as e:
                logger.warn(f"Failed to load config file: {e}, using default config")
        
        # Save config (including any new default values)
        self._save_config(default_config)
        return default_config
    
    def _save_config(self, config: Dict):
        """保存配置到文件"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"保存配置文件失败: {e}")
    
    def _get_preferred_tools(self) -> Dict[str, str]:
        """根据可用性确定首选工具"""
        preferred = {}
        
        # 窗口操作首选工具
        if self.available_tools.get('xdotool'):
            preferred['window_ops'] = 'xdotool'
        elif self.available_tools.get('wmctrl'):
            preferred['window_ops'] = 'wmctrl'
        else:
            preferred['window_ops'] = None
            
        # 窗口管理首选工具
        if self.available_tools.get('wmctrl'):
            preferred['window_mgmt'] = 'wmctrl'
        elif self.available_tools.get('xdotool'):
            preferred['window_mgmt'] = 'xdotool'
        else:
            preferred['window_mgmt'] = None
        
        return preferred
    
    def get_install_command(self, tool: str) -> Optional[str]:
        """获取工具的安装命令"""
        if tool not in self.DEFAULT_TOOLS:
            return None
        
        tool_info = self.DEFAULT_TOOLS[tool]
        install_key = f'install_{self.distro}'
        
        return tool_info.get(install_key, tool_info.get('install_ubuntu'))
    
    def get_desktop_shortcuts(self, action: str) -> List[str]:
        """获取桌面环境特定的快捷键"""
        desktop_shortcuts = self.DESKTOP_SHORTCUTS.get(self.desktop_env, {})
        return desktop_shortcuts.get(action, [])
    
    def update_tool_availability(self):
        """更新工具可用性状态"""
        self.available_tools = self._scan_available_tools()
        self.config['available_tools'] = self.available_tools
        self.config['preferred_tools'] = self._get_preferred_tools()
        self._save_config(self.config)
    
    def get_timeout(self, operation: str) -> int:
        """获取操作超时时间"""
        return self.config['timeouts'].get(operation, 5)
    
    def get_retry_count(self, operation: str) -> int:
        """获取操作重试次数"""
        return self.config['retry_counts'].get(operation, 2)
    
    def set_user_preference(self, key: str, value):
        """设置用户偏好"""
        self.config['user_preferences'][key] = value
        self._save_config(self.config)
    
    def get_user_preference(self, key: str, default=None):
        """获取用户偏好"""
        return self.config['user_preferences'].get(key, default)
    
    def generate_dependency_report(self) -> str:
        """生成依赖报告"""
        report_lines = [
            "=== RPALite Linux依赖报告 ===",
            f"发行版: {self.distro}",
            f"桌面环境: {self.desktop_env}",
            "",
            "系统工具状态:"
        ]
        
        for tool_name, tool_info in self.DEFAULT_TOOLS.items():
            status = "✓ 已安装" if self.available_tools.get(tool_name) else "✗ 缺失"
            install_cmd = self.get_install_command(tool_name)
            
            report_lines.append(f"  {tool_name}: {status}")
            report_lines.append(f"    描述: {tool_info['description']}")
            if not self.available_tools.get(tool_name) and install_cmd:
                report_lines.append(f"    安装: {install_cmd}")
            report_lines.append("")
        
        return "\n".join(report_lines)

# 全局配置实例
_linux_config = None

def get_linux_config() -> LinuxConfig:
    """获取全局Linux配置实例"""
    global _linux_config
    if _linux_config is None:
        _linux_config = LinuxConfig()
    return _linux_config 