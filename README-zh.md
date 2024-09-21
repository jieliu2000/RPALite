# RPALite - 用于 Python 和 Robot Framework 的开源 RPA(Robotic Process Automation，机器人流程自动化)编程库

| [English](README.md) | [中文](README-zh.md) |

## 介绍

RPALite 是一个开源的 RPA(Robotic Process Automation，机器人流程自动化)库。你可以通过 Python 或者[Robot Framework](https://robotframework.org/)使用 RPALite，实现各种自动化任务。

_在目前版本，RPALite 仅支持 Windows 平台，对其他平台的支持将在未来版本中添加。_

## 特性

目前 RPALite 在 Windows 平台支持以下操作：

- 启动应用
- 根据应用名称或者 ClassName 查找应用
- 关闭应用
- 支持对特定文字的鼠标点击
- 支持基于文本框提示词或者文本框标签的文本框定位和输入
- 支持基于坐标的鼠标点击
- 鼠标点击支持左键，右键，和双击
- 支持基于 Windows 控件的名称，类，或者 Automation ID 查找对应控件的坐标
- 支持对基于图片的定位。你可以通过传给 RPALite 一张屏幕局部的图片返回对应图片部分在屏幕上的坐标


## 运行效率优化

RPALite 中最消耗时间的操作是图片识别和 OCR，其中 OCR 部分我们使用了[EasyOCR](https://github.com/JaidedAI/EasyOCR)。EasyOCR 在有独立显卡和 CUDA 支持的电脑上运行效率会更高，所以如果发现 RPALite 运行速度比较慢，可以考虑切换到有独立显卡和 CUDA 支持的电脑上运行，并安装对应的 pytorch 版本。


## 文档
在这份文档的后面部分，我们提供了[快速开始](#快速开始)，让你可以对RPALite有一个简单直接的了解。

以下是更详细的文档链接：

- [Python中使用RPALite的编程指南](docs/zh/python/guide.md)
- [Robot Framework中使用RPALite的编程指南](docs/zh/robot/guide.md)

除了以上文档以外，我们提供一份英文的 Robot Framework Library文档，你可以通过[在线Robot Framework文档](https://jieliu2000.github.io/RPALite/docs/en/robot/RPALite.html)访问。如果你希望在本地打开，可以直接打开[项目目录下的 Robot Framework Library文档](docs/en/robot/RPALite.html)。

## 安装

你可以通过 pip 安装 RPALite：

```bash
pip install RPALite
```

也可以通过下面的方法在下载代码以后进行安装：

### 下载代码后安装

首先将项目克隆到本地：

```bash
git clone https://github.com/jieliu2000/RPALite.git
```

之后进入 rpalite 目录后 build 并安装

```bash
cd RPALite
```

安装 build 所需要的库：

```bash
pip install -r requirements.txt
```

进行项目构建：

```bash
python -m build
```

之后使用 pip 进行安装。以下代码为一个示例，*实际使用时请把 XXX 改成对应的实际版本号*。

```bash
cd dist
pip install rpalite-XXX.tar.gz
```

## 快速开始

正如我们在前面所说的，你可以使用 Python 或者 Robot Framework 使用 RPALite。下面部分是一些示例：

### Python

以下为使用 RPALite 操作 Windows 记事本 (Notepad) 的一个示例：

```python
from RPALite import RPALite
rpalite = RPALite()

# 按下Windows + D以显示桌面
rpalite.send_keys("{VK_LWIN down}D{VK_LWIN up}")

# 运行notepad并输入一段文字
rpalite.run_command("notepad.exe")
rpalite.input_text("This is a demo using RPALite.\n")

# 找到notepad app并关闭
app = rpalite.find_application(".*Notepad")
rpalite.close_app(app)
```

### Robot Framework

以下为使用 RPALite 操作 Notepad 的一个示例：

```robotframework
*** Settings ***
Library    RPALite

*** Test Cases ***
Test Notepad
    Send Keys    {VK_LWIN down}D{VK_LWIN up}
    Run Command    notepad.exe
    ${app} =     Find Application    .*Notepad
    Maximize Window    ${app}
    Input Text    This is a demo using RPALite.
    Close App    ${app}

```


## 贡献者指南

如果你希望为 RPALite 贡献代码，可以直接创建 Pull Request。请确保你的代码风格与现有代码一致，以及通过 tests 目录下的所有测试。此外也请确保你为新增或者修改的代码更新了单元测试。

- Github 代码库：https://github.com/jieliu2000/RPALite
- Gitee 代码库：https://gitee.com/jieliu2000/rpalite
- Gitcode 代码库：https://gitcode.com/jieliu2000/rpalite
