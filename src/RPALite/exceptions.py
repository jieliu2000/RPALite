#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RPALite Exception Classes Definition
Defines project-specific exception types for more precise error handling
"""


class RPALiteException(Exception):
    """RPALite base exception class"""
    
    def __init__(self, message: str, error_code: str = None, details: dict = None):
        """
        Initialize exception
        
        Parameters
        ----------
        message : str
            Error message
        error_code : str, optional
            Error code
        details : dict, optional
            Additional error details
        """
        super().__init__(message)
        self.message = message
        self.error_code = error_code or 'RPALITE_ERROR'
        self.details = details or {}
    
    def __str__(self):
        base_msg = f"[{self.error_code}] {self.message}"
        if self.details:
            details_str = ", ".join([f"{k}={v}" for k, v in self.details.items()])
            base_msg += f" ({details_str})"
        return base_msg


class PlatformNotSupportedException(RPALiteException):
    """Platform not supported exception"""
    
    def __init__(self, platform: str, supported_platforms: list = None):
        supported = supported_platforms or ['Windows', 'macOS', 'Linux']
        message = f"Platform '{platform}' is not supported. Supported platforms: {', '.join(supported)}"
        super().__init__(
            message=message,
            error_code='PLATFORM_NOT_SUPPORTED',
            details={'platform': platform, 'supported': supported}
        )


class DependencyMissingException(RPALiteException):
    """Dependency missing exception"""
    
    def __init__(self, dependency: str, install_command: str = None, platform: str = None):
        message = f"Dependency missing: {dependency}"
        if install_command:
            message += f". Install command: {install_command}"
        
        details = {'dependency': dependency}
        if install_command:
            details['install_command'] = install_command
        if platform:
            details['platform'] = platform
        
        super().__init__(
            message=message,
            error_code='DEPENDENCY_MISSING',
            details=details
        )


class WindowNotFoundException(RPALiteException):
    """Window not found exception"""
    
    def __init__(self, window_title: str = None, window_class: str = None, window_id: str = None):
        if window_title:
            message = f"Window with title '{window_title}' not found"
        elif window_class:
            message = f"Window with class '{window_class}' not found"
        elif window_id:
            message = f"Window with ID '{window_id}' not found"
        else:
            message = "Specified window not found"
        
        super().__init__(
            message=message,
            error_code='WINDOW_NOT_FOUND',
            details={
                'window_title': window_title,
                'window_class': window_class,
                'window_id': window_id
            }
        )


class ImageNotFoundException(RPALiteException):
    """图像未找到异常"""
    
    def __init__(self, image_path: str = None, confidence: float = None):
        message = "未找到指定图像"
        if image_path:
            message += f": {image_path}"
        
        details = {}
        if image_path:
            details['image_path'] = image_path
        if confidence:
            details['confidence'] = confidence
        
        super().__init__(
            message=message,
            error_code='IMAGE_NOT_FOUND',
            details=details
        )


class TextNotFoundException(RPALiteException):
    """文本未找到异常"""
    
    def __init__(self, text: str, timeout: int = None):
        message = f"未找到文本: '{text}'"
        if timeout:
            message += f" (超时: {timeout}秒)"
        
        super().__init__(
            message=message,
            error_code='TEXT_NOT_FOUND',
            details={'text': text, 'timeout': timeout}
        )


class ControlNotFoundException(RPALiteException):
    """控件未找到异常"""
    
    def __init__(self, control_type: str = None, control_name: str = None, 
                 control_id: str = None, details: dict = None):
        message = "未找到指定控件"
        
        error_details = details or {}
        if control_type:
            error_details['control_type'] = control_type
            message += f" (类型: {control_type})"
        if control_name:
            error_details['control_name'] = control_name
            message += f" (名称: {control_name})"
        if control_id:
            error_details['control_id'] = control_id
            message += f" (ID: {control_id})"
        
        super().__init__(
            message=message,
            error_code='CONTROL_NOT_FOUND',
            details=error_details
        )


class ScreenshotException(RPALiteException):
    """截图异常"""
    
    def __init__(self, reason: str = None):
        message = "截图失败"
        if reason:
            message += f": {reason}"
        
        super().__init__(
            message=message,
            error_code='SCREENSHOT_FAILED',
            details={'reason': reason}
        )


class OCRException(RPALiteException):
    """OCR识别异常"""
    
    def __init__(self, engine: str = None, reason: str = None):
        message = "OCR识别失败"
        if engine:
            message += f" (引擎: {engine})"
        if reason:
            message += f": {reason}"
        
        super().__init__(
            message=message,
            error_code='OCR_FAILED',
            details={'engine': engine, 'reason': reason}
        )


class KeyboardInputException(RPALiteException):
    """键盘输入异常"""
    
    def __init__(self, keys: str = None, reason: str = None):
        message = "键盘输入失败"
        if keys:
            message += f" (按键: {keys})"
        if reason:
            message += f": {reason}"
        
        super().__init__(
            message=message,
            error_code='KEYBOARD_INPUT_FAILED',
            details={'keys': keys, 'reason': reason}
        )


class MouseOperationException(RPALiteException):
    """鼠标操作异常"""
    
    def __init__(self, operation: str = None, position: tuple = None, reason: str = None):
        message = "鼠标操作失败"
        if operation:
            message += f" (操作: {operation})"
        if position:
            message += f" (位置: {position})"
        if reason:
            message += f": {reason}"
        
        super().__init__(
            message=message,
            error_code='MOUSE_OPERATION_FAILED',
            details={'operation': operation, 'position': position, 'reason': reason}
        )


class SystemCommandException(RPALiteException):
    """系统命令执行异常"""
    
    def __init__(self, command: str = None, return_code: int = None, 
                 stdout: str = None, stderr: str = None):
        message = "系统命令执行失败"
        if command:
            message += f": {command}"
        if return_code is not None:
            message += f" (返回码: {return_code})"
        
        super().__init__(
            message=message,
            error_code='SYSTEM_COMMAND_FAILED',
            details={
                'command': command,
                'return_code': return_code,
                'stdout': stdout,
                'stderr': stderr
            }
        )


class TimeoutException(RPALiteException):
    """超时异常"""
    
    def __init__(self, operation: str = None, timeout: int = None):
        message = "操作超时"
        if operation:
            message += f": {operation}"
        if timeout:
            message += f" ({timeout}秒)"
        
        super().__init__(
            message=message,
            error_code='OPERATION_TIMEOUT',
            details={'operation': operation, 'timeout': timeout}
        )


class ConfigurationException(RPALiteException):
    """配置异常"""
    
    def __init__(self, config_key: str = None, reason: str = None):
        message = "配置错误"
        if config_key:
            message += f" (配置项: {config_key})"
        if reason:
            message += f": {reason}"
        
        super().__init__(
            message=message,
            error_code='CONFIGURATION_ERROR',
            details={'config_key': config_key, 'reason': reason}
        )


class LinuxEnvironmentException(RPALiteException):
    """Linux环境异常"""
    
    def __init__(self, environment_issue: str = None, suggestion: str = None):
        message = "Linux环境问题"
        if environment_issue:
            message += f": {environment_issue}"
        if suggestion:
            message += f"。建议: {suggestion}"
        
        super().__init__(
            message=message,
            error_code='LINUX_ENVIRONMENT_ERROR',
            details={'issue': environment_issue, 'suggestion': suggestion}
        )


def handle_exception_gracefully(func):
    """
    异常处理装饰器
    将常见的底层异常转换为RPALite特定异常
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError as e:
            raise DependencyMissingException(str(e))
        except subprocess.TimeoutExpired as e:
            raise TimeoutException(f"命令超时: {e.cmd}", e.timeout)
        except subprocess.CalledProcessError as e:
            raise SystemCommandException(
                command=e.cmd,
                return_code=e.returncode,
                stdout=getattr(e, 'stdout', None),
                stderr=getattr(e, 'stderr', None)
            )
        except ImportError as e:
            dependency = str(e).split("'")[1] if "'" in str(e) else str(e)
            raise DependencyMissingException(dependency)
        except Exception as e:
            # 如果已经是RPALite异常，直接抛出
            if isinstance(e, RPALiteException):
                raise
            # 否则包装为通用RPALite异常
            raise RPALiteException(f"未知错误: {str(e)}", 'UNKNOWN_ERROR')
    
    return wrapper 