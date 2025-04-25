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

- macOS 支持目前正在开发中
- 代码尚未稳定，因此暂时禁用了 macOS 相关功能
- 我们正在努力在未来的版本中提供完整的 macOS 支持

## 性能优化

RPALite 中最耗时的操作是图像识别和 OCR。对于 OCR，用户可以选择使用 [EasyOCR](https://github.com/JaidedAI/EasyOCR)或者 [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) 进行文本识别。EasyOCR和PaddleOCR 在具有独立显卡和 CUDA 支持的计算机上运行效率更高。如果您发现 RPALite 运行缓慢，请考虑在具有独立显卡和 CUDA 支持的计算机上运行，并安装适当版本的 PyTorch。

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
