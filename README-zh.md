# RPALite - 一个开源的 Python 和 Robot Framework RPA（机器人流程自动化）编程库

| [English](README.md) | [中文](README-zh.md) |

[![PyPI](https://img.shields.io/pypi/v/RPALite?color=blue&label=PyPI%20Package)](https://pypi.org/project/RPALite/)
[![License](https://img.shields.io/github/license/jieliu2000/RPALite)](https://github.com/jieliu2000/RPALite/blob/main/LICENSE)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/RPALite)](https://www.python.org/downloads/)

## 目录

- [简介](#简介)
- [功能特性](#功能特性)
- [平台支持](#平台支持)
- [OCR 引擎选项](#OCR引擎选项)
- [性能优化](#性能优化)
- [文档](#文档)
- [安装](#安装)
- [快速入门](#快速入门)
  - [Python](#python)
  - [Robot Framework](#robot-framework)
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

- macOS 支持目前正在开发中
- 代码尚未稳定，因此暂时禁用了 macOS 相关功能
- 我们正在努力在未来的版本中提供完整的 macOS 支持

### Linux (计划中)

- Linux 支持计划在未来版本中提供
- 目前处于早期设计阶段

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

## 性能优化

RPALite 中最耗时的操作是图像识别和 OCR。这两种 OCR 引擎在具有独立显卡和 CUDA 支持的计算机上运行效率更高。如果您发现 RPALite 运行缓慢，请考虑在具有独立显卡和 CUDA 支持的计算机上运行，并安装适当版本的 PyTorch。

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

#### 高级功能示例

```python
from RPALite import RPALite
rpalite = RPALite()

# 等待文本出现，设置超时时间
position = rpalite.wait_until_text_shown("登录", timeout=10)

# 点击由文本标识的按钮
rpalite.click_by_text("登录")

# 操作表单字段
rpalite.enter_in_field("用户名", "my_user")
rpalite.enter_in_field("密码", "my_password")

# 等待图像出现
rpalite.wait_until_image_shown("dashboard_icon.png", timeout=15)

# 开始屏幕录制
recording_path = rpalite.start_screen_recording(fps=15)

# 执行一些操作...

# 停止录制
rpalite.stop_screen_recording()
```

#### 高级键盘输入示例

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

## 贡献指南

如果您想为 RPALite 贡献代码，欢迎提交 Pull Request。请确保您的代码风格与现有代码库一致，并通过 tests 目录中的所有测试。此外，请确保为任何新增或修改的代码更新单元测试。

- GitHub 仓库：https://github.com/jieliu2000/RPALite
- Gitee 仓库：https://gitee.com/jieliu2000/rpalite
- Gitcode 仓库：https://gitcode.com/jieliu2000/rpalite
