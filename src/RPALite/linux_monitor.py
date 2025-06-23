#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RPALite Linux Performance Monitoring Module
Monitor performance and resource usage of RPA operations in Linux environment
"""

import time
import psutil
import threading
import logging
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import subprocess
import json
import os

logger = logging.getLogger(__name__)

@dataclass
class PerformanceMetrics:
    """Performance metrics data class"""
    timestamp: datetime
    cpu_percent: float = 0.0
    memory_percent: float = 0.0
    memory_used_mb: float = 0.0
    disk_io_read_mb: float = 0.0
    disk_io_write_mb: float = 0.0
    network_sent_mb: float = 0.0
    network_recv_mb: float = 0.0
    active_windows_count: int = 0
    x11_connections: int = 0
    operation_duration: float = 0.0
    operation_name: str = ""
    error_count: int = 0

@dataclass
class SystemInfo:
    """System information data class"""
    os_version: str = ""
    kernel_version: str = ""
    desktop_environment: str = ""
    x11_server: str = ""
    available_memory_gb: float = 0.0
    cpu_cores: int = 0
    cpu_freq_mhz: float = 0.0
    screen_resolution: str = ""
    installed_tools: Dict[str, bool] = field(default_factory=dict)

class LinuxMonitor:
    """Linux performance monitor"""
    
    def __init__(self, sample_interval: float = 1.0, max_samples: int = 1000):
        """
        Initialize monitor
        
        Parameters
        ----------
        sample_interval : float
            Sampling interval (seconds)
        max_samples : int
            Maximum number of samples to keep
        """
        self.sample_interval = sample_interval
        self.max_samples = max_samples
        self.metrics_history: List[PerformanceMetrics] = []
        self.is_monitoring = False
        self.monitor_thread: Optional[threading.Thread] = None
        self.operation_start_time: Optional[float] = None
        self.current_operation: str = ""
        self.error_count = 0
        
        # Basic system information
        self.system_info = self._collect_system_info()
        
        # Performance threshold configuration
        self.thresholds = {
            'cpu_percent': 80.0,
            'memory_percent': 85.0,
            'operation_duration': 30.0,  # seconds
            'error_rate': 0.1  # 10%
        }
        
        # Callback functions
        self.alert_callbacks: List[Callable] = []

    def _collect_system_info(self) -> SystemInfo:
        """Collect system information"""
        info = SystemInfo()
        
        try:
            # Operating system information
            with open('/etc/os-release', 'r') as f:
                for line in f:
                    if line.startswith('PRETTY_NAME='):
                        info.os_version = line.split('=')[1].strip().strip('"')
                        break
        except FileNotFoundError:
            info.os_version = "Unknown"
        
        try:
            # Kernel version
            info.kernel_version = subprocess.check_output(['uname', '-r'], text=True).strip()
        except subprocess.CalledProcessError:
            info.kernel_version = "Unknown"
        
        # Desktop environment
        info.desktop_environment = os.environ.get('XDG_CURRENT_DESKTOP', 'Unknown')
        
        # X11 server information
        display = os.environ.get('DISPLAY')
        if display:
            try:
                result = subprocess.run(['xdpyinfo'], capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    for line in result.stdout.split('\n'):
                        if 'version number' in line:
                            info.x11_server = line.strip()
                            break
            except (FileNotFoundError, subprocess.TimeoutExpired):
                info.x11_server = f"X Server on {display}"
        
        # Hardware information
        info.available_memory_gb = psutil.virtual_memory().total / (1024**3)
        info.cpu_cores = psutil.cpu_count()
        
        try:
            cpu_freq = psutil.cpu_freq()
            if cpu_freq:
                info.cpu_freq_mhz = cpu_freq.current
        except Exception:
            info.cpu_freq_mhz = 0.0
        
        # Screen resolution
        try:
            result = subprocess.run(['xdpyinfo'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if 'dimensions:' in line:
                        info.screen_resolution = line.split('dimensions:')[1].split()[0]
                        break
        except (FileNotFoundError, subprocess.TimeoutExpired):
            info.screen_resolution = "Unknown"
        
        # Installed tools
        tools_to_check = ['xdotool', 'wmctrl', 'xwininfo', 'xprop', 'xclip']
        for tool in tools_to_check:
            info.installed_tools[tool] = subprocess.run(
                ['which', tool], capture_output=True
            ).returncode == 0
        
        return info

    def start_monitoring(self):
        """Start monitoring"""
        if self.is_monitoring:
            logger.warn("Monitoring is already running")
            return
        
        self.is_monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        logger.info("Performance monitoring started")

    def stop_monitoring(self):
        """Stop monitoring"""
        if not self.is_monitoring:
            return
        
        self.is_monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2.0)
        logger.info("Performance monitoring stopped")

    def _monitor_loop(self):
        """监控循环"""
        last_disk_io = psutil.disk_io_counters()
        last_net_io = psutil.net_io_counters()
        
        while self.is_monitoring:
            try:
                metrics = PerformanceMetrics(timestamp=datetime.now())
                
                # CPU和内存使用率
                metrics.cpu_percent = psutil.cpu_percent(interval=None)
                memory = psutil.virtual_memory()
                metrics.memory_percent = memory.percent
                metrics.memory_used_mb = memory.used / (1024**2)
                
                # 磁盘I/O
                current_disk_io = psutil.disk_io_counters()
                if last_disk_io and current_disk_io:
                    metrics.disk_io_read_mb = (current_disk_io.read_bytes - last_disk_io.read_bytes) / (1024**2)
                    metrics.disk_io_write_mb = (current_disk_io.write_bytes - last_disk_io.write_bytes) / (1024**2)
                    last_disk_io = current_disk_io
                
                # 网络I/O
                current_net_io = psutil.net_io_counters()
                if last_net_io and current_net_io:
                    metrics.network_sent_mb = (current_net_io.bytes_sent - last_net_io.bytes_sent) / (1024**2)
                    metrics.network_recv_mb = (current_net_io.bytes_recv - last_net_io.bytes_recv) / (1024**2)
                    last_net_io = current_net_io
                
                # X11相关信息
                metrics.active_windows_count = self._count_active_windows()
                metrics.x11_connections = self._count_x11_connections()
                
                # 操作信息
                if self.operation_start_time:
                    metrics.operation_duration = time.time() - self.operation_start_time
                metrics.operation_name = self.current_operation
                metrics.error_count = self.error_count
                
                # 添加到历史记录
                self.metrics_history.append(metrics)
                
                # 保持历史记录在限制范围内
                if len(self.metrics_history) > self.max_samples:
                    self.metrics_history.pop(0)
                
                # 检查阈值并触发警报
                self._check_thresholds(metrics)
                
                time.sleep(self.sample_interval)
                
            except Exception as e:
                logger.error(f"监控循环出错: {e}")
                time.sleep(self.sample_interval)

    def _count_active_windows(self) -> int:
        """统计活跃窗口数量"""
        try:
            result = subprocess.run(['wmctrl', '-l'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                return len([line for line in result.stdout.strip().split('\n') if line.strip()])
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass
        return 0

    def _count_x11_connections(self) -> int:
        """统计X11连接数"""
        try:
            # 统计/tmp/.X11-unix/下的套接字数量（粗略估计）
            x11_dir = '/tmp/.X11-unix'
            if os.path.exists(x11_dir):
                return len([f for f in os.listdir(x11_dir) if f.startswith('X')])
        except Exception:
            pass
        return 0

    def _check_thresholds(self, metrics: PerformanceMetrics):
        """检查性能阈值"""
        alerts = []
        
        if metrics.cpu_percent > self.thresholds['cpu_percent']:
            alerts.append(f"CPU使用率过高: {metrics.cpu_percent:.1f}%")
        
        if metrics.memory_percent > self.thresholds['memory_percent']:
            alerts.append(f"内存使用率过高: {metrics.memory_percent:.1f}%")
        
        if metrics.operation_duration > self.thresholds['operation_duration']:
            alerts.append(f"操作耗时过长: {metrics.operation_duration:.1f}秒")
        
        # 计算错误率
        if len(self.metrics_history) > 10:
            recent_errors = sum(1 for m in self.metrics_history[-10:] if m.error_count > 0)
            error_rate = recent_errors / 10
            if error_rate > self.thresholds['error_rate']:
                alerts.append(f"错误率过高: {error_rate:.1%}")
        
        # 触发警报回调
        for alert in alerts:
            for callback in self.alert_callbacks:
                try:
                    callback(alert, metrics)
                except Exception as e:
                    logger.error(f"警报回调执行失败: {e}")

    def start_operation(self, operation_name: str):
        """开始监控一个操作"""
        self.current_operation = operation_name
        self.operation_start_time = time.time()
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(f"开始监控操作: {operation_name}")

    def end_operation(self, success: bool = True):
        """结束操作监控"""
        if self.operation_start_time:
            duration = time.time() - self.operation_start_time
            if not success:
                self.error_count += 1
            
            if logger.isEnabledFor(logging.DEBUG):
                status = "成功" if success else "失败"
                logger.debug(f"操作结束: {self.current_operation} ({status}, {duration:.2f}秒)")
        
        self.current_operation = ""
        self.operation_start_time = None

    def add_alert_callback(self, callback: Callable):
        """添加警报回调函数"""
        self.alert_callbacks.append(callback)

    def get_current_metrics(self) -> Optional[PerformanceMetrics]:
        """获取当前性能指标"""
        if self.metrics_history:
            return self.metrics_history[-1]
        return None

    def get_average_metrics(self, last_n_samples: int = 60) -> Dict:
        """获取平均性能指标"""
        if not self.metrics_history:
            return {}
        
        samples = self.metrics_history[-last_n_samples:]
        if not samples:
            return {}
        
        return {
            'avg_cpu_percent': sum(m.cpu_percent for m in samples) / len(samples),
            'avg_memory_percent': sum(m.memory_percent for m in samples) / len(samples),
            'avg_memory_used_mb': sum(m.memory_used_mb for m in samples) / len(samples),
            'total_disk_read_mb': sum(m.disk_io_read_mb for m in samples),
            'total_disk_write_mb': sum(m.disk_io_write_mb for m in samples),
            'total_network_sent_mb': sum(m.network_sent_mb for m in samples),
            'total_network_recv_mb': sum(m.network_recv_mb for m in samples),
            'total_errors': sum(m.error_count for m in samples),
            'sample_count': len(samples)
        }

    def generate_performance_report(self) -> str:
        """生成性能报告"""
        if not self.metrics_history:
            return "暂无性能数据"
        
        avg_metrics = self.get_average_metrics()
        current = self.get_current_metrics()
        
        report_lines = [
            "=== RPALite Linux性能报告 ===",
            f"报告时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"监控样本数: {len(self.metrics_history)}",
            "",
            "=== 系统信息 ===",
            f"操作系统: {self.system_info.os_version}",
            f"内核版本: {self.system_info.kernel_version}",
            f"桌面环境: {self.system_info.desktop_environment}",
            f"X11服务器: {self.system_info.x11_server}",
            f"CPU核心数: {self.system_info.cpu_cores}",
            f"总内存: {self.system_info.available_memory_gb:.1f} GB",
            f"屏幕分辨率: {self.system_info.screen_resolution}",
            "",
            "=== 已安装工具 ===",
        ]
        
        for tool, installed in self.system_info.installed_tools.items():
            status = "✓" if installed else "✗"
            report_lines.append(f"  {tool}: {status}")
        
        if avg_metrics:
            report_lines.extend([
                "",
                "=== 平均性能指标 ===",
                f"CPU使用率: {avg_metrics['avg_cpu_percent']:.1f}%",
                f"内存使用率: {avg_metrics['avg_memory_percent']:.1f}%",
                f"内存使用量: {avg_metrics['avg_memory_used_mb']:.1f} MB",
                f"磁盘读取: {avg_metrics['total_disk_read_mb']:.2f} MB",
                f"磁盘写入: {avg_metrics['total_disk_write_mb']:.2f} MB",
                f"网络发送: {avg_metrics['total_network_sent_mb']:.2f} MB",
                f"网络接收: {avg_metrics['total_network_recv_mb']:.2f} MB",
                f"错误次数: {avg_metrics['total_errors']}"
            ])
        
        if current:
            report_lines.extend([
                "",
                "=== 当前状态 ===",
                f"当前CPU: {current.cpu_percent:.1f}%",
                f"当前内存: {current.memory_percent:.1f}%",
                f"活跃窗口: {current.active_windows_count}",
                f"X11连接: {current.x11_connections}",
                f"当前操作: {current.operation_name or '无'}",
                f"操作时长: {current.operation_duration:.1f}秒" if current.operation_duration > 0 else ""
            ])
        
        return "\n".join(report_lines)

    def export_metrics_to_json(self, filepath: str):
        """导出性能指标到JSON文件"""
        try:
            data = {
                'system_info': {
                    'os_version': self.system_info.os_version,
                    'kernel_version': self.system_info.kernel_version,
                    'desktop_environment': self.system_info.desktop_environment,
                    'cpu_cores': self.system_info.cpu_cores,
                    'available_memory_gb': self.system_info.available_memory_gb,
                    'screen_resolution': self.system_info.screen_resolution,
                    'installed_tools': self.system_info.installed_tools
                },
                'metrics': [
                    {
                        'timestamp': m.timestamp.isoformat(),
                        'cpu_percent': m.cpu_percent,
                        'memory_percent': m.memory_percent,
                        'memory_used_mb': m.memory_used_mb,
                        'disk_io_read_mb': m.disk_io_read_mb,
                        'disk_io_write_mb': m.disk_io_write_mb,
                        'network_sent_mb': m.network_sent_mb,
                        'network_recv_mb': m.network_recv_mb,
                        'active_windows_count': m.active_windows_count,
                        'x11_connections': m.x11_connections,
                        'operation_duration': m.operation_duration,
                        'operation_name': m.operation_name,
                        'error_count': m.error_count
                    }
                    for m in self.metrics_history
                ]
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"性能数据已导出到: {filepath}")
            
        except Exception as e:
            logger.error(f"导出性能数据失败: {e}")

# 全局监控实例
_linux_monitor = None

def get_linux_monitor() -> LinuxMonitor:
    """获取全局Linux监控实例"""
    global _linux_monitor
    if _linux_monitor is None:
        _linux_monitor = LinuxMonitor()
    return _linux_monitor

def start_performance_monitoring():
    """启动性能监控"""
    monitor = get_linux_monitor()
    monitor.start_monitoring()

def stop_performance_monitoring():
    """停止性能监控"""
    monitor = get_linux_monitor()
    monitor.stop_monitoring()

def operation_monitor(operation_name: str):
    """操作监控装饰器"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            monitor = get_linux_monitor()
            monitor.start_operation(operation_name)
            try:
                result = func(*args, **kwargs)
                monitor.end_operation(success=True)
                return result
            except Exception as e:
                monitor.end_operation(success=False)
                raise
        return wrapper
    return decorator 