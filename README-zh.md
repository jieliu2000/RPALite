# RPALite - 一个开源的 Python 和 Robot Framework RPA（机器人流程自动化）编程库

| [English](README.md) | [中文](README-zh.md) |

[![PyPI](https://img.shields.io/pypi/v/RPALite?color=blue&label=PyPI%20Package)](https://pypi.org/project/RPALite/)
[![License](https://img.shields.io/github/license/jieliu2000/RPALite)](https://github.com/jieliu2000/RPALite/blob/main/LICENSE)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/RPALite)](https://www.python.org/downloads/)

## 目录

- [简介](#简介)
- [功能特性](#功能特性)
- [平台支持](#平台支持)
- [性能优化](#性能优化)
- [文档](#文档)
- [安装](#安装)
- [快速入门](#快速入门)
  - [Python](#python)
  - [Robot Framework](#robot-framework)
- [贡献指南](#贡献指南)

## 简介

RPALite 是一个开源的 RPA（机器人流程自动化）库。您可以通过 Python 或 [Robot Framework](https://robotframework.org/) 来使用 RPALite 实现各种自动化任务。

RPALite 现在支持 Windows 平台。对 MacOS 和 Linux 的支持正在开发中。

## 功能特性

RPALite 支持以下操作：

- 启动应用程序
- 通过名称或 ClassName 查找应用程序
- 关闭应用程序
- 对特定文本进行鼠标点击
- 基于占位符或标签定位和输入文本框
- 基于坐标的鼠标点击
- 支持左键点击、右键点击和双击操作
- 基于控件名称、类或自动化 ID（Windows）定位控件并获取其坐标
- 基于图像的定位。您可以将部分截图传递给 RPALite，以返回屏幕上对应部分的坐标
- 屏幕录制功能
- 剪贴板操作
- 高级键盘输入支持（包括特殊键和组合键）
- 窗口管理（最大化、最小化、显示桌面）

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
   - 将您的 Python 应用程序或终端添加到允许的应用程序列表中
   - 此权限对于截图和 OCR 功能是必需的

2. **辅助功能权限**：

   - 前往系统设置 > 隐私与安全性 > 辅助功能
   - 将您的 Python 应用程序或终端添加到允许的应用程序列表中
   - 此权限对于鼠标和键盘模拟是必需的

3. **自动化权限**：

   - 首次尝试控制应用程序时，macOS 会提示请求权限
   - 点击"好"以允许您的脚本控制目标应用程序
   - 这些提示会针对您自动化的每个应用程序出现

4. **常见问题**：
   - 如果在授予权限后自动化仍然无法工作，请尝试重启终端或应用程序
   - 对于从不同环境（IDE、终端）运行的脚本，每个环境都需要单独的权限
   - 在某些情况下，您可能需要将 Python 本身添加到权限列表中

注意：根据您的 macOS 版本，这些设置的确切路径可能略有不同。

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

#### Windows 示例

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

#### Windows 示例

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

## 贡献指南

如果您想为 RPALite 贡献代码，欢迎提交 Pull Request。请确保您的代码风格与现有代码库一致，并通过 tests 目录中的所有测试。此外，请确保为任何新增或修改的代码更新单元测试。

- GitHub 仓库：https://github.com/jieliu2000/RPALite
- Gitee 仓库：https://gitee.com/jieliu2000/rpalite
- Gitcode 仓库：https://gitcode.com/jieliu2000/rpalite
