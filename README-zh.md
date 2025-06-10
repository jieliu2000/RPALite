# RPALite - 一个开源的 Python 和 Robot Framework RPA（机器人流程自动化）编程库

| [English](README.md) | [中文](README-zh.md) |

[![PyPI](https://img.shields.io/pypi/v/RPALite?color=blue&label=PyPI%20Package)](https://pypi.org/project/RPALite/)
[![License](https://img.shields.io/github/license/jieliu2000/RPALite)](https://github.com/jieliu2000/RPALite/blob/main/LICENSE)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/RPALite)](https://www.python.org/downloads/)

## 目录

- [简介](#简介)
- [功能特性](#功能特性)
- [平台支持](#平台支持)
- [安装](#安装)
- [快速入门](#快速入门)
  - [Python](#python)
  - [Robot Framework](#robot-framework)
- [文档](#文档)
- [OCR 引擎选项](#OCR引擎选项)
  - [自动语言检测](#自动语言检测)
  - [手动语言配置](#手动语言配置)
- [性能优化](#性能优化)
- [贡献指南](#贡献指南)

## 简介

RPALite 是一个开源的 RPA（机器人流程自动化）库。您可以通过 Python 或 [Robot Framework](https://robotframework.org/) 来使用 RPALite 实现各种自动化任务，只需少量代码即可完成。

RPALite 提供了强大的自动化能力和简洁的 API，让您能够跨不同应用程序自动化 UI 交互、数据输入和基于图像的操作。

RPALite 目前仅支持 Windows 平台。对 macOS 和 Linux 的支持正在积极开发中。

## 功能特性

RPALite 支持以下操作：

- **应用程序管理**

  - 启动应用程序
  - 通过名称或类名查找应用程序
  - 关闭应用程序（支持强制关闭选项）
  - 窗口管理（最大化、最小化、显示桌面）

- **鼠标操作**

  - 通过坐标、文本或图像进行点击
  - 支持左键点击、右键点击和双击操作
  - 鼠标按下/释放操作（用于拖放功能）
  - 滚轮操作
  - 将鼠标移动到文本元素上

- **键盘操作**

  - 在光标位置输入文本
  - 支持特殊键和组合键的高级键盘输入
  - 基于标签的文本框交互

- **视觉自动化**

  - 基于 OCR 的文本识别（支持多种语言）
  - 基于图像的定位和验证
  - 查找屏幕上图像的所有实例
  - 等待文本或图像出现/消失
  - 屏幕录制功能

- **UI 自动化**

  - 通过标签、附近文本或自动化 ID 查找控件
  - 灵活的 UI 元素定位系统
  - 基于元素属性的控件交互

- **实用工具**
  - 剪贴板操作（获取/设置）
  - 屏幕截图功能
  - 同步机制（等待和延时）

## 平台支持

### Windows

- 完整的自动化支持，包括 UI 控件
- Windows 特有功能，如 UI 自动化
- 某些功能可能需要管理员权限

### macOS (开发中)

- 现已提供基本的 macOS 自动化支持
- 支持的主要功能：
  - 应用程序启动和窗口管理
  - 键盘和鼠标输入
  - 屏幕捕获和 OCR 文本检测
  - 剪贴板操作
- 系统依赖项：
  - pyobjc-core：核心 Objective-C 绑定
  - pyobjc-framework-Cocoa：AppKit 和 Foundation 框架
  - pyobjc-framework-Quartz：屏幕捕获和图像处理
  - pyobjc-framework-ApplicationServices：辅助功能和用户输入
  - 推荐 macOS 10.14 或更高版本
- 系统依赖项安装：
  ```bash
  # 安装所需的 macOS 依赖项
  pip install pyobjc-core pyobjc-framework-Cocoa pyobjc-framework-Quartz pyobjc-framework-ApplicationServices
  ```
- 已知限制：
  - 尚未通过辅助功能框架实现 UI 元素识别
  - 对特定应用程序的自动化支持有限
  - 某些功能可能需要在系统设置 > 隐私与安全性中授予额外权限

#### macOS 系统权限设置

要在 macOS 上使用 RPALite，您需要在系统设置中授予必要的权限：

1. **屏幕录制权限**：

   - 前往系统设置 > 隐私与安全性 > 屏幕录制
   - 点击"+"按钮添加应用程序
   - 对于终端(Terminal)：
     - 导航到 `/Applications/Utilities/Terminal.app`（应用程序/实用工具/终端）
     - 选择终端并点击"打开"
   - 对于 VSCode：
     - 导航到 `/Applications/Visual Studio Code.app`（或您的自定义安装位置）
     - 选择 VSCode 并点击"打开"
   - 添加后重启终端或 VSCode
   - 此权限对于截图和 OCR 功能是必需的

2. **辅助功能权限**：

   - 前往系统设置 > 隐私与安全性 > 辅助功能
   - 点击"+"按钮添加应用程序
   - 对于终端(Terminal)：
     - 导航到 `/Applications/Utilities/Terminal.app`（应用程序/实用工具/终端）
     - 选择终端并点击"打开"
   - 对于 VSCode：
     - 导航到 `/Applications/Visual Studio Code.app`
     - 选择 VSCode 并点击"打开"
   - 确保终端和 VSCode 旁边的复选框已勾选
   - 此权限对于鼠标和键盘模拟是必需的

3. **自动化权限**：

   - 当您的脚本尝试控制应用程序时，系统会动态请求这些权限
   - 当系统提示时，点击"好"以允许您的脚本控制目标应用程序
   - 要预先批准应用程序（可选）：
     - 前往系统设置 > 隐私与安全性 > 自动化
     - 您将看到可以控制其他应用程序的应用程序列表
     - 勾选您希望允许终端或 VSCode 控制的应用程序旁边的复选框

4. **直接添加 Python（替代方法）**：
   - 如果您直接使用 Python 运行脚本而不是通过终端/VSCode：
     - 找到您的 Python 安装位置（通常在 `/usr/local/bin/python3` 或虚拟环境中）
     - 将此 Python 可执行文件添加到屏幕录制和辅助功能权限中
   - 如果使用 Homebrew 安装的 Python：
     - 添加 `/opt/homebrew/bin/python3`（对于 Apple Silicon）或 `/usr/local/bin/python3`（对于 Intel Mac）

注意：根据您的 macOS 版本，这些设置的确切路径可能略有不同。在较旧的 macOS 版本中，这些设置在系统偏好设置 > 安全性与隐私 > 隐私中。

#### macOS 问题排查指南

如果您在 macOS 上运行 RPALite 时遇到问题：

1. **权限错误**：

   - 确保您的终端/IDE 拥有所需的权限（参见 macOS 系统权限设置）
   - 尝试使用管理员权限运行脚本：`sudo python your_script.py`
   - 如果系统提示应用程序控制权限，请始终点击"好"

2. **OCR 或截图问题**：

   - 验证是否为您的终端/IDE 授予了屏幕录制权限
   - 尝试使用不同的 OCR 引擎：`rpalite = RPALite(ocr_engine="paddleocr")`
   - 如果文本识别效果不佳，请调整屏幕分辨率或增加字体大小

3. **鼠标/键盘控制问题**：

   - 验证是否授予了辅助功能权限
   - 如果基于文本的点击失败，请使用绝对坐标进行点击
   - 对于键盘输入问题，尝试使用 `send_keys()` 方法而不是 `input_text()`

4. **应用程序启动问题**：
   - 如果 `run_command()` 失败，请指定应用程序的完整路径
   - 对于某些应用程序，使用带 `.app` 扩展名的完整名称：`"Calculator.app"`
   - 检查应用程序包名称是否正确

### Linux

- 支持基于 X11 的桌面环境的完整自动化
- 需要 X Window System (X11) 和图形桌面环境
- 系统依赖项：
  - xdotool：用于键盘和鼠标模拟
  - wmctrl：用于窗口管理
  - python-xlib：用于 X11 交互
- 系统依赖项安装：

  ```bash
  # Ubuntu/Debian
  sudo apt-get install xdotool wmctrl python3-xlib

  # CentOS/RHEL
  sudo yum install xdotool wmctrl python3-xlib

  # Arch Linux
  sudo pacman -S xdotool wmctrl python-xlib
  ```

## 性能优化

RPALite 中最耗时的操作是图像识别和 OCR。对于 OCR，用户可以选择使用 [EasyOCR](https://github.com/JaidedAI/EasyOCR)或者 [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) 进行文本识别。EasyOCR 和 PaddleOCR 在具有独立显卡和 CUDA 支持的计算机上运行效率更高。如果您发现 RPALite 运行缓慢，请考虑在具有独立显卡和 CUDA 支持的计算机上运行，并安装适当版本的 PyTorch。

## 文档

在这份文档的后面部分，我们提供了[快速入门](#快速入门)，让你可以对 RPALite 有一个简单直接的了解。

以下是更详细的文档链接：

- [Python 中使用 RPALite 的编程指南](docs/zh/python/guide.md)
- [Robot Framework 中使用 RPALite 的编程指南](docs/zh/robot/guide.md)

除了以上文档以外，我们提供一份英文的 Robot Framework Library 文档，你可以通过[在线 Robot Framework 文档](https://jieliu2000.github.io/RPALite/docs/en/robot/RPALite.html)访问。如果你希望在本地打开，可以直接打开[项目目录下的 Robot Framework Library 文档](docs/en/robot/RPALite.html)。

## 安装

您可以通过 pip 安装 RPALite：

```bash
pip install RPALite
```

系统会根据您的操作系统自动安装特定平台所需的依赖项。

## 快速入门

如前所述，您可以通过 Python 或 Robot Framework 使用 RPALite。以下是一些示例：

### Python

#### 基础示例

以下是使用 RPALite 操作 Windows 记事本的示例：

```python
from RPALite import RPALite
rpalite = RPALite()

# 显示桌面
rpalite.show_desktop()

# 运行记事本并输入一些文本
rpalite.run_command("notepad.exe")
rpalite.input_text("这是一个使用 RPALite 的演示。\n")

# 查找记事本应用并关闭它
app = rpalite.find_application(".*Notepad")
rpalite.close_app(app)
```

#### Linux 示例

以下是使用 RPALite 操作 Linux 计算器的示例：

```python
from RPALite import RPALite
rpalite = RPALite()

# 启动计算器
rpalite.launch_application("gnome-calculator")  # GNOME 桌面环境
# 或
rpalite.launch_application("kcalc")  # KDE 桌面环境

# 点击数字 5
rpalite.click_text("5")

# 点击加号按钮
rpalite.click_text("+")

# 点击数字 3
rpalite.click_text("3")

# 点击等号按钮
rpalite.click_text("=")

# 验证结果
result = rpalite.get_text_from_coordinates(100, 100)  # 根据您的计算器调整坐标
assert result == "8"
```

#### macOS 示例

以下是使用 RPALite 操作 macOS 计算器的示例：

```python
from RPALite import RPALite
rpalite = RPALite()

# 启动计算器
rpalite.run_command("Calculator")

# 点击数字 5
rpalite.click_text("5")

# 点击加号按钮
rpalite.click_text("+")

# 点击数字 3
rpalite.click_text("3")

# 点击等号按钮
rpalite.click_text("=")

# 获取结果（由于元素检测有限，使用剪贴板）
rpalite.click_text("编辑")
rpalite.click_text("拷贝")
result = rpalite.get_clipboard_text()
assert result.strip() == "8"
```

### 高级键盘输入示例

```python
# 简单文本输入
rpalite.send_keys("欢迎使用 RPALite")

# 特殊键
rpalite.send_keys("{ENTER}")
rpalite.send_keys("{ESC}")

# 组合键
rpalite.send_keys("^c")          # Control+C
rpalite.send_keys("%{F4}")       # Alt+F4
rpalite.send_keys("+(abc)")      # Shift+ABC（大写）
```

### Robot Framework

#### 基础示例

以下是使用 RPALite 操作 Windows 记事本的示例：

```robotframework
*** Settings ***
Library    RPALite

*** Test Cases ***
测试记事本
    Send Keys    {VK_LWIN down}D{VK_LWIN up}
    Run Command    notepad.exe
    ${app} =     Find Application    .*Notepad
    Maximize Window    ${app}
    Input Text    这是一个使用 RPALite 的演示。
    Close App    ${app}
```

#### 高级功能示例

```robotframework
*** Settings ***
Library    RPALite
Library    OperatingSystem

*** Test Cases ***
登录表单自动化
    # 等待文本出现，设置超时时间
    ${position} =    Wait Until Text Shown    登录    timeout=10

    # 点击 UI 元素
    Click By Text    登录

    # 填写表单字段
    Enter In Field    用户名    my_user
    Enter In Field    密码    my_password

    # 截图验证
    ${screenshot} =    Take Screenshot    filename=login_screen.png

    # 等待图像出现
    Wait Until Image Shown    dashboard_icon.png    timeout=15

    # 开始屏幕录制
    ${recording_path} =    Start Screen Recording    fps=15

    # 执行测试操作
    Click By Text    控制面板
    Sleep    2

    # 验证屏幕上存在文本
    Validate Text Exists    欢迎, my_user

    # 停止录制
    ${final_path} =    Stop Screen Recording
    Log    录制保存到: ${final_path}
```

#### 高级键盘输入示例

```robotframework
*** Settings ***
Library    RPALite

*** Test Cases ***
键盘操作
    # 简单文本输入
    Input Text    来自 Robot Framework 的问候！

    # 特殊键和组合键
    Send Keys    {ENTER}
    Send Keys    ^a    # 全选
    Send Keys    ^c    # 复制
    Send Keys    {TAB}
    Send Keys    ^v    # 粘贴

    # 功能键和修饰符
    Send Keys    {F5}
    Send Keys    %{F4}    # Alt+F4

    # 获取剪贴板内容
    ${clipboard_text} =    Get Clipboard Text
    Log    剪贴板内容: ${clipboard_text}
```

## 文档

以下是更详细的文档链接：

- [Python 中使用 RPALite 的编程指南](docs/zh/python/guide.md)
- [Robot Framework 中使用 RPALite 的编程指南](docs/zh/robot/guide.md)

除了以上文档以外，我们提供一份英文的 Robot Framework Library 文档，你可以通过[在线 Robot Framework 文档](https://jieliu2000.github.io/RPALite/docs/en/robot/RPALite.html)访问。如果你希望在本地打开，可以直接打开[项目目录下的 Robot Framework Library 文档](docs/en/robot/RPALite.html)。

## OCR 引擎选项

RPALite 支持两种 OCR 引擎进行文本识别：

- **EasyOCR**（默认）

  - 更好的多语言支持
  - 适合通用 OCR 任务
  - 模型体积较大

- **PaddleOCR**
  - 对中文文本识别效果更好
  - 模型体积更小
  - 推理速度更快

您可以在初始化时指定使用哪个引擎：

```python
# 使用默认引擎（EasyOCR）
rpa = RPALite()

# 使用PaddleOCR
rpa = RPALite(ocr_engine="paddleocr")
```

### 自动语言检测

RPALite 会自动检测您操作系统的显示语言，并为 OCR 引擎添加相应的语言支持。如果您的系统设置为中文，将自动添加中文语言支持以提高文本识别准确性。此功能适用于 EasyOCR 和 PaddleOCR 引擎。

### 手动语言配置

您也可以手动指定 OCR 识别的语言：

```python
# 对于 EasyOCR
rpa = RPALite(ocr_engine="easyocr", languages=["en", "ch_sim", "fr"])

# 对于 PaddleOCR
rpa = RPALite(ocr_engine="paddleocr", languages=["en", "ch", "fr"])
```

**语言代码参考：**

- **EasyOCR**：[支持的语言](https://github.com/JaidedAI/EasyOCR#supported-languages)
- **PaddleOCR**：[语言支持](https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.7/doc/doc_ch/multi_languages.md)

## 性能优化

RPALite 中最耗时的操作是图像识别和 OCR。这两种 OCR 引擎在具有独立显卡和 CUDA 支持的计算机上运行效率更高。如果您发现 RPALite 运行缓慢，请考虑在具有独立显卡和 CUDA 支持的计算机上运行，并安装适当版本的 PyTorch。

## 贡献指南

如果您想为 RPALite 贡献代码，欢迎提交 Pull Request。请确保您的代码风格与现有代码库一致，并通过 tests 目录中的所有测试。此外，请确保为任何新增或修改的代码更新单元测试。

- GitHub 仓库：https://github.com/jieliu2000/RPALite
- Gitee 仓库：https://gitee.com/jieliu2000/rpalite
- Gitcode 仓库：https://gitcode.com/jieliu2000/rpalite
