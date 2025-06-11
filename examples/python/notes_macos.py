#!/usr/bin/env python3
"""
本文档提供中英文双语说明 / This document provides bilingual instructions in Chinese and English

=== English Introduction ===
RPALite macOS Notes Demo

This script demonstrates how to use RPALite to automate tasks on macOS.
It will open the Notes app, create a new note from the menu, type some text, and close the app.

=== Running the Example ===

Before running this example, you must grant necessary permissions:

1. System Settings > Privacy & Security > Screen Recording:
   - Add Terminal or Visual Studio Code (depending on where you're running this)
   
2. System Settings > Privacy & Security > Accessibility:
   - Add Terminal or Visual Studio Code (depending on where you're running this)

3. System Settings > Privacy & Security > Automation:
   - You'll be prompted to grant automation permissions when the script runs

=== Terminal Instructions ===

To run this example in Terminal:
1. Open Terminal (Applications > Utilities > Terminal)
2. Navigate to the example directory:
   ```
   cd path/to/examples/python
   ```
3. Run the script:
   ```
   python notes_macos.py
   ```
4. If prompted for permissions, click "OK" to allow

=== VSCode Instructions ===

To run this example in VSCode:
1. Open VSCode and this file
2. Make sure VSCode has required permissions (see above)
3. Open the terminal in VSCode or use the Run button
4. If using the terminal, run:
   ```
   python notes_macos.py
   ```
5. If prompted for permissions, click "OK" to allow

=== Troubleshooting ===

If the example doesn't work:
- Ensure Terminal/VSCode has proper permissions
- Try restarting Terminal/VSCode after granting permissions
- If you're running Python directly (not through Terminal/VSCode), add Python to permissions

=== 中文说明 ===

RPALite macOS 备忘录演示

此脚本演示如何使用 RPALite 在 macOS 上自动化任务。
它将打开备忘录应用程序，从菜单创建新备忘录，输入一些文本，然后关闭应用程序。

=== 运行示例 ===

在运行此示例之前，您必须授予必要的权限：

1. 系统设置 > 隐私与安全性 > 屏幕录制：
   - 添加终端或 Visual Studio Code（取决于您在哪里运行此脚本）
   
2. 系统设置 > 隐私与安全性 > 辅助功能：
   - 添加终端或 Visual Studio Code（取决于您在哪里运行此脚本）

3. 系统设置 > 隐私与安全性 > 自动化：
   - 脚本运行时会提示您授予自动化权限

=== 终端运行说明 ===

在终端中运行此示例：
1. 打开终端（应用程序 > 实用工具 > 终端）
2. 导航到示例目录：
   ```
   cd path/to/examples/python
   ```
3. 运行脚本：
   ```
   python notes_macos.py
   ```
4. 如果提示权限，点击"确定"允许

=== VSCode 运行说明 ===

在 VSCode 中运行此示例：
1. 打开 VSCode 和此文件
2. 确保 VSCode 具有所需权限（见上文）
3. 在 VSCode 中打开终端或使用运行按钮
4. 如果使用终端，运行：
   ```
   python notes_macos.py
   ```
5. 如果提示权限，点击"确定"允许

=== 故障排除 ===

如果示例无法运行：
- 确保终端/VSCode 具有适当的权限
- 授予权限后尝试重启终端/VSCode
- 如果您直接运行 Python（不通过终端/VSCode），请将 Python 添加到权限中
"""

from RPALite import RPALite
from datetime import datetime

# Initialize RPALite
rpalite = RPALite() 

try:
    # Launch Notes app
    print("Launching Notes app...")
    rpalite.run_command("Notes")
    
    # Wait a moment for the app to fully load
    rpalite.sleep(2)
    
    # Create a new note using the File menu
    rpalite.click_by_text("Notes")

    print("Creating a new note from File menu...")
    rpalite.click_by_text("File")
    rpalite.sleep(1)
    rpalite.click_by_text("New Note")
    
    # Wait for the new note to be created
    rpalite.sleep(2)
    
    # Type some text in the note
    print("Typing text in the note...")
    sample_text = """RPALite Notes Demo

This is a demonstration of RPALite automation with macOS Notes app.

Today's date: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """

Features demonstrated:
• Opening Notes app
• Creating new note via menu
• Typing formatted text
• Closing app properly

RPALite makes macOS automation simple and powerful!"""
    
    rpalite.input_text(sample_text)
    
    # Wait to see the typed content
    print("Note created successfully! Waiting 3 seconds to display content...")
    rpalite.sleep(3)
    
    # Close Notes app using the File menu
    print("Closing Notes app via File menu...")
    rpalite.click_by_text("File")
    rpalite.sleep(1)
    rpalite.click_by_text("Close")
    
    print("Demo completed successfully!")
    print("The note has been saved automatically and Notes app has been closed.")
    
except Exception as e:
    print(f"An error occurred: {e}")
    print("Check that you've granted all required permissions.")
    # Try to close Notes using keyboard shortcut as fallback
    try:
        print("Attempting to close Notes using keyboard shortcut...")
        rpalite.send_keys("^q")  # Command+Q on macOS
    except:
        print("Could not close Notes automatically. Please close it manually.")
    
finally:
    print("Demo completed.") 