#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RPALite Linux 综合示例
演示在Linux平台上的各种RPA操作
"""

from RPALite import RPALite
import time

def main():
    # 初始化RPALite，启用调试模式以获得更多信息
    rpalite = RPALite(debug_mode=True)
    
    print("=== RPALite Linux 综合示例 ===")
    
    # 1. 显示桌面
    print("1. 显示桌面...")
    rpalite.show_desktop()
    rpalite.sleep(2)
    
    # 2. 打开文本编辑器
    print("2. 打开文本编辑器...")
    # 尝试常见的Linux文本编辑器
    editors = ["gedit", "kate", "mousepad", "leafpad", "xed"]
    editor_opened = False
    
    for editor in editors:
        try:
            rpalite.run_command(editor)
            rpalite.sleep(3)  # 等待编辑器启动
            editor_opened = True
            print(f"成功打开 {editor}")
            break
        except Exception as e:
            print(f"尝试打开 {editor} 失败: {e}")
            continue
    
    if not editor_opened:
        print("无法打开任何文本编辑器，请确保安装了gedit、kate或其他编辑器")
        return
    
    # 3. 文本输入示例
    print("3. 文本输入示例...")
    sample_text = """这是RPALite在Linux上的测试文本。
支持中文输入和各种操作。
当前时间: """ + time.strftime("%Y-%m-%d %H:%M:%S")
    
    rpalite.input_text(sample_text)
    rpalite.sleep(2)
    
    # 4. 键盘快捷键示例
    print("4. 键盘快捷键示例...")
    # 全选文本
    rpalite.send_keys("^a")
    rpalite.sleep(1)
    
    # 复制文本
    rpalite.send_keys("^c")
    rpalite.sleep(1)
    
    # 新建文档
    rpalite.send_keys("^n")
    rpalite.sleep(2)
    
    # 粘贴文本
    rpalite.send_keys("^v")
    rpalite.sleep(2)
    
    # 5. 截图示例
    print("5. 截图示例...")
    screenshot = rpalite.take_screenshot(filename="linux_test_screenshot.png")
    if screenshot:
        print("截图已保存为 linux_test_screenshot.png")
    
    # 6. 鼠标操作示例
    print("6. 鼠标操作示例...")
    # 获取屏幕尺寸
    screen_width, screen_height = rpalite.get_screen_size()
    print(f"屏幕尺寸: {screen_width}x{screen_height}")
    
    # 移动鼠标到屏幕中央
    center_x, center_y = screen_width // 2, screen_height // 2
    rpalite.mouse_move(center_x, center_y)
    rpalite.sleep(1)
    
    # 7. 滚动示例
    print("7. 滚动示例...")
    # 向下滚动
    rpalite.scroll(-3)
    rpalite.sleep(1)
    # 向上滚动
    rpalite.scroll(3)
    rpalite.sleep(1)
    
    # 8. 剪贴板操作
    print("8. 剪贴板操作...")
    test_clipboard_text = "这是剪贴板测试文本"
    rpalite.copy_text_to_clipboard(test_clipboard_text)
    clipboard_content = rpalite.get_clipboard_text()
    print(f"剪贴板内容: {clipboard_content}")
    
    # 9. 应用程序管理
    print("9. 应用程序管理...")
    # 尝试查找文本编辑器应用
    app = rpalite.find_application("编辑器")  # 可能的中文名称
    if not app:
        app = rpalite.find_application("Text Editor")  # 英文名称
    if not app:
        app = rpalite.find_application("gedit")  # 具体程序名
    
    if app:
        print("找到文本编辑器应用")
        # 最大化窗口
        try:
            rpalite.maximize_window(app)
            print("窗口已最大化")
        except Exception as e:
            print(f"最大化窗口失败: {e}")
        
        rpalite.sleep(3)
        
        # 关闭应用
        try:
            rpalite.close_app(app)
            print("应用已关闭")
        except Exception as e:
            print(f"关闭应用失败: {e}")
    else:
        print("未找到文本编辑器应用")
    
    print("=== Linux示例完成 ===")
    print("注意事项:")
    print("1. 确保安装了xdotool和wmctrl: sudo apt-get install xdotool wmctrl")
    print("2. 某些功能可能需要root权限或特定的桌面环境")
    print("3. 在不同的Linux发行版和桌面环境中，行为可能有所不同")

 